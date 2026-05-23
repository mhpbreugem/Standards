# Writing standards

Standards for every artifact in a paper — figures, tables, notation, structure,
bibliography, and prose. Before producing an artifact, read the matching chapter
and apply its checklist. Papers follow these; they do not invent per-paper styles.

## Chapters

| Chapter | Covers | Path | Status |
|---|---|---|---|
| Figures | pgfplots BC20→ECTA style, captions, legends, bounded axes, log axes, contour bands, bar charts | `figures/` | **done** |
| Tables | booktabs / Econometrica, generate-don't-type | `tables/` | planned |
| LaTeX / notation | preamble, macros, symbol conventions | `latex/` | planned |
| Paper structure | manuscript repo layout, section order | `paper-structure/` | planned |
| Bibliography | citation style, `.bib` conventions | `bibliography/` | planned |
| Prose style | financial-economics writing checklist | `prose-style/` | planned |

## Rules

- **Read before you build.** Consult the relevant chapter's `README.md` and run
  its checklist before committing a figure / table / manuscript change.
- **One source of truth.** A standard has exactly one home — here. Papers follow
  it rather than keeping private variants; improve the standard here and let
  papers pull.
- **Generate, don't hand-type.** Figure coordinates and table bodies come from
  committed scripts in the paper repo, never typed by hand (see each chapter).
- **Econometrica target.** The current chapters are tuned for Econometrica; note
  any journal-specific deviation in the chapter itself.

Currently written: **`figures/`** — the BC20→ECTA pgfplots standard. The other
chapters are planned; the table above tracks status.
