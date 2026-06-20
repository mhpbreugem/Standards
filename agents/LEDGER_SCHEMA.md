# Ledger schema

`todo/research-ledger.json` is the single source of truth for a project's research
work. It is a strict superset of the runner's compute queue
(`runner/TASK_SCHEMA.md`): a `compute` item **is** a runner task, so the existing
git-race claim/done/bail machinery (`runner/claim_task.py`) drives the ledger
unchanged — only the set of types is wider.

## Shape

```jsonc
{
  "version": 1,
  "project": "MIWN",
  "items": [ /* Item objects */ ]
}
```

## Item

| field | type | meaning |
|---|---|---|
| `id` | string | stable unique slug, e.g. `proof-lemma3-gap` |
| `type` | enum | `proof · compute · figure · literature · writing · decision` |
| `title` | string | one line a human reads in the dashboard |
| `status` | enum | `ready · claimed · done · bailed · blocked · needs-decision` |
| `gate` | string | the Standards checklist that must pass before `done` (see below) |
| `autonomy` | enum | `auto · human-gate` — defaults from `agents.config.json` by type, may be overridden per item |
| `depends_on` | string[] | ids that must be satisfied first |
| `deps_satisfy` | enum | `all · any` (default `all`) |
| `owner` | string\|null | worker/agent id once claimed |
| `claimed_at` | iso8601\|null | for stale-claim recovery (15 min) |
| `completed_at` | iso8601\|null | |
| `artifact` | string\|null | path or PR url the agent produced |
| `result` | object\|null | type-specific metrics (e.g. compute: `{F_max, oneR2, slope}`) |
| `notes` | string | free text; the agent's last digest line |

## Status lifecycle

```
ready ──claim(git-race)──▶ claimed ──pass gate──▶ done
  ▲                          │  │
  │      stale >15min        │  └──fail/uncertain──▶ bailed ──requeue──▶ ready
  └──────────────────────────┘
blocked ──deps satisfied──▶ ready
claimed ──needs human──▶ needs-decision ──dashboard answer──▶ ready
```

- **Claiming is atomic** via `runner/claim_task.py` (edit status + push; losers detect
  the race). An agent only ever works a claim it won.
- **`bailed` never blocks** — a requeue strategy (per fleet pack) returns it to `ready`.
- **`needs-decision`** is the only state that pulls in the researcher; the dashboard
  surfaces it and writes the answer back, which returns the item to `ready`.

## Gates

`gate` names a checklist that lives in its home pillar — the agent cannot mark an
item `done` until it passes:

| type | `gate` value | home |
|---|---|---|
| compute | `methods/precision` | `methods/PRECISION_POLICY.md`, `solver/precision.py` (`‖F‖<1e-20` + branch guard) |
| figure | `writing/figures` | `writing/figures/` |
| literature | `writing/references` | `writing/references/` |
| proof | `writing/proofs` | `writing/proofs/` |
| writing | `writing/<chapter>` + `make stale` | `writing/`, project `scripts/stale.py` |
| decision | — | resolved by the researcher, no gate |

## Relation to the compute queue

A project may keep its existing `todo/TASK_QUEUE.json` for compute and have the
ledger reference those ids, or fold compute items inline. Either way the ledger is
what the dashboard reads; the runner only ever sees the `compute` subset.
