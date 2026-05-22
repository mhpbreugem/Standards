# Standards-and-Methods

Central hub for the author's financial-economics papers: standards for **writing**
a paper, plus standardized **code** that individual projects pull so they share
structure, methods, and layout. `CLAUDE.md` is the full map; agents start there.

## What's here

- **`writing/`** — writing standards (Figures done; Tables, LaTeX, bibliography, prose, structure planned).
- **`methods/`** — shared, latest-version code; registry in `methods/MAP.md`.
- **`runner/`** — project-agnostic VM/worker coordination for distributed jobs.

## Conventions

- **Single source of truth.** Methods and runner live here; papers vendor or
  submodule them — they do not fork private copies. Fix bugs here, then pull.
- **Self-containment.** The repo aims to run with no dependency on other private
  repos. Current gap: `methods/solver/` still imports the REZN `code/` package —
  see the self-containment status in `methods/MAP.md`.
- **Change control.** All changes go through a PR the owner approves; never push
  to `main`. See `CLAUDE.md`.

> Repository rename pending (owner-only, Settings): broadening beyond `Writing`
> back toward this name as scope now spans writing + methods + runner.
