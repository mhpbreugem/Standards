# Compute agent

Absorbs the manual rerun/extract scripts (`rerun_highF.py`, `rerun_suspects.py`,
`reset_and_extract.py`) into a self-driving loop on top of `runner/`.

- **Trigger:** cron `*/5` (heartbeat) + push/CI events.
- **Claims:** ledger items `type: compute`, `status: ready` (this is a runner task).
- **Gate:** `methods/precision` — accept only at `‖F‖ < 1e-20`; the **branch guard**
  (fully-revealing collapse) is a hard fail.
- **Tier:** `auto`.

## Procedure

1. Claim via `runner/claim_task.py` (git-race). Solve through `methods/solver` with
   the project's `numerics/<problem>/solve.py`, `--max-seconds` wall-capped.
2. On convergence + gate pass → write the immutable `solutions/pool/<problem>/vNNNN/`,
   set `result {F_max, oneR2, slope}`, status `done`, PR auto-merges on green CI.
3. On non-convergence or gate fail → status `bailed` and apply one requeue strategy
   (warm-start from `depends_on` checkpoint → larger `G` → perturb IC), then `ready`.
   Never raise precision to beat a discretization floor; never pin boundaries.
4. For figure-extraction items, emit the derived quantities and hand off a `figure`
   item to the Figure agent.

## Guardrails

- Stale claims auto-release after 15 min — don't double-claim.
- One claim per worker; commit results atomically.
- A wrong-branch result is worse than no result — bail, don't commit it.
