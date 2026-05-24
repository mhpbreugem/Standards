# Research standards, methods & runner

Central, canonical hub for the author's financial-economics papers. Three things
live here, each a **single source of truth** that individual papers pull from:

1. **Writing standards** (`writing/`) — figures, tables, LaTeX, prose, bibliography, structure.
2. **Methods** (`methods/`) — standardized, latest-version shared code.
3. **Runner** (`runner/`) — VM/worker coordination for distributed jobs.

> Repository rename pending (owner-only, in Settings). It began as
> `Standards-and-Methods`, was briefly `Writing`; now that it again spans methods
> and runner, a broader name fits (e.g. `research-hub` / `research-commons` —
> owner to choose). GitHub redirects old URLs, so links and clones keep working.

## Change control — read first

Every change to this repository requires the owner's approval.

- The owner is **@mhpbreugem**. Their GitHub login (password + 2FA) is the
  approval gate.
- **Never push to or merge `main`.** Do all work on a feature branch and open a
  pull request for the owner to review and merge.
- **Do not merge a PR yourself**, even if you have the ability — wait for the
  owner to merge.
- `CODEOWNERS` assigns @mhpbreugem as reviewer of all paths. Server-side
  enforcement is branch protection on `main` (owner enables: Settings ->
  Branches -> Require a pull request before merging).

## Repository map

### `writing/` — paper writing standards
Before producing a paper artifact, read the matching chapter and apply its checklist.

| Chapter | Covers | Path | Status |
|---|---|---|---|
| Figures | pgfplots BC20→ECTA style, captions | `writing/figures/` | done |
| Tables | booktabs / Econometrica, generate-don't-type | `writing/tables/` | planned (stub) |
| References | citation style, `.bib` conventions | `writing/references/` | planned (stub) |
| Paper structure | manuscript repo layout, section order | `writing/paper/` | planned (stub) |
| LaTeX / notation | preamble, macros, symbol conventions | `writing/latex/` | planned |
| Prose style | financial-economics writing checklist | `writing/prose-style/` | planned |

### `methods/` — shared code (source of truth)
Registry in **`methods/MAP.md`** (read first). Currently `methods/solver/` — REE /
fixed-point numerical methods. Import these; do not fork private copies.

### `runner/` — VM + worker coordination
See **`runner/README.md`**. Project-agnostic task-queue framework: claim/done/bail
with git-race locking, GCP VM bootstrap, heartbeats, supervision.

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
