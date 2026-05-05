import os

import numpy


class CondensedMatrix(object):
    """
    Python 3 compatibility replacement for pyRMSD.condensedMatrix.CondensedMatrix.

    The internal data layout is the same one used by scipy.spatial.distance.pdist:
    (0,1), (0,2), ..., (0,n-1), (1,2), ...
    """

    def __init__(self, data):
        if isinstance(data, numpy.ndarray):
            data = numpy.asarray(data)
        else:
            data = numpy.asarray(data, dtype=numpy.float32)
        if data.ndim != 1:
            raise ValueError("[CondensedMatrix] Input numpy array must be a 1D real vector.")

        self._data = data
        self.data_size = len(data)
        self.row_length = int((1 + numpy.sqrt(1 + 8 * self.data_size)) / 2)

    def __len__(self):
        return self.data_size

    def __getitem__(self, key):
        if isinstance(key, tuple) and len(key) == 2:
            return self.get_value(key[0], key[1])
        return self._data[key]

    def __setitem__(self, key, value):
        if isinstance(key, tuple) and len(key) == 2:
            self.set_value(key[0], key[1], value)
        else:
            self._data[key] = value

    def _linear_index(self, i, j):
        if i > j:
            i, j = j, i
        return self.row_length * i - (i * (i + 1)) // 2 + (j - i - 1)

    def get_data(self):
        return self._data

    def get_number_of_rows(self):
        return self.row_length

    def get_number_of_columns(self):
        return self.row_length

    def get_number_of_elements(self):
        return self.row_length

    def get_expected_number_of_elements(self):
        return (self.row_length * (self.row_length - 1)) // 2

    def get_value(self, i, j):
        if i == j:
            return 0.0
        return float(numpy.float32(self._data[self._linear_index(int(i), int(j))]))

    def set_value(self, i, j, value):
        if i == j:
            return
        self._data[self._linear_index(int(i), int(j))] = numpy.float32(value)

    def get_row(self, i):
        row = numpy.zeros(self.row_length)
        for j in range(self.row_length):
            row[j] = self.get_value(i, j)
        return row

    def element_neighbors_within_radius(self, element_index, radius):
        return self.get_neighbors_for_node(
            element_index,
            range(self.row_length),
            radius
        )

    def calculate_neighbourhood(self, node, cutoff):
        return list(self.get_neighbors_for_node(node, range(self.row_length), cutoff))

    def get_neighborhood(self, node, cutoff):
        return self.calculate_neighbourhood(node, cutoff)

    def get_neighbors_for_node(self, node, remaining_nodes, cutoff):
        neighbours = []
        for other_node in remaining_nodes:
            if other_node != node and self.get_value(node, other_node) <= cutoff:
                neighbours.append(other_node)
        return numpy.array(neighbours, dtype=numpy.int32)

    def choose_node_with_higher_cardinality(self, node_list, cutoff):
        best_node = None
        best_cardinality = -1
        for node in node_list:
            cardinality = len(self.get_neighbors_for_node(node, node_list, cutoff))
            if cardinality > best_cardinality:
                best_node = node
                best_cardinality = cardinality
        return best_node, best_cardinality

    def recalculateStatistics(self):
        pass

    def _statistics_data(self):
        return self._data.astype(numpy.float32, copy=False)

    def calculateMin(self):
        return float(numpy.min(self._statistics_data()))

    def calculateMax(self):
        return float(numpy.max(self._statistics_data()))

    def calculateMean(self):
        return float(numpy.mean(self._statistics_data(), dtype=numpy.float64))

    def calculateVariance(self):
        return float(numpy.var(self._statistics_data(), dtype=numpy.float64))

    def calculateSkewness(self):
        data = self._statistics_data()
        std = numpy.sqrt(self.calculateVariance())
        if std == 0:
            return 0.0
        centered = data - self.calculateMean()
        return float(numpy.mean(centered ** 3, dtype=numpy.float64) / (std ** 3))

    def calculateKurtosis(self):
        data = self._statistics_data()
        std = numpy.sqrt(self.calculateVariance())
        if std == 0:
            return 0.0
        centered = data - self.calculateMean()
        return float(numpy.mean(centered ** 4, dtype=numpy.float64) / (std ** 4) - 3.0)

    def save(self, matrix_file_without_extension):
        numpy.save(matrix_file_without_extension, self.get_data())

    @classmethod
    def load(cls, matrix_file_without_extension):
        path = matrix_file_without_extension
        if not os.path.exists(path):
            path = matrix_file_without_extension + ".npy"
        return cls(list(numpy.load(path).astype(numpy.float64, copy=False)))
