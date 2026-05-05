pyProCT (Python 3 fork)
=======================

**pyProCT** is a clustering framework designed to analyze large
ensembles of protein conformations, with a strong focus on
**protein–protein docking** and **structural similarity clustering**.

This repository is a **Python 3 compatible fork** of the original
pyProCT project, preserving its original philosophy while updating the
codebase to work with modern Python, NumPy, SciPy, and Cython.

Migration and validation details are tracked in
`docs/PYTHON3_MIGRATION.md <docs/PYTHON3_MIGRATION.md>`_.

--------------

1. What is pyProCT?
-------------------

pyProCT is a modular framework that:

-  Computes distance matrices between structures (typically L-RMSD)
-  Applies multiple clustering algorithms
-  Evaluates cluster quality using different metrics
-  Selects the best clustering automatically
-  Generates postprocessing outputs (clusters, representatives,
   statistics)

Originally designed for docking decoy analysis, it is still very well
suited for that purpose.

--------------

2. Important differences from the original pyProCT
--------------------------------------------------

⚠️ **This fork is not a drop-in replacement of the original
repository.**

Key differences:

-  ✅ **Python 3.9+ compatible**

-  ❌ External ``pyRMSD`` is no longer a mandatory dependency; this fork
   includes a local compatibility wrapper for the API used by pyProCT

-  🔧 Scheduler, analysis pipeline and postprocessing loader were fixed

-  🧠 Cython extensions were updated and recompiled:

   -  DBSCAN
   -  Spectral clustering

-  🧮 NumPy deprecations fixed:

   -  ``np.float`` → ``float / np.float64``
   -  ``np.int`` → ``int / np.int64``

-  📐 SciPy API updated:

   -  ``eigvals`` → ``subset_by_index``

-  📄 JSON schemas slightly clarified (parameter names matter)

The goal of this fork is **functionality and reproducibility**, not
feature expansion.

--------------

3. Installation (Python 3)
--------------------------

Requirements
~~~~~~~~~~~~

-  Python ≥ 3.9
-  NumPy
-  SciPy
-  Cython
-  matplotlib (optional, for plots)

.. code:: bash

   conda create -n pyproct python=3.10
   conda activate pyproct
   pip install psutil numpy scipy cython matplotlib

Clone the repository:

.. code:: bash

   git clone https://github.com/pyDock/pyProCT.git
   cd pyProCT

Compile Cython extensions
~~~~~~~~~~~~~~~~~~~~~~~~~

DBSCAN
======

.. code:: bash

   python pyproct/clustering/algorithms/dbscan/cython/setup.py build_ext --inplace

Spectral
========

.. code:: bash

   python pyproct/clustering/algorithms/spectral/cython/setup.py build_ext --inplace

pyProCT
=======

.. code:: bash

   pip install -e .

Verify:

.. code:: bash

   python -c "import pyproct.clustering.algorithms.dbscan.cython.cythonDbscanTools"
   python -c "import pyproct.clustering.algorithms.spectral.cython.spectralTools"

--------------

4. Quick start
--------------

.. code:: bash

   python -m pyproct.main config.json

Where ``config.json`` defines:

-  input structures
-  clustering algorithms
-  evaluation criteria
-  postprocessing actions

--------------

5. Distance matrices
--------------------

pyProCT typically works with **condensed distance matrices** (as in
SciPy).

In docking applications, distances usually represent **L-RMSD (Å)**.

Typical observed ranges:

::

   min ≈ 0.7 Å
   median ≈ 50 Å
   p95 ≈ 80 Å
   max ≈ 85 Å

This scale is important when choosing clustering parameters.

--------------

6. Clustering algorithms
------------------------

✅ Supported and tested algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

============ =========== =========================
Algorithm    Status      Notes
============ =========== =========================
gromos       ✅ Stable   Recommended for docking
dbscan       ✅ Stable   Parameter sensitive
kmedoids     ✅ Stable   Requires K
hierarchical ✅ Stable   Cutoff critical
spectral     ✅ Stable   Computationally expensive
random       ⚠️ Baseline For comparison only
============ =========== =========================

--------------

