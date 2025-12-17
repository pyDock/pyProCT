import numpy as np

class BaseCalculator:
    def __init__(self, distance_matrix):
        # distance_matrix is CondensedMatrix
        self.dm = distance_matrix
        self.n = distance_matrix.row_length

    def d(self, i, j):
        return self.dm.get_value(i, j)


class CohesionCalculator(BaseCalculator):

    def evaluate(self, clustering, dm=None):
        results = {}

        clusters = clustering.clusters

        # Soportar lista o dict
        if isinstance(clusters, list):
            iterable = enumerate(clusters)
        else:
            iterable = clusters.items()

        for cluster_id, cluster in iterable:
            elems = cluster.all_elements
            if len(elems) < 2:
                results[cluster_id] = 0.0
                continue

            dsum = 0.0
            count = 0
            for i in range(len(elems)):
                for j in range(i + 1, len(elems)):
                    dsum += self.d(elems[i], elems[j])
                    count += 1

            results[cluster_id] = dsum / count

        return results
class CompactnessCalculator(BaseCalculator):

    def evaluate(self, clustering, dm=None):
        results = {}
        clusters = clustering.clusters

        if isinstance(clusters, list):
            iterable = enumerate(clusters)
        else:
            iterable = clusters.items()

        for cluster_id, cluster in iterable:
            elems = cluster.all_elements
            if len(elems) < 2:
                results[cluster_id] = 0.0
                continue

            best = None
            best_sum = np.inf
            for c in elems:
                s = sum(self.d(c, x) for x in elems)
                if s < best_sum:
                    best_sum = s
                    best = c

            results[cluster_id] = best_sum / len(elems)

        return results



class SeparationCalculator(BaseCalculator):
    """
    Minimum distance between two clusters.
    """
    def evaluate(self, clustering, dm=None):
        cluster_ids = list(clustering.clusters.keys())
        k = len(cluster_ids)
        sep = np.full((k, k), np.inf)

        for i in range(k):
            A = clustering.clusters[cluster_ids[i]].all_elements
            for j in range(i + 1, k):
                B = clustering.clusters[cluster_ids[j]].all_elements
                m = min(self.d(a, b) for a in A for b in B)
                sep[i, j] = sep[j, i] = m

        return sep.tolist()

class RadiiCalculator(BaseCalculator):

    def evaluate(self, clustering, dm=None):
        results = {}
        clusters = clustering.clusters

        if isinstance(clusters, list):
            iterable = enumerate(clusters)
        else:
            iterable = clusters.items()

        for cluster_id, cluster in iterable:
            elems = cluster.all_elements
            if len(elems) < 2:
                results[cluster_id] = 0.0
                continue

            # medoid
            best_sum = np.inf
            best_node = None
            for c in elems:
                s = sum(self.d(c, x) for x in elems)
                if s < best_sum:
                    best_sum = s
                    best_node = c

            radius = max(self.d(best_node, x) for x in elems)
            results[cluster_id] = radius

        return results

class SilhouetteCoefficientCalculator(BaseCalculator):

    def evaluate(self, clustering, dm=None):
        clusters = clustering.clusters

        # Assign labels
        labels = np.full(self.n, -1)

        if isinstance(clusters, list):
            cluster_items = list(enumerate(clusters))
        else:
            cluster_items = list(clusters.items())

        for cid, cluster in cluster_items:
            for x in cluster.all_elements:
                labels[x] = cid

        s = np.zeros(self.n)

        for i in range(self.n):
            own = labels[i]
            if own == -1:
                continue

            own_members = clusters[own].all_elements

            # a(i)
            if len(own_members) > 1:
                a = np.mean([self.d(i, j) for j in own_members if j != i])
            else:
                a = 0.0

            b = np.inf
            for cid2, cluster2 in cluster_items:
                if cid2 == own:
                    continue
                B = cluster2.all_elements
                b = min(b, np.mean([self.d(i, j) for j in B]))

            s[i] = (b - a) / max(a, b)

        results = {}
        for cid, cluster in cluster_items:
            vals = s[cluster.all_elements]
            results[cid] = float(np.mean(vals))

        return results
