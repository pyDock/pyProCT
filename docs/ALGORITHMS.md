# Clustering Algorithms in pyProCT (Python 3 fork)

This document describes the clustering algorithms currently available in this
Python 3–compatible fork of **pyProCT**, their parameters, and practical notes
about their behavior.

---

## Available algorithms

The following algorithms are implemented and tested:

- `gromos`
- `dbscan`
- `hierarchical`
- `kmedoids`
- `spectral`
- `random` ⚠️ (baseline / control only)

---

## 1. GROMOS

### Description
Distance-based clustering algorithm commonly used in molecular dynamics.
Clusters are built around central conformations using a distance cutoff.

### Parameters
```json
{
  "cutoff": 8.0
}
````

### Notes

* Very robust and fast.
* Widely used in MD trajectory analysis.
* All points are assigned to a cluster (no noise).

### Typical use

* MD trajectories
* Docking pose clustering
* Baseline clustering method

---

## 2. DBSCAN

### Description

Density-based clustering algorithm. Clusters are defined as dense regions in
distance space.

### Parameters

```json
{
  "eps": 15.0,
  "minpts": 2
}
```

| Parameter | Meaning                             |
| --------- | ----------------------------------- |
| `eps`     | Distance threshold (e.g. RMSD in Å) |
| `minpts`  | Minimum neighbors to form a cluster |

### Notes

* Can produce **noise** (unclustered conformations).
* Very sensitive to `eps`.
* Ideal for detecting dominant binding modes.

### Typical use

* Docking pose clustering
* Removing outliers
* Detecting multiple binding modes

---

## 3. Hierarchical

### Description

Agglomerative hierarchical clustering using a linkage method and a distance cutoff.

### Parameters

```json
{
  "method": "average",
  "cutoff": 10.0
}
```

Supported methods:

* `complete`
* `average`
* `single`

### Notes

* Cutoff strongly affects number of clusters.
* Can generate many small clusters.
* Silhouette score often useful to select best cutoff.

### Typical use

* Exploratory clustering
* Fine-grained cluster structure analysis

---

## 4. K-Medoids

### Description

Partitioning clustering algorithm similar to k-means but using real data points
(medoids).

### Parameters

```json
{
  "k": 5,
  "initial_seeding": "EQUIDISTANT"
}
```

### Notes

* Requires predefined number of clusters.
* No noise.
* More stable than k-means for distance matrices.

### Typical use

* When number of clusters is known
* Comparative benchmarking

---

## 5. Spectral

### Description

Graph-based clustering using eigenvectors of a Laplacian matrix.

### Parameters

```json
{
  "max_clusters": 10,
  "sigma": 10.0
}
```

### Notes

* Computationally expensive.
* Requires Cython extensions.
* Sensitive to numerical stability.

### Typical use

* Research / advanced analysis
* Not recommended for large datasets

---

## 6. Random ⚠️

### Description

Random assignment of elements into clusters.

### Parameters

```json
{
  "num_of_clusters": 2
}
```

### Notes

* **Not a real clustering algorithm**.
* Used only as baseline or control.

---

## Summary Table

| Algorithm    | Noise | Fast | MD-friendly | Recommended |
| ------------ | ----- | ---- | ----------- | ----------- |
| GROMOS       | No    | ✅    | ✅           | ⭐⭐⭐⭐        |
| DBSCAN       | Yes   | ✅    | ✅           | ⭐⭐⭐⭐⭐       |
| Hierarchical | No    | ⚠️   | ✅           | ⭐⭐⭐         |
| K-Medoids    | No    | ⚠️   | ⚠️          | ⭐⭐⭐         |
| Spectral     | No    | ❌    | ⚠️          | ⭐           |
| Random       | No    | ✅    | ❌           | ❌           |

---
