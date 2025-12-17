# pyProCT (Python 3 fork)

**pyProCT** is a clustering framework designed to analyze large ensembles of protein conformations, with a strong focus on **protein–protein docking** and **structural similarity clustering**.

This repository is a **Python 3 compatible fork** of the original pyProCT project, preserving its original philosophy while updating the codebase to work with modern Python, NumPy, SciPy, and Cython.

---

## 1. What is pyProCT?

pyProCT is a modular framework that:

* Computes distance matrices between structures (typically L-RMSD)
* Applies multiple clustering algorithms
* Evaluates cluster quality using different metrics
* Selects the best clustering automatically
* Generates postprocessing outputs (clusters, representatives, statistics)

Originally designed for docking decoy analysis, it is still very well suited for that purpose.

---

## 2. Important differences from the original pyProCT

⚠️ **This fork is not a drop-in replacement of the original repository.**

Key differences:

* ✅ **Python 3.9+ compatible**
* ❌ `pyRMSD` is no longer a mandatory dependency
* 🔧 Scheduler, analysis pipeline and postprocessing loader were fixed
* 🧠 Cython extensions were updated and recompiled:

  * DBSCAN
  * Spectral clustering
* 🧮 NumPy deprecations fixed:

  * `np.float` → `float / np.float64`
  * `np.int` → `int / np.int64`
* 📐 SciPy API updated:

  * `eigvals` → `subset_by_index`
* 📄 JSON schemas slightly clarified (parameter names matter)

The goal of this fork is **functionality and reproducibility**, not feature expansion.

---

## 3. Installation (Python 3)

### Requirements

* Python ≥ 3.9
* NumPy
* SciPy
* Cython
* matplotlib (optional, for plots)

```bash
conda create -n pyproct python=3.10
conda activate pyproct
pip install psutil numpy scipy cython matplotlib
```

Clone the repository:

```bash
git clone https://github.com/<your-user>/pyproct-python3.git
cd pyproct-python3
```

### Compile Cython extensions

# DBSCAN
```bash
python pyproct/clustering/algorithms/dbscan/cython/setup.py build_ext --inplace
```
# Spectral
```bash
python pyproct/clustering/algorithms/spectral/cython/setup.py build_ext --inplace
```
# pyProCT
```bash
pip install -e .
```

Verify:

```bash
python -c "import pyproct.clustering.algorithms.dbscan.cython.cythonDbscanTools"
python -c "import pyproct.clustering.algorithms.spectral.cython.spectralTools"
```

---

## 4. Quick start

```bash
python -m pyproct.main config.json
```

Where `config.json` defines:

* input structures
* clustering algorithms
* evaluation criteria
* postprocessing actions

---

## 5. Distance matrices

pyProCT typically works with **condensed distance matrices** (as in SciPy).

In docking applications, distances usually represent **L-RMSD (Å)**.

Typical observed ranges:

```
min ≈ 0.7 Å
median ≈ 50 Å
p95 ≈ 80 Å
max ≈ 85 Å
```

This scale is important when choosing clustering parameters.

---

## 6. Clustering algorithms

### ✅ Supported and tested algorithms

| Algorithm    | Status      | Notes                     |
| ------------ | ----------- | ------------------------- |
| gromos       | ✅ Stable    | Recommended for docking   |
| dbscan       | ✅ Stable    | Parameter sensitive       |
| kmedoids     | ✅ Stable    | Requires K                |
| hierarchical | ✅ Stable    | Cutoff critical           |
| spectral     | ✅ Stable    | Computationally expensive |
| random       | ⚠️ Baseline | For comparison only       |

---

### 6.1 GROMOS (recommended)

```json
"gromos": {
  "parameters": [
    { "cutoff": 4.0 },
    { "cutoff": 6.0 },
    { "cutoff": 8.0 }
  ]
}
```

* `cutoff` = maximum RMSD (Å) to consider two structures neighbors
* Typical values:

  * 2–4 Å: very strict
  * 6–8 Å: flexible docking

---

### 6.2 DBSCAN

```json
"dbscan": {
  "parameters": [
    { "eps": 10.0, "minpts": 2 },
    { "eps": 15.0, "minpts": 2 },
    { "eps": 20.0, "minpts": 2 }
  ]
}
```

**Interpretation (important):**

* `eps` = maximum RMSD distance (Å)
* `minpts` = minimum number of neighbors to form a cluster

If `eps` is too small → **0 clusters**
If `eps` is large → fewer, larger clusters

---

### 6.3 K-Medoids

```json
"kmedoids": {
  "parameters": [
    { "k": 5 },
    { "k": 10 },
    { "k": 20 }
  ]
}
```

* Requires knowing approximately how many clusters you expect
* Very stable algorithm

---

### 6.4 Hierarchical clustering

```json
"hierarchical": {
  "parameters": [
    { "method": "average", "cutoff": 6.0 },
    { "method": "average", "cutoff": 8.0 },
    { "method": "average", "cutoff": 10.0 }
  ]
}
```

Notes:

* `average` is usually better than `complete` for RMSD
* Very sensitive to `cutoff`
* Can generate many singletons if cutoff is small

---

### 6.5 Spectral clustering

```json
"spectral": {
  "parameters": [
    { "max_clusters": 10 },
    { "max_clusters": 20 }
  ],
  "force_sparse": false
}
```

* More expensive than other methods
* Useful for non-convex cluster shapes
* Requires well-scaled distance matrices

---

### 6.6 Random (baseline)

```json
"random": {
  "parameters": [
    { "num_of_clusters": 2 },
    { "num_of_clusters": 5 }
  ]
}
```

* Not a real clustering algorithm
* Useful as a **baseline** for evaluation metrics

---

## 7. Evaluation criteria

For docking applications, **Silhouette** and **Cohesion** are the most informative.

Example:

```json
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
```

Notes:

* Silhouette can be `NaN` for 1-cluster solutions (this is expected)
* Some algorithms may generate valid clusterings that are later rejected by evaluation filters

---

## 8. Postprocessing actions (KEYWORD list)

Valid postprocessing actions:

| KEYWORD           | Description                      |
| ----------------- | -------------------------------- |
| representatives   | representative structures        |
| clusters          | PDB files per cluster            |
| cluster_stats     | per-cluster statistics           |
| rmsf              | RMSF per cluster                 |
| centers_and_trace | cluster centers and trajectories |
| compression       | redundancy elimination           |

⚠️ Note:
`pdb_clusters` was replaced by `clusters`.

---

## 9. Known limitations

* DBSCAN may legitimately return zero clusters for some parameters
* Hierarchical clustering can generate many singletons
* Spectral clustering is sensitive to matrix scaling
* Random clustering is not meaningful scientifically
* Not all “Improductive clustering search” messages indicate a bug

---

## 10. Recommended workflow for docking

1. Start with **GROMOS**
2. Add **DBSCAN** with increasing `eps`
3. Use **Silhouette** as main selection criterion
4. Inspect cluster representatives visually
5. Use hierarchical only for exploratory analysis

---

## 11. Citation

Original pyProCT paper:

<img src="img/cite.png"></img> If you plan to use pyProCT or any of its parts, including its documentation, to write a scientific article, 
please consider to add the following cite:  
*J. Chem. Theory Comput., 2014, 10 (8), pp 3236–3243*  

This fork provides **Python 3 compatibility and maintenance fixes**, but does not change the scientific methodology.
