# Bootstrap — "use standards as a setup"

The target experience for starting a new paper. The researcher says, in one chat:

> **"This is the project repo `xyz`. Use standards as a setup."**

…and a bootstrap agent stands up the whole machinery — submodule, runner, agent
fleet, ledger, dashboard — so the project is ready to run with no further wiring.
This automates `NEW_PROJECT.md` (today a manual checklist) end to end.

## What the bootstrap agent does

Given a target repo `xyz`:

1. **Vendor the hub.** `git submodule add https://github.com/mhpbreugem/standards.git standards`, pin it.
2. **Lay down the layout** (mirrors MIWN):
   ```
   xyz/
     standards/                      # this hub, pinned
     numerics/<problem>/{PROBLEM.md, spec.json, solve.py}
     todo/{TASK_QUEUE.json, research-ledger.json, runner.config.json, agents.config.json, progress/}
     solutions/{pool/<problem>/vNNNN/, by-tex/<stem>/, REGISTRY.json}
     scripts/stale.py
     .github/workflows/{solve.yml, agents.yml}
   ```
3. **Copy templates** from `standards/runner/templates/` and `standards/agents/templates/`.
4. **Fill the configs** — `runner.config.json` (project, repo, queue_path, workers)
   and `agents.config.json` (per-type cadence · model tier · autonomy).
5. **Seed the ledger** from `numerics/<problem>/spec.json` — one item per task,
   typed per `agents/LEDGER_SCHEMA.md`.
6. **Add the CLAUDE.md pointer** to the hub (the block in the root `CLAUDE.md`),
   so every future session in `xyz` knows the rules.
7. **Wire the dashboard** — point `standards/runner/web/` at `xyz` and enable Pages.
8. **Enable the workflows** — `solve.yml` (compute) and `agents.yml` (fleet), both
   on the `*/5` schedule. From this point the project is self-driving.

The researcher then returns to the single dashboard chat and gives a few prompts a
day; the fleet runs in the background per `DESIGN.md`.

## Guardrails the bootstrap inherits (don't regress)

These are already solved in `NEW_PROJECT.md` and must carry over unchanged:

- **Precision policy** — import from `methods/solver/precision.py`; accept only at `‖F‖ < 1e-20`. Never hardcode.
- **Branch guard** — reject a fully-revealing collapse instead of committing a wrong-branch result.
- **Never hang** — `--max-seconds` wall-caps each solve and returns the best iterate.
- **Stale-claim recovery** — claims older than 15 min return to `ready`; "claimed" never piles up.
- **Back-port, don't fork** — shared code changes go to this hub by PR, then bump the submodule pin.

## Status

Design only. The bootstrap agent is **Phase 1's headline deliverable** once the
ledger schema, autonomy policy, and templates land (see `DESIGN.md` rollout).
Until then, stand up a project by hand via `../NEW_PROJECT.md`.
