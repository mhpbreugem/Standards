# Figure agent

Regenerates figures from converged pool versions to the Standards figures
standard, and kills placeholders.

- **Trigger:** cron (hourly) + when a `compute` item it depends on turns `done`.
- **Claims:** ledger items `type: figure`, `status: ready`.
- **Gate:** `writing/figures` — pgfplots BC20→ECTA style, 8 cm axes, bounded axes,
  grayscale-safe, caption below, no placeholder background.
- **Tier:** `auto`.

## Procedure

1. Claim the item. Read the figure's `solutions/by-tex/<stem>/lock.json` to find the
   exact pool `vNNNN` it pins; load that data (never re-solve here).
2. Render via the project's committed figure script → `by-tex/<stem>/figures/*.pdf`.
3. Run the `writing/figures` checklist. If it passes, PR auto-merges on green CI and
   the item goes `done`.
4. If the figure still needs solver data that doesn't exist, open a `compute` item
   and set this one `blocked` on it.

## Guardrails

- Coordinates come from committed scripts — results must regenerate from source.
- Don't duplicate heavy pool data into `by-tex/`; copy only the small ready PDF.
- A stale pin (`make stale`) is a `bailed`, not a silent re-pin.
