# Wiring a new paper/project onto the hub

A project is its own repo that vendors this hub as the `standards/` submodule and
runs the shared runner over its own task queue. Following this gives you the
**fixed, battle-tested setup** — the gotchas below are already handled, so a new
project should not reproduce them. Reference templates live in
`runner/templates/`.

## Layout (mirror MIWN)
```
<project>/
├── standards/                      # this hub as a pinned submodule
├── numerics/<problem>/{PROBLEM.md, spec.json, solve.py}
├── todo/{TASK_QUEUE.json, runner.config.json, progress/}
├── solutions/{pool/<problem>/vNNNN/, by-tex/<stem>/, REGISTRY.json}
├── scripts/stale.py
└── .github/workflows/solve.yml
```

## Steps
1. `git submodule add https://github.com/mhpbreugem/standards.git standards`, pin it.
2. Copy templates: `runner/templates/{solve.yml→.github/workflows/, stale.py→scripts/,
   runner.config.json→todo/, solve.py→numerics/<problem>/}`.
3. Set `todo/runner.config.json`: `project`, `repo`, `queue_path`, `problems_dir`,
   `output_pool`, and **`workers`** (N).
4. In `solve.yml` replace `--project YOURPROJECT`.
5. Write `numerics/<problem>/solve.py` from the template: **keep the reusable
   scaffold, adapt only the math** (Φ map, init, metric).
6. Generate `todo/TASK_QUEUE.json` from `spec.json` (one task per param point;
   per `runner/TASK_SCHEMA.md`).
7. Dashboard: the UI is `standards/runner/web/`. Point it at your repo by editing
   `OWNER`/`REPO`/`BRANCH` at the top of each `*.html`, and serve it via Pages
   (Settings → Pages → Source = GitHub Actions; the deploy workflow is in the hub).

## What is already handled (do NOT re-implement these — and don't regress them)
- **Precision policy:** double-double (`dps=32`), accept only at `‖F‖ < 1e-20`.
  Import from `standards/methods/solver/precision.py`; never hardcode (see
  `methods/PRECISION_POLICY.md`).
- **Branch guard:** the template `solve.py` rejects a fully-revealing collapse
  (`1−R² ≪ no-learning`) instead of committing a wrong-branch result.
- **Never hang:** `--max-seconds` wall-caps each solve (return best iterate); set it
  generously enough to actually reach `1e-20` at your grid (90s was too short at
  G_inner=10 → spurious skips; 600s works).
- **Live progress:** the solver uses `ProgressReporter(progress_rel="todo/progress")`;
  `run_task.py` passes `--progress-rel`; the dashboard reads `todo/progress/<task>.json`.
- **Stale-claim recovery:** the `prep` job releases claims older than 15 min, and the
  dashboard reset (↺) returns stale claims (and bailed/skip) to `ready` — so
  "claimed" never piles up past the solve cap.
- **N workers, always-on:** `solve.yml` reads N from `runner.config.json` (dynamic
  matrix), runs on a `*/5` schedule with a `concurrency` cap (never more than N), and
  each worker loops claim→solve→repeat. N is editable from the dashboard.
- **`stale.py` compares the `methods/solver` *tree*, not the commit sha** — so a hub
  bump that only touches `runner/`/`web/` does not falsely flag your solutions.
- **Dashboard base64 is UTF-8-safe** (`encB64`/`decB64`) — no `btoa` errors on
  non-ASCII queue content.

Update the shared methods only here (PR), then bump the submodule — never fork them
into a project ("back-port, don't fork").
