import numpy as np

class RadiiCalculator:
    """
    Computes cluster radii:

        Radius(C) = max distance of any element in C to the centroid of C

    The centroid is defined in index-space:
        centroid = argmin_i sum_j d(i,j)

    (This works for RMSD matrices).
    """

    def __init__(self, distance_matrix):
        self.dm = distance_matrix

    def calculate(self, clustering):
        clusters = {cid: cl.elems[:] for cid, cl in clustering.clusters.items()}

        radii = {}

        for cid, elems in clusters.items():
            k = len(elems)
            if k <= 1:
                radii[cid] = 0.0
                continue

            # find pseudo-centroid: element minimizing total distance to others
            total_dist = []
            for i in elems:
                total = sum(self.dm.get_value(i, j) for j in elems)
                total_dist.append((total, i))

            centroid = min(total_dist)[1]

            # radius = max distance centroid → others
            r = max(self.dm.get_value(centroid, j) for j in elems)

            radii[cid] = float(r)

        global_r = float(np.mean(list(radii.values()))) if radii else 0.0

        return {
            "radii_per_cluster": radii,
            "global_radii": global_r
        }

