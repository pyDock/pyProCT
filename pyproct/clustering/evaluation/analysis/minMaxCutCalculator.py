import numpy as np

class MinMaxCut:
    """
    MinMaxCut metric, using similarity derived from distances:
        w(i,j) = 1 / (1 + d(i,j))
    """

    def __init__(self, distance_matrix):
        self.dm = distance_matrix

    def w(self, i, j):
        d = self.dm.get_value(i, j)
        return 1.0 / (1.0 + d)

    def calculate(self, clustering):
        clusters = {cid: cl.elems[:] for cid, cl in clustering.clusters.items()}
        all_nodes = set().union(*clusters.values())

        mmc_vals = {}

        for cid, elems in clusters.items():

            C = set(elems)
            notC = list(all_nodes - C)

            if len(C) <= 1:
                mmc_vals[cid] = 0.0
                continue

            # Internal association
            assoc_in = 0.0
            for i in C:
                for j in C:
                    if i != j:
                        assoc_in += self.w(i, j)

            # External association
            assoc_out = 0.0
            for i in C:
                for j in notC:
                    assoc_out += self.w(i, j)

            if assoc_in == 0:
                mmc_vals[cid] = 0.0
            else:
                mmc_vals[cid] = float(assoc_out / assoc_in)

        global_mmc = float(np.mean(list(mmc_vals.values()))) if mmc_vals else 0.0

        return {
            "minmaxcut_per_cluster": mmc_vals,
            "global_minmaxcut": global_mmc
        }

