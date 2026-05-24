# Runner

Project-agnostic infrastructure to coordinate VMs and workers running a
distributed task queue. Imported from `mhpbreugem/fixed-point-factory` `core/`
@ `4875059` (2026-05-22). None of these files name a specific project — the math,
queue, and checkpoints live in each paper's own repo.

## Files

| File | Purpose |
|------|---------|
| `create_gcp_vm.sh` | Spin up a GCP spot VM (1-hour max-run-duration) |
| `bootstrap.sh` | VM startup: install deps, clone repo, start the worker loop |
| `claim_task.py` | Git-race optimistic locking on `TASK_QUEUE.json`: claim / done / bail / release / status |
| `run_task.py` | **Cross-repo task driver**: claim → allocate `vNNNN` → run the project's solver → write the solution back |
| `web/` | **Dashboard** (GitHub Pages): status / workers / mobile UI that reads a project repo's queue, solutions, and figure data via the GitHub API. Pointed at a project via `OWNER`/`REPO`/`BRANCH` at the top of each page (currently `mhpbreugem/MIWN`). Deployed by `.github/workflows/pages.yml` (enable Settings → Pages → Source = GitHub Actions). |
| `supervisor.py` | Local monitoring: VM health, stale claims, queue status |
| `heartbeat.sh` | Worker liveness: write a timestamp every 5 min and push |
| `progress.py` | Structured progress reporting (see `PROGRESS_FORMAT.md`) |
| `TASK_SCHEMA.md` | JSON schema + lifecycle rules for `TASK_QUEUE.json` |
| `PROGRESS_FORMAT.md` | Progress-record format |
| `SOLVER_INSTRUCTIONS.md` | Generic worker protocol (claim → solve → done) |

## Cross-repo mode (current)

The runner operates on an **external project repo** (a paper repo such as MIWN)
that vendors Standards as the `standards/` submodule. It does **not** assume the
old single-repo `projects/<name>/` layout — that auto-path has been dropped.

The consuming project provides a `todo/runner.config.json`:

```json
{ "queue_path": "todo/TASK_QUEUE.json", "problems_dir": "numerics",
  "output_pool": "solutions/pool", "write_back": true }
```

and the runner is driven from a checkout of that repo (its git `origin` is the
project repo, so all claim/done commits land there):

```sh
REPO_ROOT=$PWD WORKER_ID=ci-1 BRANCH=main \
    python3 standards/runner/run_task.py --config todo/runner.config.json
```

- **Queue location** is supplied by the project: `claim_task.py` reads
  `QUEUE_REL` (env) or `--queue-path` (e.g. `todo/TASK_QUEUE.json`). The git-race
  optimistic-lock protocol is unchanged — it operates on whatever repo
  `repo_root()` / `REPO_ROOT` points at, and `_gh_repo()` resolves the project
  automatically from `origin`.
- **`run_task.py`** finds a ready task, claims it, allocates the next immutable
  `solutions/pool/<problem>/vNNNN/` version (monotonic; a per-problem `next_version`
  counter in `solutions/REGISTRY.json` plus a pool-dir scan), invokes the project's
  own `numerics/<problem>/solve.py` (which imports the shared methods), records
  metrics + `standards_methods_sha` in `meta.json`, and marks the task `done`,
  committing the solution + queue + registry back to the project repo (push with
  rebase-retry). `--local` performs claim/done as in-place queue edits with no
  git/REST — for safe dry-runs.

`runner/` stays the **framework**; the per-paper queue, params, pool, and the thin
`solve.py` live in the project repo. See `../methods/MAP.md` for the
source-of-truth/update protocol.

> **Deprecated:** `bootstrap.sh` (VM startup) still references the old `core/` and
> `projects/<P>/` monorepo layout and a `fixed-point-factory` clone URL. The active
> orchestration is GitHub Actions in the project repo (e.g. MIWN's
> `.github/workflows/solve.yml`). Revive/rewrite `bootstrap.sh` only if VM-based
> running is needed again.
