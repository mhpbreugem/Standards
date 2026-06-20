# Agentic Research OS — design

> Proposal for `agents/`, the fourth Standards pillar. See `README.md` for the
> one-paragraph version and `design/agentic_research_os_summary.pdf` for the
> single-figure summary.

## Why

A research paper is more than compute. The `runner/` already automates the
distributed solve loop well — N always-on workers, git-race locking, stale-claim
recovery, a web dashboard. But proofs, literature, figures, and manuscript work
are still hand-driven, one chat session at a time, with all the per-session ritual
that lives in the older project repos. The goal: the researcher gives **a few
prompts a day in one chat**, and a fleet of background agents keeps every
workstream moving, at the quality the Standards checklists define.

## Principles

- **One ledger, all workstreams.** Generalise the runner's compute-only
  `TASK_QUEUE.json` into a typed `research-ledger.json`. Git is the message bus —
  auditable and conflict-safe, exactly the pattern the runner already uses.
- **`agents/` is `runner/` generalised.** Same cron-matrix workflow, same
  claim/done/bail locking; tasks just become *typed* and route to a prompt-pack.
- **Gates live in their home pillar.** An agent marks an item `done` only after
  passing the matching `writing/` or `methods/` checklist. No gate logic is
  duplicated here.
- **Tiered autonomy.** Low-risk work auto-merges on green CI; high-stakes work
  waits for the researcher. Standards `main` is always owner-merge-only.
- **Sessions are disposable, the ledger is permanent.** An agent that wakes up
  reads the ledger and resumes; nothing lives in the session.

## The ledger (sketch)

`todo/research-ledger.json` — one array of items; extends `runner/TASK_SCHEMA.md`.

```jsonc
{
  "id": "proof-lemma3-gap",
  "type": "proof",            // proof | compute | figure | literature | writing | decision
  "status": "ready",          // ready | claimed | done | bailed | needs-decision
  "gate": "writing/proofs",   // the checklist that must pass before done
  "depends_on": ["compute-g0.25-tau2"],
  "owner": null,              // agent/worker id once claimed
  "claimed_at": null,
  "artifact": null,           // path/PR the agent produced
  "autonomy": "human-gate"    // inherited from agents.config.json by type
}
```

## The fleet

Each agent is a scheduled Claude Code session with a tight contract: **input =
ledger items of its type → output = a PR + a ledger update + one digest line.**

| Agent | Does | Gate | Default tier |
|---|---|---|---|
| **Compute** | Triage bailed tasks, pick retry strategy, requeue, extract figures (absorbs the old `rerun_*.py` / `reset_and_extract.py` scripts) | precision + branch guard | auto |
| **Figure** | Regenerate figures from converged pool versions; kill placeholders | `writing/figures` | auto |
| **Literature** | Web-search new / competing / citable work; verify citations; flag known/contradicted claims | `writing/references` | auto (notes) |
| **Proof** | Step-check proofs, find gaps, cross-check against numerics, draft corrections | `writing/proofs` | human-gate |
| **Writing / QA** | Run `make stale`; enforce prose/latex checklists before manuscript edits | `writing/*` | human-gate |

## The dashboard = this chat

The control-room session owns no work. On each prompt (or a scheduled morning
digest) it reads the ledger + open PRs and reports done / running / blocked,
surfacing **only** items in `needs-decision` via a short multiple-choice, then
writes the answer back into the ledger (which wakes the right agent).

## Tiered autonomy

| Auto-merge on green CI | Researcher approves (one click) |
|---|---|
| figures, compute requeues/extraction, literature notes, stale-pin bumps | proof corrections, manuscript prose/structure, method changes, **anything touching `methods/` or Standards `main`** |

## Liveness — agents never sleep

Containers are ephemeral; agents are resumable and externally woken.

1. **Cron heartbeat.** A `*/5` GitHub Actions schedule (per-type cadence in
   `agents.config.json`) wakes each agent — a dead container just means the next
   tick spins up a fresh one. (Identical to `runner/templates/solve.yml`.)
2. **Event wake-ups.** PR comments, CI results, and pushes wake the relevant agent
   instantly via webhook subscriptions.
3. **Self-check-ins.** For "come back in an hour and re-verify", an agent re-arms a
   timer before its container dies.

Nothing is lost because **all state is in the ledger**; stale claims auto-release
after 15 min (as the runner already does) and the item is re-picked.

## Where it lives & how a project consumes it

The pillar ships templates that a project copies, exactly like the runner today
(see `NEW_PROJECT.md`):

```
agents/
  LEDGER_SCHEMA.md          typed items (extends runner/TASK_SCHEMA.md)
  AUTONOMY.md               the tiered merge policy
  dashboard/DASHBOARD.md    prompt-pack for the control-room chat
  fleet/{compute,figure,literature,proof,writing-qa}.md   per-type prompt-packs
  templates/
    agents.config.json      per-type cadence · model tier · autonomy
    agents.yml              cron workflow (clone of solve.yml, dispatches by type)
    research-ledger.json    seed
```

A project already vendors `standards/` as a submodule, so opting in is one added
`NEW_PROJECT.md` step: copy the templates, fill in `todo/agents.config.json`.
Improvements flow back here by PR — never forked ("back-port, don't fork").

## Rollout (each phase small, ships value)

1. **Scaffold the pillar** — `LEDGER_SCHEMA.md`, `AUTONOMY.md`, `dashboard/`. No behaviour.
2. **Compute agent** — absorbs the manual rerun scripts onto the existing runner; proves the ledger → gate → tiered-merge loop end to end.
3. **Figure agent** — its gate (`writing/figures`) is already done.
4. **Gates written** (`writing/proofs`, `writing/references`) ✓ — then wire the **literature + proof agents**.
5. **Writing/QA agent** + promote the dashboard to a scheduled morning digest.
6. **Consolidate** — migrate REZN's proofs/manuscript into MIWN, the canonical project repo.

## Consolidation target

**MIWN is the single live project repo.** REZN (theory/proofs/paper), MIZN (solver
rebuild), and FIXED-POINT-FACTORY (compute) all refer to the same project and are
**archived** — frozen, read-only history. Their content folds into MIWN: REZN's
proofs/manuscript and MIZN's strict-h=0 operator move into MIWN (the operator
back-ports to `methods/`), and the compute farm is already generalised in
`runner/`. The structure figure is `design/miwn_structure.pdf`.
