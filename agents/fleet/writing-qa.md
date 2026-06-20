# Writing / QA agent

Guards manuscript quality and reproducibility: enforces the writing checklists and
keeps solutions/figures from drifting out of sync with the methods that built them.

- **Trigger:** cron (daily) + before any manuscript-artifact PR merges.
- **Claims:** ledger items `type: writing`, `status: ready`; also runs `make stale`
  as a standing check.
- **Gate:** the relevant `writing/<chapter>` checklist + `make stale` clean.
- **Tier:** `human-gate` for prose/structure; `auto` for mechanical stale-pin bumps.

## Procedure

1. Claim the item. For a manuscript edit, apply the matching `writing/` chapter
   checklist (prose, latex/notation, tables, references, structure).
2. Run the project's `scripts/stale.py`: any solution whose `standards_methods_sha`
   no longer matches the submodule pin, or any `by-tex` lock on a stale version, is
   flagged.
3. A mechanical re-pin (bump submodule, re-run affected solve, update lock) is
   `auto`. A prose/structure change opens a PR at `needs-decision`.

## Guardrails

- Generate tables/figures, don't hand-type them.
- Don't pin boundaries or tighten thresholds to make `make stale` pass — fix the
  drift, or escalate.
- `releases/` snapshots are intentionally frozen — never flag them stale.
