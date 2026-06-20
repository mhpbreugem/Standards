# Research standards, methods & runner

Central, canonical hub for the author's financial-economics papers. Four things
live here, each a **single source of truth** that individual papers pull from:

1. **Writing standards** (`writing/`) — figures, tables, LaTeX, prose, bibliography, structure.
2. **Methods** (`methods/`) — standardized, latest-version shared code.
3. **Runner** (`runner/`) — VM/worker coordination for distributed jobs.
4. **Agents** (`agents/`) — the agentic research OS: one ledger, a background agent
   fleet, the dashboard, and the "use standards as a setup" bootstrap.

> Repository rename pending (owner-only, in Settings). It began as
> `Standards-and-Methods`, was briefly `Writing`; now that it again spans methods
> and runner, a broader name fits (e.g. `research-hub` / `research-commons` —
> owner to choose). GitHub redirects old URLs, so links and clones keep working.

## Change control — read first

This repository is owned by **@mhpbreugem**, who has granted the AI agent
**standing permission to commit directly to `main`**.

- **Work on `main`. Do not create side/feature branches.** Every change lands on
  `main` as a small, descriptive commit.
- **The owner's permission is the gate, and it is standing** — it covers routine
  changes to this hub. Keep commits small and reversible.
- **Surface, don't surprise.** Anything large, irreversible, or outside routine
  maintenance is flagged to the owner before it lands.
- `CODEOWNERS` records @mhpbreugem as owner of all paths.

## Repository map

### `writing/` — paper writing standards
Before producing a paper artifact, read the matching chapter and apply its checklist.

| Chapter | Covers | Path | Status |
|---|---|---|---|
| Figures | pgfplots BC20→ECTA style, captions | `writing/figures/` | done |
| Proofs | step-justification + numerical corroboration (proof-agent gate) | `writing/proofs/` | done |
| References | author–year, `natbib`, `.bib` conventions (literature-agent gate) | `writing/references/` | done |
| Tables | booktabs / Econometrica, generate-don't-type | `writing/tables/` | planned (stub) |
| Paper structure | manuscript repo layout, section order | `writing/paper/` | planned (stub) |
| LaTeX / notation | preamble, macros, symbol conventions | `writing/latex/` | planned |
| Prose style | financial-economics writing checklist | `writing/prose-style/` | planned |

### `methods/` — shared code (source of truth)
Registry in **`methods/MAP.md`** (read first). Currently `methods/solver/` — REE /
fixed-point numerical methods. Import these; do not fork private copies.

### `runner/` — VM + worker coordination
See **`runner/README.md`**. Project-agnostic task-queue framework: claim/done/bail
with git-race locking, GCP VM bootstrap, heartbeats, supervision.

### `agents/` — agentic research OS
See **`agents/README.md`**. A typed `research-ledger.json` (the single source of
truth), a fleet of background agents (`fleet/`) gated by the `writing/`/`methods/`
checklists, the dashboard prompt-pack (`dashboard/`), the tiered autonomy policy
(`AUTONOMY.md`), and the bootstrap that stands up a new project from
*"this is repo xyz, use standards as a setup"* (`BOOTSTRAP.md`). It is `runner/`
generalised: same cron-matrix + git-race locking, now for every workstream.

## Using this hub from a project repo

**Standing up a new project?** Follow **`NEW_PROJECT.md`** — it has the layout, the
steps, reference templates (`runner/templates/`), and the list of bugs already
fixed so a new project doesn't reproduce them.

Add this pointer to the project's own `CLAUDE.md`:

> Shared standards/methods/runner live in `github.com/mhpbreugem/<repo>`.
> - **Writing:** before a figure/table/manuscript edit, consult `writing/` and apply the checklist.
> - **Methods:** import from `methods/` (single source of truth — see `MAP.md`); never keep private edits, back-port instead.
> - **Precision:** every fixed point must follow `methods/PRECISION_POLICY.md` — double-double precision, accept only at `||F|| < 1e-20` (constants in `methods/solver/precision.py`).
> - **Distributed runs:** wire this paper's queue/solver onto `runner/` per `runner/README.md`.
> Paper-specific math, task queues, and glue stay in this project repo.
