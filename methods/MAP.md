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
| `code/` | vendored REZN numerical core (`contour_K3_halo`, `halo`, `staggered`, `f128`, `metrics`, + transitive deps) | yes (vendored) | numpy, scipy, numba |
| `solve.py` | REZN task wrapper (claim → solve → checkpoint) | yes | vendored `code/`, `runner/progress` |
| `run_sweep.py` | sweep driver | yes | vendored `code/`, `phi_mp`, `ode_sweep` |
| `test_rk4_quick.py`, `test_sweep_quick.py` | smoke tests | yes | vendored `code/` (+ a paper anchor `.npz` via `REZN_CKPT_DIR` to run end-to-end) |

## Self-containment status

The repo is **self-contained**. The REZN numerical core is vendored under
`methods/solver/code/` (whole package — it uses relative imports, so it is
vendored as a unit), and nothing is cloned at runtime. All dependencies are pip
libraries pinned in `requirements.txt` (`numpy`, `scipy`, `mpmath`, `numba`).

The modules that used to be imported from the external REZN repo now resolve to
the vendored package:

| Import | Provides | Resolves to |
|--------|----------|-------------|
| `code.contour_K3_halo` | `init_no_learning_K3`, `phi_K3_halo_smooth` | `methods/solver/code/` |
| `code.halo` | `extract_inner`, `replace_inner` | `methods/solver/code/` |
| `code.staggered` | `staggered_solve` | `methods/solver/code/` |
| `code.f128` | `revelation_deficit_f128` | `methods/solver/code/` |
| `code.metrics` | `revelation_deficit` | `methods/solver/code/` |

What changed to finish self-containment:
1. Vendored the entire REZN `code/` package (with transitive deps) under
   `methods/solver/code/`.
2. Deleted the runtime `git clone` / `REZN_SRC` blocks in `solve.py`,
   `run_sweep.py`, and the two smoke tests.
3. Rewired imports: `code.*` resolves to the vendored package (the script's own
   directory is on `sys.path`); `progress` resolves from `runner/` (was `core/`),
   with `ROOT = parents[2]` for the `methods/solver/` layout.

To refresh the vendored core, re-copy `code/` from REZN and bump the commit
recorded under "Source of truth & versions"; do not hand-edit vendored files.

## Source of truth & versions

- Imported from `mhpbreugem/fixed-point-factory` @ `4875059`
  (branch `claude/organize-quality-standards-GzEaW`) on 2026-05-22:
  - `methods/solver/`  ← `projects/REZN/solver_code/`
  - `runner/`          ← `core/`  (see `runner/README.md`)
- `methods/solver/code/` vendored from `mhpbreugem/REZN` @ `7f03509`
  (2026-05-06) on 2026-05-22: the numerical core (`contour_K3_halo`, `halo`,
  `staggered`, `f128`, `metrics`, + transitive deps). Whole package copied
  verbatim; do not hand-edit.
- **Update protocol:** edit here first; bump the commit/date above; then papers
  pull. Never fork a private copy in a paper repo without back-porting here.

## Used by

| Paper | Methods | Runner |
|-------|---------|--------|
| REZN — *Inefficient Markets Without Noise* | `solver/` | yes |
| _(add future papers here)_ | | |
