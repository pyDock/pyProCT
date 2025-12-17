import numpy as np

class NCut:
    """
    Normalized Cut evaluation for clusters.

    Using a similarity derived from distances:
        w(i,j) = 1 / (1 + d(i,j))

    For each cluster C:
        Ncut(C) = assoc(C, notC) / assoc(C, C)

    Global measure = mean NCut across clusters.
    """

    def __init__(self, distance_matrix):
        self.dm = distance_matrix

    def w(self, i, j):
        d = self.dm.get_value(i, j)
        return 1.0 / (1.0 + d)

    def calculate(self, clustering):
        clusters = {cid: cl.elems[:] for cid, cl in clustering.clusters.items()}
        all_nodes = set().union(*clusters.values())

        ncut_vals = {}

        for cid, elems in clusters.items():

            C = set(elems)
            notC = list(all_nodes - C)

            if len(C) <= 1:
                ncut_vals[cid] = 0.0
                continue

            assoc_CC = 0.0
            assoc_CnC = 0.0

            # assoc(C, C)
            for i in C:
                for j in C:
                    if i != j:
                        assoc_CC += self.w(i, j)

            # assoc(C, notC)
            for i in C:
                for j in notC:
                    assoc_CnC += self.w(i, j)

            if assoc_CC == 0:
                ncut_vals[cid] = 0.0
            else:
                ncut_vals[cid] = float(assoc_CnC / assoc_CC)

        global_ncut = float(np.mean(list(ncut_vals.values()))) if ncut_vals else 0.0

        return {
            "ncut_per_cluster": ncut_vals,
            "global_ncut": global_ncut
        }

