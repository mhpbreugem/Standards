# Autonomy policy

How much a background agent may do without the researcher. Tiered by workstream,
enforced through the ledger and the project repo's branch protection — never on
Standards `main`, where the owner's standing permission is the only path in.

## Tiers

| Tier | What the agent may do | Applies to (default) |
|---|---|---|
| **auto** | open a PR and **merge it on green CI** once the gate passes; update the ledger; post one digest line | figure, compute (requeue/extract), literature notes, stale-pin bumps |
| **human-gate** | open a PR and set the item to `needs-decision`; **wait for the researcher** to approve from the dashboard | proof corrections, manuscript prose/structure, method changes |

Defaults live in `agents.config.json` (`agents.<type>.autonomy`) and may be
overridden per item via the ledger `autonomy` field.

## Hard escalations (always human-gate, ignore the default)

An item is forced to `human-gate` if it:

- touches `methods/` or any shared Standards code (a method change is a back-port
  PR to Standards the **owner** merges — see `methods/PRECISION_POLICY.md`);
- edits manuscript prose, claims, or proof statements;
- would delete or overwrite an immutable artifact (a solution `vNNNN`, a release);
- trips a gate's red line — e.g. the compute **branch guard** (a fully-revealing
  collapse) — which is a `bailed`, never an auto-merge.

## How "auto-merge on green CI" works

On a project repo only:

1. agent pushes a branch and opens a PR for the item;
2. CI runs the item's gate (figures checklist / `make stale` / precision check);
3. if green **and** the item's tier is `auto`, the workflow merges and sets the
   ledger item `done` with the PR url in `artifact`;
4. if red, the item goes `bailed` (compute) or `needs-decision` (everything else).

Standards `main` is out of scope for auto-merge: shared-code PRs always wait for
the owner, by policy.

## What the researcher sees

Only `needs-decision` items reach the dashboard. Everything `auto` flows past as a
single digest line ("merged fig5 regen, ‖F‖ ok"). The point of the tiers is that a
normal day is a short list of *decisions*, not a queue of approvals.
