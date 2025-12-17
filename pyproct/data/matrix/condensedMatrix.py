import numpy as np

class CondensedMatrix:
    
    def element_neighbors_within_radius(self, element_index, radius):
        """
        Return a list of neighbor indices j such that dist(element_index, j) <= radius.
        Includes neither self nor guarantees any order.
        Complexity: O(n) per call (DBSCAN will call this a lot).
        """
        n = self.row_length
        neigh = []
        for j in range(n):
            if j == element_index:
                continue
            if self.get_value(element_index, j) <= radius:
                neigh.append(j)
        return neigh
    
    def get_number_of_rows(self):
        return self.row_length

    def get_number_of_columns(self):
        return self.row_length
    
    def get_data(self):
        return self._data
    
    def get_number_of_elements(self):
        # alias defensivo (a veces se usa con matrices)
        return self.row_length
    
    def __getitem__(self, key):
        """
        Permite acceder como matriz: m[i, j]
        """
        if isinstance(key, tuple) and len(key) == 2:
            i, j = key
            return self.get_value(int(i), int(j))
        raise TypeError("CondensedMatrix indices must be a tuple (i, j)")
    
    def __len__(self):
        return len(self._data)

    def __init__(self, data):
        data = np.asarray(data)

        if data.ndim == 1:
            self._data = data
            L = len(data)
            n = int((1 + np.sqrt(1 + 8*L)) / 2)
            self.row_length = n
        else:
            n = data.shape[0]
            self.row_length = n
            self._data = data[np.tril_indices(n, k=-1)]

    def get_data(self):
        return self._data

    def get_value(self, i, j):
        if i == j:
            return 0.0
        if i < j:
            i, j = j, i
        n = self.row_length
        idx = n*j - j*(j+1)//2 + (i-j-1)
        return self._data[idx]

    ###########################################################################
    # --- EXTRA API REQUIRED BY GROMOS ALGORITHM ---
    ###########################################################################

    def get_row(self, i):
        """Return full row i as a numpy array."""
        n = self.row_length
        row = np.zeros(n)
        for j in range(n):
            row[j] = self.get_value(i, j)
        return row

    def calculate_neighbourhood(self, node, cutoff):
        """Return list of neighbours of `node` closer than cutoff."""
        neigh = []
        n = self.row_length
        for j in range(n):
            if j != node and self.get_value(node, j) < cutoff:
                neigh.append(j)
        return neigh

    def choose_node_with_higher_cardinality(self, node_list, cutoff):
        """
        Return (node, neighbour_count) of the node with most neighbours under cutoff.
        """
        best_node = None
        best_card = -1

        for node in node_list:
            neigh = self.calculate_neighbourhood(node, cutoff)
            card = len(neigh)
            if card > best_card:
                best_card = card
                best_node = node

        return best_node, best_card

    def get_neighbors_for_node(self, node, remaining_nodes, cutoff):
        """
        Returns neighbours of `node` among `remaining_nodes`,
        where distance < cutoff.
        """
        neigh = []
        for j in remaining_nodes:
            if j != node and self.get_value(node, j) < cutoff:
                neigh.append(j)
        return neigh

    def get_neighborhood(self, node, cutoff):
        """
        Alias used by some old GROMOS implementations.
        Returns all neighbours of node under cutoff.
        """
        return self.calculate_neighbourhood(node, cutoff)
