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
| `supervisor.py` | Local monitoring: VM health, stale claims, queue status |
| `heartbeat.sh` | Worker liveness: write a timestamp every 5 min and push |
| `progress.py` | Structured progress reporting (see `PROGRESS_FORMAT.md`) |
| `TASK_SCHEMA.md` | JSON schema + lifecycle rules for `TASK_QUEUE.json` |
| `PROGRESS_FORMAT.md` | Progress-record format |
| `SOLVER_INSTRUCTIONS.md` | Generic worker protocol (claim → solve → done) |

## Deployment contract (read before reusing)

These scripts assume the **consuming project** provides:

- a repo with `projects/<name>/TASK_QUEUE.json` — `claim_task.py` and
  `supervisor.py` resolve queues via `repo_root()/projects/<name>/...`;
- a project-specific solver invoked by the worker loop (e.g. `methods/solver/`);
- per-project checkpoints/progress directories.

So `runner/` is the **framework**; the per-paper queue, solver wiring, and any
project-specific maintenance scripts (e.g. REZN's `rerun_*`, `compute_ferr`) stay
in that paper's repo. Wiring a new paper onto this runner is the integration step
— see `MAP.md` for the source-of-truth/update protocol.
