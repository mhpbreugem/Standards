#!/usr/bin/env python3
"""
run_task.py — cross-repo task driver (Standards runner).

Runs inside a checkout of a *project* repo (e.g. MIWN) that has Standards present
as the standards/ submodule. Reads the project's todo/runner.config.json to locate
its queue, problems, and output pool, then:

    find ready task -> claim (git-race lock) -> allocate vNNNN (shared counter)
      -> invoke numerics/<problem>/solve.py -> write solutions/pool/<problem>/vNNNN/
      -> mark the task done (queue + solution committed back to the project repo)

This is the cross-repo replacement for the old monorepo solve.py wrapper: it keeps
the locking authority in claim_task.py and the math in the shared methods, while
the per-paper params/queue/pool stay in the project repo.

Usage:
    # production (inside a MIWN checkout, origin = MIWN, submodule initialized):
    REPO_ROOT=$PWD WORKER_ID=ci-1 BRANCH=main \\
        python3 standards/runner/run_task.py --config todo/runner.config.json

    # safe local dry-run (no git commits/pushes, no REST):
    REPO_ROOT=$PWD python3 standards/runner/run_task.py \\
        --config todo/runner.config.json --local --G 5
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # standards/runner
sys.path.insert(0, str(HERE))
import claim_task as ct  # noqa: E402  (same dir)


def repo_root() -> Path:
    root = os.environ.get("REPO_ROOT")
    if root:
        return Path(root).resolve()
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip() if out.returncode == 0 else ".").resolve()


def load_config(repo: Path, cfg_rel: str) -> dict:
    cfg = repo / cfg_rel
    if not cfg.exists():
        raise SystemExit(f"run_task: config not found: {cfg}")
    return json.loads(cfg.read_text())


def alloc_version(repo: Path, problem: str) -> tuple[str, Path]:
    """Next vNNNN from max(REGISTRY counter, existing pool dirs) + 1 (shared counter)."""
    reg_path = repo / "solutions" / "REGISTRY.json"
    reg = json.loads(reg_path.read_text()) if reg_path.exists() else {}
    counter = int(reg.get("counters", {}).get(problem, 0))

    pool = repo / "solutions" / "pool" / problem
    max_dir = 0
    if pool.exists():
        for d in pool.iterdir():
            if d.is_dir() and d.name.startswith("v") and d.name[1:].isdigit():
                max_dir = max(max_dir, int(d.name[1:]))

    n = max(counter, max_dir) + 1
    return f"v{n:04d}", reg_path


def bump_counter(reg_path: Path, problem: str, version: str) -> None:
    """Record counters.<problem> = N (preserves the solutions[] list solve.py wrote)."""
    reg = json.loads(reg_path.read_text()) if reg_path.exists() else {"registry_version": 1, "solutions": []}
    reg.setdefault("counters", {})[problem] = int(version[1:])
    reg_path.write_text(json.dumps(reg, indent=2) + "\n")


def run_solver(repo: Path, spec: dict, task: dict, version: str, g_override: int | None,
               max_seconds: float, worker_id: str) -> Path:
    """Invoke the project's own numerics/<problem>/solve.py for one (gamma, tau)."""
    entry = spec.get("solver", {}).get("entrypoint", f"numerics/{task['problem']}/solve.py")
    G = g_override if g_override is not None else int(spec.get("solver", {}).get("G", 15))
    u_max = float(spec.get("solver", {}).get("u_max", 3.0))
    cmd = [
        sys.executable, entry,
        "--gamma", str(task["gamma"]),
        "--tau", str(task["tau"]),
        "--G", str(G),
        "--u-max", str(u_max),
        "--max-seconds", str(max_seconds),
        "--version", version,
        "--task-id", task["id"],
        "--worker-id", worker_id,
        # NOTE: git-push progress reporting is disabled — it contended with the
        # done-commit under N workers. Live progress will return via the REST API.
    ]
    print(f"[run_task] solve: {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=str(repo))
    if r.returncode != 0:
        raise SystemExit(f"run_task: solver exited {r.returncode} for {task['id']}")
    vdir = repo / "solutions" / "pool" / task["problem"] / version
    if not (vdir / "meta.json").exists():
        raise SystemExit(f"run_task: solver did not write {vdir}/meta.json")
    return vdir


def result_from_meta(vdir: Path, version: str) -> dict:
    meta = json.loads((vdir / "meta.json").read_text())
    m = meta.get("metrics", {})
    return {
        "1-R2": m.get("one_minus_R2"),
        "F_max": m.get("F_inf"),
        "version": version,
        "standards_methods_sha": meta.get("standards_methods_sha"),
    }


# --------------------------------------------------------------------------- #
# Queue transitions (local vs git-backed)
# --------------------------------------------------------------------------- #

def claim_local(project: str, task_id: str, worker_id: str) -> bool:
    q = ct.load_queue(project)
    t = ct._find_by_id(q, task_id)
    if t is None or t["status"] != "ready":
        return False
    t["status"] = "claimed"
    t["claimed_by"] = worker_id
    t["claimed_at"] = ct._now()
    ct.save_queue(project, q)
    return True


def finish_local(project: str, task_id: str, checkpoint: str, result: dict) -> None:
    q = ct.load_queue(project)
    t = ct._find_by_id(q, task_id)
    t["status"] = "done"
    t["checkpoint"] = checkpoint
    t["result"] = result
    t["completed_at"] = ct._now()
    t.pop("claimed_by", None)
    t.pop("claimed_at", None)
    ct._unblock_downstream(q)
    ct._update_summary(q)
    ct.save_queue(project, q)


def _robust_commit(branch: str, mutate, extra_paths=(), message: str = "update",
                   attempts: int = 25) -> bool:
    """Land a single-task queue change under N-worker contention.

    The queue (TASK_QUEUE.json) is one file every worker edits, so a plain
    pull --rebase conflicts and loses the change. Instead, on every attempt we
    re-sync to origin, re-apply our one change onto the *fresh* queue, add any
    unique solution files (which never conflict), commit, and push. Retries until
    it lands — optimistic concurrency via git.

    `mutate()` edits the on-disk queue and returns False if there's nothing to do
    (e.g. the task is already in the target state).
    """
    for i in range(attempts):
        ct._git("fetch", "origin", branch, check=False)
        ct._git("reset", "--mixed", f"origin/{branch}", check=False)   # HEAD->origin, keep working files
        ct._git("checkout", f"origin/{branch}", "--", ct.queue_rel(), check=False)  # fresh queue
        if mutate() is False:
            return True
        ct._git("add", ct.queue_rel(), *extra_paths, check=False)
        if ct._git("diff", "--cached", "--quiet", check=False).returncode == 0:
            return True
        ct._git("commit", "-m", message, check=False)
        if ct._push(branch):
            return True
        time.sleep(1 + (i % 4))
    return False


def finish_git(repo: Path, project: str, task_id: str, checkpoint: str,
               result: dict, branch: str, version_dir: Path) -> bool:
    """Commit the (unique) solution dir + flip the task done, robust to contention."""
    soln_rel = os.path.relpath(version_dir, repo)

    def _mut():
        q = ct.load_queue(project)
        t = ct._find_by_id(q, task_id)
        if t is None or t.get("status") == "done":
            return False
        t["status"] = "done"
        t["checkpoint"] = checkpoint
        t["result"] = result
        t["completed_at"] = ct._now()
        t.pop("claimed_by", None)
        t.pop("claimed_at", None)
        ct._unblock_downstream(q)
        ct._update_summary(q)
        ct.save_queue(project, q)
        return True

    return _robust_commit(branch, _mut, extra_paths=[soln_rel],
                          message=f"{task_id}: done {checkpoint}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Cross-repo task driver (Standards runner).")
    ap.add_argument("--config", default="todo/runner.config.json",
                    help="repo-relative path to runner.config.json")
    ap.add_argument("--task-id", help="specific task (default: next ready task)")
    ap.add_argument("--worker-id", default=os.environ.get("WORKER_ID", "run_task-1"))
    ap.add_argument("--branch", default=os.environ.get("BRANCH", "main"))
    ap.add_argument("--G", type=int, default=None, help="grid override (e.g. small for a dry-run)")
    ap.add_argument("--max-seconds", type=float, default=90.0,
                    help="per-solve wall cap passed to the solver (never hangs a worker)")
    ap.add_argument("--local", action="store_true",
                    help="no git/REST: claim+done edit the queue file in place (dry-run)")
    args = ap.parse_args()

    repo = repo_root()
    os.environ["REPO_ROOT"] = str(repo)            # claim_task resolves paths from here
    cfg = load_config(repo, args.config)
    project = cfg.get("project", "project")
    os.environ["QUEUE_REL"] = cfg["queue_path"]    # claim_task queue location
    problems_dir = cfg.get("problems_dir", "numerics")

    # 1. pick a task
    if args.task_id:
        q = ct.load_queue(project)
        task = ct._find_by_id(q, args.task_id)
        if task is None or task["status"] != "ready":
            print(f"[run_task] task {args.task_id} is not ready", flush=True)
            return 1
    else:
        task = ct.find_ready_task(project, args.worker_id)
        if task is None:
            print("[run_task] no ready task — queue drained", flush=True)
            return 3   # distinct code so a worker loop can stop cleanly
    print(f"[run_task] picked {task['id']} (problem={task['problem']} "
          f"gamma={task['gamma']} tau={task['tau']})", flush=True)

    # 2. claim
    if args.local:
        claimed = claim_local(project, task["id"], args.worker_id)
    else:
        claimed = ct.try_claim(project, task["id"], args.worker_id, args.branch)
    if not claimed:
        print(f"[run_task] could not claim {task['id']} (another worker beat us)", flush=True)
        return 1
    print(f"[run_task] claimed {task['id']}", flush=True)

    # 3. allocate version, 4. solve, 5. write-back
    spec = json.loads((repo / problems_dir / task["problem"] / "spec.json").read_text())
    version, reg_path = alloc_version(repo, task["problem"])
    try:
        vdir = run_solver(repo, spec, task, version, args.G, args.max_seconds, args.worker_id)
    except SystemExit as e:
        reason = str(e)
        print(f"[run_task] solve rejected/failed: {reason}", flush=True)
        # Park as skip (not bail+requeue) — a worker moves on.
        def _mut_skip():
            q = ct.load_queue(project); t = ct._find_by_id(q, task["id"])
            if t is None or t.get("status") == "skip":
                return False
            t["status"] = "skip"; t["result"] = {"reason": reason}
            t.pop("claimed_by", None); t.pop("claimed_at", None)
            ct._update_summary(q); ct.save_queue(project, q)
            return True
        if args.local:
            _mut_skip()
        else:
            _robust_commit(args.branch, _mut_skip, message=f"{task['id']}: skip ({reason[:40]})")
        return 0

    bump_counter(reg_path, task["problem"], version)
    checkpoint = f"solutions/pool/{task['problem']}/{version}/"
    result = result_from_meta(vdir, version)

    # 6. mark done
    if args.local:
        finish_local(project, task["id"], checkpoint, result)
        ok = True
    else:
        ok = finish_git(repo, project, task["id"], checkpoint, result, args.branch, vdir)
    print(f"[run_task] {'done' if ok else 'FAILED to land done'}: {task['id']} -> {checkpoint} "
          f"(1-R2={result['1-R2']}, F={result['F_max']})", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
