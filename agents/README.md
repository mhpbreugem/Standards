# `agents/` — agentic research OS (PILLAR 4, design stage)

A fourth pillar alongside `writing/`, `methods/`, and `runner/`. Where the runner
coordinates **compute jobs**, this pillar coordinates **research work of every
kind** — proofs, literature, figures, writing, decisions — and routes each item to
a specialised background AI agent. The researcher gives a few prompts a day in one
chat (the *dashboard*); the fleet does the rest.

> **Status: design / proposal.** This folder currently holds the design only
> (`DESIGN.md`, `BOOTSTRAP.md`, and `design/`). No agent runs yet. The build order
> is in `DESIGN.md`; nothing here changes `methods/`, `runner/`, or `writing/`.

## The idea in one paragraph

One git-backed **`research-ledger.json`** is the single source of truth. It holds
typed items — `proof · compute · figure · literature · writing · decision` — each
with a `status`, the Standards `gate` it must pass before it can be marked done,
and its dependencies. A fleet of background agents (one per type) reads items of
its type, does the work, and opens a PR. **This chat is the dashboard:** it reads
the ledger plus open PRs and reports what's done / running / blocked, asking the
researcher only when an item needs a decision.

`agents/` is deliberately **`runner/` generalised** — the same `*/5` cron-matrix
workflow and the same claim/done/bail git-race locking, extended from compute-only
tasks to typed research items. That keeps the build small and rides proven code.

## Contents

| File | What |
|---|---|
| `DESIGN.md` | The full proposal: ledger schema, the fleet, tiered autonomy, liveness, rollout. |
| `BOOTSTRAP.md` | The target UX — *"this is repo xyz, use standards as a setup"* — and the steps an agent runs to deliver it. |
| `design/` | The overview figures (`*.pdf`) and the scripts that regenerate them (`make_*.py`). |

## Quality gates (where they live)

Agents may only mark an item `done` after passing the matching Standards
checklist. The gates are not new code here — they live in their home pillars:

| Workstream | Gate | Home |
|---|---|---|
| compute | `‖F‖ < 1e-20` + branch guard | `methods/PRECISION_POLICY.md`, `methods/solver/precision.py` |
| figure | figures checklist | `writing/figures/` (done) |
| literature | citation / references policy | `writing/references/` (**to write**) |
| proof | proof-audit checklist | `writing/proofs/` (**to write**) |
| writing | prose / latex checklists + `make stale` | `writing/`, project `scripts/stale.py` |

## Regenerating the figures

```
cd design && pip install matplotlib && python make_summary.py && python make_overview.py
```

Figures regenerate from committed source, per the hub convention.
