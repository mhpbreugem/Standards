# Proof agent

Step-checks the paper's proofs, finds gaps, and drafts corrections — cross-checked
against the numerics so analysis and computation stay consistent.

- **Trigger:** cron (daily) + when a proof source or a depended-on `compute` item
  changes.
- **Claims:** ledger items `type: proof`, `status: ready`.
- **Gate:** `writing/proofs` *(to write)* — every step justified, assumptions
  tracked, no leap unaccounted; numerics corroborate the analytic claim.
- **Tier:** `human-gate` (proofs are high-stakes).

## Procedure

1. Claim the item. Parse the proof in the manuscript / proof source.
2. Walk it step by step; record each gap or unjustified jump.
3. Where a claim is numerical (e.g. a 1−R² magnitude, a knife-edge), check it
   against the relevant `solutions/pool/<problem>/vNNNN/` result.
4. Draft a correction or an annotation, open a PR, set the item `needs-decision`
   with a tight summary of the gap and the proposed fix.

## Guardrails

- Never silently rewrite a theorem statement — surface it.
- A discretization artifact is not a proof gap; say which it is.
- The researcher approves every proof change (no auto-merge).
