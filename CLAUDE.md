# Writing — standards for financial-economics papers

Central, canonical standards for the **writing side** of a paper: figures,
tables, prose, LaTeX, bibliography, and paper structure. Coding methods are
out of scope and live in the individual project repos. This repository holds
documentation plus non-code templates only (no `.py` scripts).

> Repository is being renamed `Standards-and-Methods` -> `Writing` (owner-only
> step in GitHub Settings). GitHub redirects the old URL, so existing links and
> clones keep working.

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

## How to use these standards

Before producing any paper artifact, read the relevant chapter and apply its
checklist.

| Chapter | What it covers | Path |
|---|---|---|
| Figures | matplotlib style, formats, color, captions | `figures/` |
| Tables | booktabs format, significance, generate-don't-type | `tables/` (planned) |
| LaTeX / math / notation | preamble, macros, symbol conventions | `latex/` (planned) |
| Paper structure | manuscript repo layout, section order | `paper-structure/` (planned) |
| Bibliography | citation style, `.bib` conventions | `bibliography/` (planned) |
| Prose style | financial-economics writing checklist | `prose-style/` (planned) |

## Using these standards from a project repo

Add this pointer to the project's own `CLAUDE.md`:

> Quality standards for figures/tables/writing live in
> `github.com/mhpbreugem/Writing`. Before producing a figure, table, or
> manuscript text, consult the matching chapter there and apply its checklist.
> Generation code (matplotlib, pandas) stays in this project; the standards
> repo holds only the format and templates.
