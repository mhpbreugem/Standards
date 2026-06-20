# Proofs

Standard for every proof in a paper, and the gate the **proof agent**
(`agents/fleet/proof.md`) must pass before an item is `done`. Proofs in this
project are part analytic, part numerical: a claim is only settled when the
argument is complete **and** the numerics corroborate it. Proof changes are always
human-gated (`agents/AUTONOMY.md`) — this chapter is what the researcher checks
when approving.

## Standard

- **Statements are exact and stable.** A theorem/lemma/proposition statement is not
  edited as a side effect of fixing its proof. Any change to a statement is
  surfaced as its own decision, never folded silently into a proof patch.
- **Every step is justified.** Each line follows from a stated definition,
  assumption, prior result, or elementary manipulation. No "clearly" / "it follows"
  carries an unproven leap.
- **Assumptions are tracked.** Every hypothesis the step uses is among the stated
  hypotheses; none is silently introduced (no hidden regularity, interiority, or
  sign assumption).
- **Quantitative claims are checked against the numerics.** A magnitude, sign, or
  limit asserted in prose (e.g. a `1−R²` value, a slope, the CARA knife-edge limit)
  is cross-checked against the relevant `solutions/pool/<problem>/vNNNN/` result,
  and the version is cited.
- **Discretization is not a proof gap.** A residual floor or a worst-cell artifact
  is labeled a *numerical* limitation, never presented as a theoretical hole — and
  vice versa. Say which it is.
- **Notation matches the manuscript.** Symbols, conventions, and signs agree with
  the LaTeX/notation chapter; no clashing local redefinitions.

## Pre-commit checklist

Run every box before marking a `proof` item done / approving the PR:

1. **Statement integrity** — the proved statement is verbatim the one in the paper
   (or the change is flagged as a separate `decision`).
2. **Assumptions** — every hypothesis used appears in the statement; none added.
3. **Step justification** — each step cites a definition / assumption / prior
   result, or is elementary; no gap hidden behind "obviously".
4. **Limit & edge cases** — boundary/limit regimes are handled explicitly (e.g.
   `γ → CARA`, extreme `τ`, degenerate price).
5. **Numerical corroboration** — quantitative claims match a named pool version
   `vNNNN`; the run is logged (manifest / `standards_methods_sha`).
6. **Artifact vs. gap** — any disagreement with the numerics is classified as a
   discretization artifact *or* a real gap, with the reason.
7. **Notation consistency** — symbols and signs agree with the manuscript; no
   clashing redefinition.
8. **Citations** — any invoked external result is cited (ties to `references/`).
9. **Reproducibility** — if the argument leans on a computation, anyone can rerun
   it from the cited version + config.

A failed box is a `needs-decision` (with the specific gap), never a silent rewrite.
