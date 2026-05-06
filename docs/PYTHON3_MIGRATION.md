# Python 3 Migration Notes

This document records the conservative Python 3 migration status for this
pyProCT fork. The goal of the migration is to preserve the behavior of the
original Python 2.7 pyProCT as closely as possible, not to redesign the
scientific workflow.

## Reference Environments

Python 2.7 original interpreter:

```bash
<PYPROCT_PY2_ENV>/bin/python
```

Python 3 migrated interpreter:

```bash
<PYPROCT_PY3_ENV>/bin/python
```

Original Python 2.7 source inspected:

```text
<PYPROCT_PY2_SOURCE>
```

Python 3 source:

```text
<PYPROCT_PY3_SOURCE>
```

Replace the placeholders above with the local paths used in your installation.
The placeholders used in this document are:

- `<PYPROCT_PY2_ENV>`: root of the Python 2.7 environment, for example
  `/path/to/conda/envs/pyproct2.7`
- `<PYPROCT_PY3_ENV>`: root of the Python 3 environment, for example
  `/path/to/conda/envs/pyproct`
- `<PYPROCT_PY2_SOURCE>`: original Python 2.7 package source, for example
  `/path/to/pyProCT-python2.7/pyproct`
- `<PYPROCT_REPO>`: root of the migrated Python 3 repository, for example
  `/path/to/pyProCT`
- `<PYPROCT_PY3_SOURCE>`: migrated Python 3 package source, usually
  `<PYPROCT_REPO>/pyproct`

## Current Python 3 Status

The migrated code is validated in the `pyproct` conda environment shown above.
It should be treated as a conservative functional port of the original Python
2.7 behavior for the modules, tests, and validation workflows documented here,
not as a redesign or a guarantee that every legacy/HPC workflow is directly
reproducible without local data or schema conversion.

## Technical Migration Commits

The core technical migration blocks were closed in these commits. Later
documentation-only commits may exist on top of this list.

```text
6fc6aaf Restore Python 3 matrix compatibility with pyProCT original
b09a987 Restore Python 3 plugin registry compatibility
aaba37d Restore Python 3 clustering compatibility
e345427 Restore Python 3 clustering evaluation compatibility
92e9320 Restore Python 3 driver workflow compatibility
058c4db Restore Python 3 RMSD conformation compatibility
734f653 Migrate legacy tests and imports for Python 3
242e873 Restore Python 3 spectral clustering compatibility
fde3700 Restore Python 3 postprocess compatibility
a72bc8b Finalize Python 3 migration validation
```

## Validation Commands

Install editable:

```bash
cd <PYPROCT_REPO>
<PYPROCT_PY3_ENV>/bin/python -m pip install -e .
```

Check imports:

```bash
<PYPROCT_PY3_ENV>/bin/python -c "import pyproct; import pyRMSD; print('imports OK')"
<PYPROCT_PY3_ENV>/bin/python -c "from pyRMSD.RMSDCalculator import RMSDCalculator; print(RMSDCalculator)"
```

Compile Python sources:

```bash
cd <PYPROCT_REPO>
<PYPROCT_PY3_ENV>/bin/python -m compileall -q pyproct pyRMSD
```

Run the test suite:

```bash
cd <PYPROCT_REPO>
<PYPROCT_PY3_ENV>/bin/python -m unittest discover pyproct -p 'Test*.py'
```

Expected current result:

```text
Ran 228 tests
OK (skipped=32)
```

The remaining skips are explicit legacy/TODO tests, optional plugin-entry-point
tests, tests for APIs absent from the original installed package, or cases that
require separate data/workflows.

## Validation Workflows

### Bidimensional Validation

The original `validation/bidimensional` workflow must be run from a copy, not
from the repository folder, because it writes matrices, workspaces, images, and
temporary files.

Example:

