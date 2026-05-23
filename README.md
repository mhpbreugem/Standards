# Standards-and-Methods

Central, canonical hub for the author's financial-economics papers. It holds three
things, each a **single source of truth** that individual paper repos pull from
rather than copy:

1. **Writing standards** (`writing/`) — how every paper artifact (figures, tables,
   LaTeX, prose, …) must look.
2. **Methods** (`methods/`) — standardized, latest-version shared numerical code.
3. **Runner** (`runner/`) — project-agnostic VM/worker coordination for
   distributed compute jobs.

`CLAUDE.md` is the agent-facing map and the change-control policy; start there.

## Repository layout

```
Standards/
├── README.md            this file
├── CLAUDE.md            agent guide + change-control rules (read first)
├── CODEOWNERS           @mhpbreugem reviews all paths
├── .gitignore           python bytecode
│
├── writing/             PILLAR 1 — paper writing standards
│   ├── README.md        pillar index (chapter status table)
│   ├── figures/         Figures chapter (done)
│   │   ├── README.md            the standard + pre-commit checklist
│   │   ├── bc20-ecta.tex        shared pgfplots style (colours + curve styles)
│   │   ├── example_fig10_ecta.tex   worked example
│   │   └── paper.mplstyle       matplotlib preview style (quick looks only)
│   ├── tables/          Tables chapter (planned — stub)
│   ├── references/      References / bibliography chapter (planned — stub)
│   └── paper/           Paper-structure chapter (planned — stub)
│
├── methods/             PILLAR 2 — shared numerical code (source of truth)
│   ├── MAP.md           registry of every method (read first)
│   ├── README.md
│   ├── requirements.txt numpy, scipy, mpmath, numba
│   └── solver/          REE / fixed-point solvers
│       ├── solve.py             task wrapper (claim → solve → checkpoint)
│       ├── run_sweep.py         γ-sweep driver
│       ├── phi_mp.py            mpmath fixed-point map Φ (K=3)
│       ├── ode_sweep.py         Anderson / mp-Newton sweep
│       ├── ode_sweep_rk4.py     RK4 + GMRES sweep variant
│       ├── contour_KN_sym.py    symmetric (K,N) contour combinatorics
│       ├── test_rk4_quick.py    smoke tests
│       ├── test_sweep_quick.py
│       └── code/                vendored REZN numerical core (self-contained)
│
└── runner/              PILLAR 3 — VM + worker coordination
    ├── README.md
    ├── claim_task.py            git-race claim/done/bail locking
    ├── progress.py              live iter/ftol reporter
    ├── supervisor.py            status CLI
    ├── bootstrap.sh             VM startup → worker loop
    ├── create_gcp_vm.sh         GCP spot-VM provisioner
    ├── heartbeat.sh             liveness ping
    ├── TASK_SCHEMA.md           task lifecycle schema
    └── PROGRESS_FORMAT.md       progress-file schema
```

## The three pillars

### `writing/` — writing standards

Before producing any paper artifact, read the matching chapter and apply its
checklist.

| Chapter | Covers | Path | Status |
|---|---|---|---|
| Figures | pgfplots BC20→ECTA style, captions, legends, bounded axes, bar charts | `writing/figures/` | **done** |
| Tables | booktabs / Econometrica, generate-don't-type | `writing/tables/` | planned (stub) |
| References | citation style, `.bib` conventions | `writing/references/` | planned (stub) |
| Paper structure | manuscript repo layout, section order | `writing/paper/` | planned (stub) |
| LaTeX / notation | preamble, macros, symbol conventions | `writing/latex/` | planned |
| Prose style | financial-economics writing checklist | `writing/prose-style/` | planned |

The Figures chapter targets **Econometrica**: vector-PDF pgfplots, 8 cm square
axes (relaxed for wide bar charts), grayscale-safe curve styles, captions below,
no overlapping text with explicit clearance, bounded axes that stay inside their
bound, and bar-chart conventions. See `writing/figures/README.md`.

### `methods/` — shared code

The registry in **`methods/MAP.md`** lists every method — what it is, where it
lives, where it came from, and what it depends on. Read it first. Today the only
area is `methods/solver/`: rational-expectations-equilibrium / fixed-point
numerical methods used by the REZN paper — Anderson and RK4 parameter sweeps, an
mpmath fixed-point map, the symmetric-K contour machinery, and the vendored REZN
numerical core under `methods/solver/code/`. Import these; never fork a private
copy — fix bugs here and pull.

Dependencies are pip libraries only (`numpy`, `scipy`, `mpmath`, `numba`), pinned
in `methods/requirements.txt`.

### `runner/` — VM + worker coordination

A project-agnostic task-queue framework for distributed solver runs: claim/done/
bail with git-race locking (`claim_task.py`), GCP spot-VM bootstrap
(`bootstrap.sh`, `create_gcp_vm.sh`), heartbeats, live progress reporting
(`progress.py`), and a supervisor CLI. Lifecycle and file schemas are in
`TASK_SCHEMA.md` and `PROGRESS_FORMAT.md`; see `runner/README.md`.

## Conventions

- **Single source of truth.** Methods and runner live here; papers vendor or
  submodule them and never keep private edits — fix bugs here, then pull.
- **Self-contained.** The repo runs with no dependency on other private repos.
  The REZN numerical core is vendored under `methods/solver/code/` (from
  `mhpbreugem/REZN @ 7f03509`); nothing is cloned at runtime. Status is tracked
  in `methods/MAP.md`.
- **Reproducible.** Figure coordinates come from committed project scripts;
  solver outputs are checkpointed; results regenerate from source.
- **Change control.** Every change goes through a pull request the owner
  (@mhpbreugem) approves. **Never push to or merge `main`** — work on a feature
  branch; the owner merges. See `CLAUDE.md` and `CODEOWNERS`.

## Using this hub from a project repo

Add this pointer to the project's own `CLAUDE.md`:

> Shared standards/methods/runner live in `github.com/mhpbreugem/<repo>`.
> - **Writing:** before a figure/table/manuscript edit, consult `writing/` and apply the checklist.
> - **Methods:** import from `methods/` (single source of truth — see `MAP.md`); never keep private edits, back-port instead.
> - **Distributed runs:** wire this paper's queue/solver onto `runner/` per `runner/README.md`.
> Paper-specific math, task queues, and glue stay in the project repo.

## Consumers

| Paper | Uses |
|---|---|
| REZN — *Inefficient Markets Without Noise* | `writing/figures`, `methods/solver`, `runner` |
| _(add future papers here)_ | |

---

> **Repository rename pending** (owner-only, in Settings). It began as
> `Standards-and-Methods`, was briefly `Writing`; now that it again spans writing
> + methods + runner, a broader name fits (e.g. `research-hub` / `research-commons`).
> GitHub redirects old URLs, so links and clones keep working.
