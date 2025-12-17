# Docking Clustering Guide with pyProCT

This guide provides practical recommendations for clustering docking poses
using **pyProCT (Python 3 fork)**.

---

## General assumptions

- Distances are typically **L-RMSD (Å)**.
- Poses with RMSD ≤ **8–10 Å** are often considered similar.
- Noise usually corresponds to unstable or irrelevant poses.

---

## Recommended algorithms for docking

### ✅ DBSCAN (recommended)

Best choice for docking pose clustering.

```json
{
  "eps": 10.0,
  "minpts": 2
}
````

#### Tips

* Start with `eps = 10–15 Å`
* Use `minpts = 2` or `3`
* Noise represents weak or unique poses

---

### ✅ GROMOS

Good alternative when you want all poses clustered.

```json
{
  "cutoff": 10.0
}
```

#### Tips

* Use when you do not want noise
* Very robust and fast

---

### ⚠️ Hierarchical

Use only for exploratory analysis.

```json
{
  "method": "average",
  "cutoff": 8.0
}
```

---

## Evaluation metrics

Recommended metrics for docking:

```json
{
  "Cohesion": { "action": ">", "weight": 1 },
  "Silhouette": { "action": ">", "weight": 1 }
}
```

### Interpretation

* **High cohesion** → compact clusters
* **High silhouette** → good separation
* **High noise** → many unique poses

---

## Practical workflow

1. Start with DBSCAN
2. Adjust `eps` until meaningful cluster sizes appear
3. Inspect representatives
4. Compare with GROMOS if needed

---

## Typical parameter ranges

| Parameter       | Range    |
| --------------- | -------- |
| eps             | 8 – 20 Å |
| minpts          | 2 – 4    |
| cutoff (GROMOS) | 8 – 12 Å |

---

## Final recommendation

> For docking studies, **DBSCAN with eps ≈ 10–15 Å and minpts = 2**
> provides the most meaningful clustering results.

---
