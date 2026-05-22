# Methods map

Central registry of standardized code shared across papers. **This repo is the
single source of truth**: changes land here first, and papers vendor or submodule
these methods rather than keeping private copies. Each entry records what the
method is, where it lives here, where it came from, and what it still depends on.

## solver/ — REE / fixed-point numerical methods

| File | Purpose | Self-contained? | Deps |
|------|---------|-----------------|------|
| `phi_mp.py` | mpmath fixed-point map Φ (K=3): `phi_K3_smooth_mp`, `f_inf_mp`, `np_to_mp` | yes | mpmath |
| `ode_sweep.py` | Anderson / mp-Newton solvers: `solve_sweep`, `anderson_solve`, `mp_newton_solve` | yes | numpy |
| `ode_sweep_rk4.py` | RK4 + GMRES variant | yes | numpy, scipy |
| `contour_KN_sym.py` | symmetric (K,N) contour combinatorics | yes | numpy |
| `solve.py` | REZN task wrapper (claim → solve → checkpoint) | **no — project glue** | external REZN `code/` |
| `run_sweep.py` | sweep driver | **no — project glue** | `code.contour_K3_halo`, `code.metrics` (REZN repo) |
| `test_rk4_quick.py`, `test_sweep_quick.py` | smoke tests | yes | — |

## Self-containment status

The repo is **not yet self-contained**: `solve.py` and `run_sweep.py` import a
REZN `code/` package and auto-clone `github.com/mhpbreugem/REZN` at runtime. The
missing modules are:

| Import | Provides |
|--------|----------|
| `code.contour_K3_halo` | `init_no_learning_K3`, `phi_K3_halo_smooth` |
| `code.halo` | `extract_inner`, `replace_inner` |
| `code.staggered` | `staggered_solve` |
| `code.f128` | `revelation_deficit_f128` |
| `code.metrics` | `revelation_deficit` |

To finish self-containment (blocked — needs access to `mhpbreugem/REZN`):
1. Vendor those modules (and their transitive deps) under `methods/solver/code/`.
2. Delete the runtime `git clone` blocks in `solve.py` / `run_sweep.py`.
3. Rewire imports: `progress` now lives in `runner/` (was `core/`); `code.*`
   resolves to the vendored `methods/solver/code/`.

Self-contained today (deps are pip libraries only, pinned in `requirements.txt`):
`phi_mp.py`, `ode_sweep.py`, `ode_sweep_rk4.py`, `contour_KN_sym.py`.

## Source of truth & versions

- Imported from `mhpbreugem/fixed-point-factory` @ `4875059`
  (branch `claude/organize-quality-standards-GzEaW`) on 2026-05-22:
  - `methods/solver/`  ← `projects/REZN/solver_code/`
  - `runner/`          ← `core/`  (see `runner/README.md`)
- **Update protocol:** edit here first; bump the commit/date above; then papers
  pull. Never fork a private copy in a paper repo without back-porting here.

## Used by

| Paper | Methods | Runner |
|-------|---------|--------|
| REZN — *Inefficient Markets Without Noise* | `solver/` | yes |
| _(add future papers here)_ | | |