6.1 GROMOS (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   "gromos": {
     "parameters": [
       { "cutoff": 4.0 },
       { "cutoff": 6.0 },
       { "cutoff": 8.0 }
     ]
   }

-  ``cutoff`` = maximum RMSD (Å) to consider two structures neighbors

-  Typical values:

   -  2–4 Å: very strict
   -  6–8 Å: flexible docking

--------------

.. _dbscan-1:

6.2 DBSCAN
~~~~~~~~~~

.. code:: json

   "dbscan": {
     "parameters": [
       { "eps": 10.0, "minpts": 2 },
       { "eps": 15.0, "minpts": 2 },
       { "eps": 20.0, "minpts": 2 }
     ]
   }

**Interpretation (important):**

-  ``eps`` = maximum RMSD distance (Å)
-  ``minpts`` = minimum number of neighbors to form a cluster

If ``eps`` is too small → **0 clusters** If ``eps`` is large → fewer,
larger clusters

--------------

6.3 K-Medoids
~~~~~~~~~~~~~

.. code:: json

   "kmedoids": {
     "parameters": [
       { "k": 5 },
       { "k": 10 },
       { "k": 20 }
     ]
   }

-  Requires knowing approximately how many clusters you expect
-  Very stable algorithm

--------------

6.4 Hierarchical clustering
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   "hierarchical": {
     "parameters": [
       { "method": "average", "cutoff": 6.0 },
       { "method": "average", "cutoff": 8.0 },
       { "method": "average", "cutoff": 10.0 }
     ]
   }

Notes:

-  ``average`` is usually better than ``complete`` for RMSD
-  Very sensitive to ``cutoff``
-  Can generate many singletons if cutoff is small

--------------

6.5 Spectral clustering
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   "spectral": {
     "parameters": [
       { "max_clusters": 10 },
       { "max_clusters": 20 }
     ],
     "force_sparse": false
   }

-  More expensive than other methods
-  Useful for non-convex cluster shapes
-  Requires well-scaled distance matrices

--------------

6.6 Random (baseline)
~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   "random": {
     "parameters": [
       { "num_of_clusters": 2 },
       { "num_of_clusters": 5 }
     ]
   }

-  Not a real clustering algorithm
-  Useful as a **baseline** for evaluation metrics

--------------

7. Evaluation criteria
----------------------

For docking applications, **Silhouette** and **Cohesion** are the most
informative.

Example:

.. code:: json

   "evaluation": {
     "evaluation_criteria": {
       "criteria_0": {
         "Silhouette": {
           "action": ">",
           "weight": 1
         }
       }
     },
     "maximum_noise": 30,
     "minimum_cluster_size": 1
   }

Notes:

-  Silhouette can be ``NaN`` for 1-cluster solutions (this is expected)
-  Some algorithms may generate valid clusterings that are later
   rejected by evaluation filters

--------------

8. Postprocessing actions (KEYWORD list)
----------------------------------------

Valid postprocessing actions:

================= ================================
KEYWORD           Description
================= ================================
representatives   representative structures
clusters          PDB files per cluster
cluster_stats     per-cluster statistics
rmsf              RMSF per cluster
centers_and_trace cluster centers and trajectories
compression       redundancy elimination
================= ================================

⚠️ Note: ``pdb_clusters`` was replaced by ``clusters``.

--------------

9. Known limitations
--------------------

-  DBSCAN may legitimately return zero clusters for some parameters
-  Hierarchical clustering can generate many singletons
-  Spectral clustering is sensitive to matrix scaling
-  Random clustering is not meaningful scientifically
-  Not all “Improductive clustering search” messages indicate a bug

--------------

10. Recommended workflow for docking
------------------------------------

1. Start with **GROMOS**
2. Add **DBSCAN** with increasing ``eps``
3. Use **Silhouette** as main selection criterion
4. Inspect cluster representatives visually
5. Use hierarchical only for exploratory analysis

--------------

11. Citation
------------

Original pyProCT paper:

|  If you plan to use pyProCT or any of its parts, including its
  documentation, to write a scientific article, please consider to add
  the following cite:
| *J. Chem. Theory Comput., 2014, 10 (8), pp 3236–3243*

This fork provides **Python 3 compatibility and maintenance fixes**, but
does not change the scientific methodology.
