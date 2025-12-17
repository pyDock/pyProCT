import numpy as np

class RatioCut:
    """
    RatioCut metric reconstructed in pure Python.
    Works over CondensedMatrix and standard cluster lists.
    """

    def __init__(self, matrix):
        # matrix must be a CondensedMatrix
        self.matrix = matrix
        self.N = matrix.row_length

    def _cut(self, cluster, rest):
        """ Sum of distances between points in cluster and points outside """
        m = self.matrix
        total = 0.0
        for i in cluster:
            for j in rest:
                total += m.get_value(i, j)
        return total

    def calculate(self, clustering):
        """
        clustering.elements is expected to be a list of clusters,
        each cluster a list of indices.
        """

        clusters = clustering.clusters  # pyProCT clustering object API
        ratio_sum = 0.0

        all_nodes = set(range(self.N))

        for cluster in clusters:
            if len(cluster) == 0:
                continue

            cluster_set = set(cluster)
            rest_set = all_nodes - cluster_set

            cut_value = self._cut(cluster_set, rest_set)

            # RatioCut term
            ratio_sum += cut_value / len(cluster)

        return {"ratio_cut": ratio_sum}