```bash
cd <PYPROCT_REPO>
tmpdir=$(mktemp -d /tmp/pyproct_validation_py3.XXXXXX)
cp -a validation "$tmpdir/"
cd "$tmpdir/validation/bidimensional"

PYTHONPATH="$tmpdir:<PYPROCT_REPO>" \
  <PYPROCT_PY3_ENV>/bin/python create_fake_pdb.py

PYTHONPATH="$tmpdir:<PYPROCT_REPO>" \
  <PYPROCT_PY3_ENV>/bin/python validation_main.py
```

Current Python 3 result for `concentric_circles`:

```text
173 clusterings generated
best algorithm: spectral
number of clusters: 3
mean cluster size: 150.0
noise: 0.0
CythonNormNCut: 0.017819798025965918
graph_criteria score: 1.0
```

The Python 2 installed baseline does not run the unmodified JSON because the
installed original does not accept `"method": "load"` globally. With a temporary
copy changed to `"matrix::load"`, it advances further but fails in the installed
Python 2 hierarchical path with NumPy's ambiguous array truth-value error.

### Conformations Validation

`validation/conformations` contains legacy scripts and HPC-oriented workflows,
but no local PDB/DCD input data. The `base_script.json` also uses an older
schema (`matrix.method: "rmsd"`, `global.pdbs`) that is not equivalent to the
current migrated driver schema.

The validated local equivalent uses versioned test data with:

- `protein::ensemble`
- `rmsd::ensemble`
- `QTRFIT_SERIAL_CALCULATOR`
- GROMOS clustering

Current Python 3 result:

```text
Loaded 4 conformations with 824 atoms
best algorithm: gromos
number of clusters: 1
noise: 0.0
cohesion: 0.0
```

## Compatibility Notes

Matrix method names currently validated:

- `load`
- `matrix::load`
- `matrix::combination`
- `array::euclidean`
- `rmsd::ensemble`
- `euclidean_distance::ensemble`

Data loader names currently validated:

- `features::array`
- `protein::ensemble`

The legacy names `rmsd` and `pdb_ensemble` were not added as broad aliases
because they are not accepted globally by the installed Python 2 reference in
the same way. If a legacy workflow needs them, convert the workflow in a copy
and document the conversion.

## pyRMSD Wrapper Scope

This fork includes a minimal `pyRMSD` compatibility package for the API used by
pyProCT:

- `pyRMSD.RMSDCalculator.RMSDCalculator`
- `pyRMSD.availableCalculators`
- `pyRMSD.condensedMatrix`
- `pyRMSD.matrixHandler`
- `pyRMSD.symmTools`

The external pyRMSD package is not required for the migrated Python 3 validation
path. This wrapper is not a full replacement for the original pyRMSD C
extension. RMSD fitting and condensed matrix behavior have been validated on
small deterministic cases, but advanced symmetry and accelerator-specific
behavior remain residual risks.

## Generated Artifacts

Do not include generated artifacts in migration commits:

- `pyProCT.egg-info/*`
- generated Cython `.c` files
- `.pyc`
- `__pycache__`
- validation outputs under temporary workspaces

Compiled extension modules (`*.so`) are required at runtime in this local setup,
but regenerated C sources should be kept out of ordinary migration commits
unless a dedicated Cython build/update block is being performed.

## Optional Plotting Dependencies

Plotting and report-generation helpers may require `matplotlib`, `Pillow`, and
Graphviz-related tooling for specific image outputs. The legacy state graph
helper also depends on the optional `pygraph` package; if it is missing, only
state graph rendering is unavailable. `seaborn` is treated as optional and only
affects plot styling; it is not imported during plugin discovery.

Scientific validation does not depend on pixel-by-pixel image comparisons.

## Residual Risks

- The `pyRMSD` compatibility layer is intentionally minimal.
- Symmetry handling is not exhaustively validated.
- Legacy `validation/conformations` workflows require external data or schema
  conversion.
- Some Python 2 installed workflows already fail under the available NumPy/Cython
  environment, so they are not clean baselines.
- The remaining skipped tests should be treated as explicit future work, not as
  silent success.
