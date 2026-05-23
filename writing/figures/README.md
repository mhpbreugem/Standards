# Figures

Standard for every figure in a paper, tuned for **Econometrica**. Figures are
drawn in **pgfplots**, compiled `standalone` to **vector PDF**, and included with
`\includegraphics`. The shared style lives in `bc20-ecta.tex`; a worked example
is `example_fig10_ecta.tex`. The code that produces the *coordinates* (from data)
lives in the project repo, not here.

A matplotlib preview style (`paper.mplstyle`) is provided for quick looks only —
the manuscript figure is always the pgfplots PDF.

## Pipeline

```latex
% preamble
\input{bc20-ecta.tex}        % loads pgfplots, colours, the bc20ecta style + curve styles

% a figure (standalone -> fig_knife_edge.pdf), included in the paper:
\begin{figure}[t]
  \centering
  \includegraphics[width=0.49\textwidth]{figures/fig_knife_edge.pdf}
  \caption{Revelation deficit $1-R^2$ versus signal precision $\tau$ for
           $\gamma\in\{0.5,1,4\}$; only CARA achieves full revelation.
           $K=3$, $W=1$, $G=15$.}
  \label{fig:knife-edge}
\end{figure}
```

Two-panel figures use `subfigure` at `0.49\textwidth` each, side by side.

## Standard

- **Format / size.** Vector **PDF** from `standalone` pgfplots; **8 cm square**
  axes (`width=8cm, height=8cm`); included at `0.49\textwidth`. Never let LaTeX
  rescale a raster.
- **Fonts.** Document serif (Computer Modern) — automatic with pgfplots; the
  figure text then matches the body exactly.
- **Curve styles (grayscale-safe).** Use the four named styles from
  `bc20-ecta.tex`, in order — each pairs a colour with a distinct dash so the
  figure reads in B&W:
  1. `bcone`  — green, solid, very thick
  2. `bctwo`  — red, dashed, very thick
  3. `bcthree`— blue, dotted, very thick
  4. `bccara` — black, dash-dotted, ultra thick (CARA / baseline at 0)
- **Interpolation.** **Linear, no `smooth`.** A Bézier through sparse points
  bows between data and rounds off real features. Only use `smooth` with ≥40
  dense points.
- **No in-axis `title=`.** Descriptive text goes in the LaTeX `\caption`, not
  inside the axes. Axes get `xlabel`/`ylabel` only.
- **No overlapping text.** No text element may overlap any other text or any
  graphical element. This covers legend entries, axis and tick labels, `\node`
  annotations, and data/value labels — none may sit on top of another piece of
  text, a curve, a bar, a marker, or the axis frame. Everything must be fully
  legible with clear separation. Fixes, in order of preference: move the element
  to an empty region; widen the axis range (for unbounded axes; see **Bounded
  quantities**) to open a clear band; for bar charts, put value labels above the
  bar (`nodes near coords`) and rotate or abbreviate crowded category ticks.
  **Never clip a curve or bar, and never shrink the data, to make room for text.**
  - **Minimum clearance.** Every text element must have at least one
    line-height of clear space between it and any curve, bar, marker,
    frame, or other text. Mathematical non-intersection is not enough:
    a label that lands within 1 mm of a curve at the figure's `0.49\textwidth`
    inclusion size is still a violation. Verify visually at the printed
    inclusion size, not at the standalone size.
  - **Zero-height bars.** In grouped bar charts, a bar with value
    exactly zero leaves its `nodes near coords` label sitting on the
    axis frame. Omit the bar (and its label) entirely rather than
    rendering a flat bar of height zero with a label on the frame. The
    absence of the bar carries the meaning. If the zero value is the
    punch line of the figure (e.g. a collapse at a knife-edge), say so
    in the caption.
  - **Widening recipe (when the y-axis is not bounded).** When the
    legend overlaps a curve and the y-axis is *not* a bounded quantity
    (see **Bounded quantities** below):
      1. First try moving the legend to a sparser corner.
      2. If still tight, widen the axis range by at least 25% above
         the data maximum (or below the minimum) so the legend sits in
         a clearly empty band.
      3. Never clip a curve, never shrink the data, and never overlap
         text.
- **Legend.** No frame and no fill (`draw=none, fill=none`) so it can never mask
  data; place it in the emptiest corner. Per the rule above, if it still overlaps
  any curve, bar, or label, widen the axis range (unbounded $y$ only — for bounded
  quantities relocate the legend instead; see **Bounded quantities**) rather than
  move the data. See `example_fig10_ecta.tex`, where `ymax` is lifted to `0.185`
  so the north-east legend clears the $\gamma=0.25$ curve (an unbounded axis).
- **Caption.** Below the float, self-contained: state the takeaway, define every
  symbol, and give the parameter values ($K$, $W$, $G$, $\tau$, $\gamma$).
- **Naming.** `fig_<name>.pdf` matching the float label `fig:<name>`; figures are
  Arabic-numbered (article/Econometrica convention) — reference via `\ref`.
- **Reproducible.** Coordinates come from a committed project script, never typed
  by hand; the figure is never hand-edited after generation.
- **Colour names.** The palette uses namespaced names (`bcgreen`, `bcred`,
  `bcblue`) so it never redefines the standard `red`/`green`/`blue`.

### Bounded quantities

If the y-axis represents a probability, a CDF, a percentage, or any
other quantity bounded by `[0, 1]` (or by `[0, 100]` for percentages),
the axis range must stay inside that bound. Do not inflate `ymax`
above 1 (or above 100) to open headroom for a legend.

If the legend overlaps a curve, find space inside the data window:

1. Move the legend to the corner of the plot farthest from the curves'
   main body. For monotone-increasing curves from `(x_min, 0)` to
   `(x_max, 1)`, the bottom-right or top-left corner is usually empty
   enough.
2. If no corner has enough empty space, move the legend outside the
   axis (above the plot via `legend pos=outer north east` or similar,
   or below the caption-side via `legend to name` and `\ref`).
3. Only as a last resort, shrink the legend by abbreviating entries
   (e.g. "Full revelation" → "FR", "Newton--Krylov polish" →
   "Newton--Krylov") or by splitting the figure into two panels.

The same rule applies to any other quantity with a fixed natural
ceiling: shares of a population, probabilities, fractions of variance
explained ($R^2$, $1 - R^2$), and so on. The ceiling is honest; the
headroom is the legend's problem, not the data's.

## Econometrica note

The manuscript currently compiles as `article` ("Target: Econometrica"). Moving
to the official `econsocart` class adds the house caption ("FIGURE n —", small
caps, below) and Roman *table* numbers automatically; the figures above already
conform.

## Checklist (before committing a figure)

- [ ] Vector PDF from pgfplots, 8 cm square, document serif fonts
- [ ] Curves use the four ordered styles; legible in grayscale
- [ ] Linear interpolation (no `smooth` unless dense)
- [ ] No in-axis title; `xlabel`/`ylabel` only
- [ ] **No text overlaps** any other text, curve, bar, marker, or frame (range widened if needed)
- [ ] Legend `draw=none, fill=none`, placed in the emptiest corner
- [ ] Caption below, self-contained, parameters stated
- [ ] Coordinates generated by a committed script (reproducible)
- [ ] Filename `fig_<name>.pdf` matches `\label{fig:<name>}`
