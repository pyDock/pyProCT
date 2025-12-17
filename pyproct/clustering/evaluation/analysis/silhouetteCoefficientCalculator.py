import numpy as np

class SilhouetteCoefficientCalculator:
    """
    Computes the silhouette coefficient for each element and the mean silhouette
    of each cluster.
    """

    def __init__(self, distance_matrix):
        # distance_matrix is a CondensedMatrix
        self.dm = distance_matrix

    def calculate(self, clustering):
        """
        clustering: pyProCT clustering object
        returns: dict with silhouette per cluster and global silhouette
        """

        # Get cluster assignments
        labels = clustering.clusters
        # Flatten cluster membership
        elem_to_cluster = {}

        for cid, cluster in labels.items():
            for e in cluster.elems:
                elem_to_cluster[e] = cid

        N = len(elem_to_cluster)

        # For fast access: cluster → list of elements
        clusters = {cid: cluster.elems[:] for cid, cluster in labels.items()}

        silhouette_per_elem = {}

        for i in range(N):
            ci = elem_to_cluster[i]
            own_cluster = clusters[ci]

            # --- a(i): mean distance to same cluster
            if len(own_cluster) > 1:
                ai = np.mean([self.dm.get_value(i, j)
                              for j in own_cluster if j != i])
            else:
                ai = 0.0

            # --- b(i): mean distance to nearest other cluster
            bi = np.inf
            for cj, other_elems in clusters.items():
                if cj == ci:
                    continue
                if len(other_elems) == 0:
                    continue
                dist = np.mean([self.dm.get_value(i, j) for j in other_elems])
                bi = min(bi, dist)

            # silhouette(i)
            si = 0.0
            if len(own_cluster) > 1:
                si = (bi - ai) / max(ai, bi)

            silhouette_per_elem[i] = si

        # Aggregate by cluster
        silhouette_per_cluster = {}
        for cid, elems in clusters.items():
            if len(elems) == 0:
                silhouette_per_cluster[cid] = 0.0
            else:
                silhouette_per_cluster[cid] = float(
                    np.mean([silhouette_per_elem[e] for e in elems])
                )

        # Global silhouette
        global_s = float(np.mean(list(silhouette_per_elem.values())))

        return {
            "silhouette_per_element": silhouette_per_elem,
            "silhouette_per_cluster": silhouette_per_cluster,
            "global_silhouette": global_s
        }

