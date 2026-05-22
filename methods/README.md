# Methods

Centralized, latest-version code shared across all papers. The catalog —
what each method is, where it came from, what it depends on, and which papers use
it — is in **`MAP.md`**. Start there.

## Layout

```
methods/
├── MAP.md       # the registry (read first)
└── solver/      # REE / fixed-point numerical methods (from REZN solver_code)
```

## Rules

- **One source of truth.** A method has exactly one home — here. Papers vendor or
  submodule it; they do not keep private edits. Fix bugs here and let papers pull.
- **Record provenance.** Every import notes its upstream repo + commit in `MAP.md`
  so "latest version" is auditable.
- **Flag external deps.** If a file imports code not vendored here (e.g. the REZN
  `code/` package), say so in `MAP.md` and track vendoring as a TODO — don't
  pretend it's drop-in.
- **Tests travel with methods.** Keep the smoke tests (`test_*.py`) alongside the
  code they exercise.
