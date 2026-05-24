"""
progress.py — Worker progress reporter.
Solvers import this and call `update(iter=N, ftol=X)` periodically.
A background thread writes the latest state to
    projects/$PROJECT/progress/$TASK_ID.json
once per `interval` seconds, commits it, and pushes.

Usage from a solver:
    from core.progress import ProgressReporter
    reporter = ProgressReporter(
        project="REZN", task_id="g400_t1000", worker_id="solver-1",
        branch="main", interval=60,
    )
    reporter.start()
    for it in range(max_iter):
        ftol = compute_residual(...)
        reporter.update(iter=it, ftol=ftol)
        if ftol < target_tol:
            break
    reporter.stop()    # final flush + thread join
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional


def _utcnow_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    return Path(result.stdout.strip()) if result.returncode == 0 else Path(".")


class ProgressReporter:
    def __init__(
        self,
        project: str,
        task_id: str,
        worker_id: str,
        branch: str = "main",
        interval: int = 60,
        repo_root: Optional[Path] = None,
        progress_rel: Optional[str] = None,
    ):
        self.project = project
        self.task_id = task_id
        self.worker_id = worker_id
        self.branch = branch
        self.interval = interval
        self.repo_root = Path(repo_root) if repo_root else _repo_root()
        # Cross-repo: a project supplies its own progress dir (e.g. "todo/progress");
        # legacy monorepo default is projects/<project>/progress.
        self.progress_rel_dir = progress_rel or f"projects/{project}/progress"
        self.progress_dir = self.repo_root / self.progress_rel_dir
        self.progress_file = self.progress_dir / f"{task_id}.json"

        self._state: dict = {
            "task_id":      task_id,
            "worker_id":    worker_id,
            "started_at":   _utcnow_iso(),
            "last_update":  _utcnow_iso(),
            "iter":         None,
            "ftol":         None,
            "ftol_history": [],
            "extra":        {},
        }
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    # ── public API ────────────────────────────────────────────────────────────────────
    def update(self, iter: Optional[int] = None, ftol: Optional[float] = None,
               **extra) -> None:
        """Called by the solver inner loop. Cheap: just updates memory."""
        with self._lock:
            if iter is not None:
                self._state["iter"] = int(iter)
            if ftol is not None:
                ftol_str = str(ftol) if isinstance(ftol, str) else f"{float(ftol):.6e}"
                self._state["ftol"] = ftol_str
                hist = self._state["ftol_history"]
                if not hist or hist[-1] != ftol_str:
                    hist.append(ftol_str)
                    if len(hist) > 8:
                        hist.pop(0)
            if extra:
                self._state["extra"].update(extra)
            self._state["last_update"] = _utcnow_iso()

    def start(self) -> None:
        """Start the background flusher thread."""
        if self._thread is not None:
            return
        self.progress_dir.mkdir(parents=True, exist_ok=True)
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self, delete: bool = True) -> None:
        """Stop the flusher thread and write a final snapshot.

        The remote progress file is left in place (small; the dashboard only reads
        progress for currently-claimed tasks, so a leftover for a done task is
        ignored and is overwritten if the task runs again)."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=15)
            self._thread = None
        try:
            self._flush()
        except Exception:
            pass
        if delete:
            try:
                p = self.progress_file
                if p.exists():
                    p.unlink()
            except Exception:
                pass

    # ── internals ────────────────────────────────────────────────────────────────────
    def _loop(self) -> None:
        while not self._stop_event.is_set():
            self._flush()
            for _ in range(self.interval):
                if self._stop_event.is_set():
                    break
                time.sleep(1)
        # Final flush — always runs so the last state is written before stop()/delete()
        self._flush()

    def _flush(self) -> None:
        with self._lock:
            snapshot = dict(self._state)
        content = json.dumps(snapshot, indent=2)
        # Prefer REST (decoupled from the contended queue branch — its own file, no
        # local git, so it can't conflict with claim/done commits). Fall back to a
        # local file when there's no token/origin (e.g. --local dry-run).
        try:
            if not self._rest_put(content, snapshot):
                self.progress_dir.mkdir(parents=True, exist_ok=True)
                self.progress_file.write_text(content)
        except Exception as exc:
            print(f"[progress] flush failed (non-fatal): {exc}", flush=True)

    def _rest_put(self, content: str, snapshot: dict) -> bool:
        """PUT progress/<task>.json via the GitHub contents API. Returns False if
        REST isn't available (caller writes locally instead)."""
        try:
            from claim_task import _gh_token, _gh_repo, _api_get, _api_put  # noqa: PLC0415
        except Exception:
            return False
        token = _gh_token(); owner, repo = _gh_repo()
        if not token or not owner:
            return False
        path = f"{self.progress_rel_dir}/{self.task_id}.json"
        sha = None
        try:
            sha = _api_get(token, owner, repo, path, self.branch).get("sha")
        except Exception:
            sha = None
        _api_put(token, owner, repo, path,
                 f"progress {self.task_id} iter={snapshot.get('iter')} "
                 f"ftol={snapshot.get('ftol')} ({self.worker_id})",
                 content.encode(), sha, self.branch)
        return True
