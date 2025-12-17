import numpy as np

class CohesionCalculator:
    """
    Computes cohesion of a cluster = average intra-cluster distance.
    """

    def __init__(self, distance_matrix):
        # distance_matrix is a CondensedMatrix
        self.dm = distance_matrix

    def calculate(self, clustering):
        """
        clustering: pyProCT clustering object
        returns: dict cluster_id -> cohesion_value
        """
        cohesions = {}

        for cid, cluster in clustering.clusters.items():
            elems = cluster.elems
            k = len(elems)

            if k < 2:
                cohesions[cid] = 0.0
                continue

            # compute average pairwise distance inside cluster
            total = 0.0
            count = 0

            for i_idx in range(k):
                for j_idx in range(i_idx + 1, k):
                    i = elems[i_idx]
                    j = elems[j_idx]
                    total += self.dm.get_value(i, j)
                    count += 1

            cohesions[cid] = total / count

        return cohesions
