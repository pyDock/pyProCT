import os
import tempfile
import unittest

import numpy
from scipy.spatial.distance import pdist

import validation.bidimensional.datasets as validation_data
from pyproct.clustering.algorithms.gromos.gromosAlgorithm import GromosAlgorithm
from pyproct.data.matrix.condensedMatrix import CondensedMatrix
from pyproct.data.matrix.matrixCalculator import MatrixCalculator
from pyproct.data.matrix.matrixHandler import MatrixHandler
from pyproct.driver.parameters import ProtocolParameters


def load_validation_observations(dataset_name):
    observations = []
    scale_factor = validation_data.scale_factor[dataset_name]
    for line in validation_data.all_datasets[dataset_name].split("\n"):
        values = line.split()
        if values:
            observations.append((float(values[0]) * scale_factor,
                                 float(values[1]) * scale_factor))
    return observations


def build_validation_matrix(dataset_name):
    return CondensedMatrix(pdist(load_validation_observations(dataset_name)))


class TestValidationBidimensionalMatrices(unittest.TestCase):

    def test_statistics_match_pyRMSD_reference(self):
        expected = {
            "concentric_circles": {
                "rows": 450,
                "size": 101025,
                "min": 0.055901698768138885,
                "max": 55.43403625488281,
                "mean": 21.19996872575433,
                "variance": 120.75018333564314,
            },
            "spaeth_01": {
                "rows": 37,
                "size": 666,
                "min": 1.4142135381698608,
                "max": 46.69047164916992,
                "mean": 22.15030047037938,
                "variance": 129.6464688359493,
            },
        }

        for dataset_name, stats in expected.items():
            matrix = build_validation_matrix(dataset_name)
            self.assertEqual(stats["rows"], matrix.row_length)
            self.assertEqual(stats["size"], matrix.data_size)
            self.assertAlmostEqual(stats["min"], matrix.calculateMin(), places=12)
            self.assertAlmostEqual(stats["max"], matrix.calculateMax(), places=12)
            self.assertAlmostEqual(stats["mean"], matrix.calculateMean(), places=12)
            self.assertAlmostEqual(stats["variance"], matrix.calculateVariance(), places=12)

    def test_known_distances_and_gromos_reference(self):
        matrix = build_validation_matrix("spaeth_01")
        self.assertAlmostEqual(float(numpy.float32(2.23606797749979)),
                               matrix[0, 1],
                               places=12)
        self.assertAlmostEqual(float(numpy.float32(46.69047011971501)),
                               matrix.calculateMax(),
                               places=12)

        clustering = GromosAlgorithm(matrix).perform_clustering({"cutoff": 5.0})
        clustering_dic = clustering.to_dic()
        self.assertEqual(12, clustering_dic["number_of_clusters"])
        self.assertEqual(
            {
                "prototype": 13,
                "elements": "4, 6, 8, 10, 13:14, 17:20",
                "id": "cluster_0",
            },
            clustering_dic["clusters"][0]
        )

    def test_load_alias_matches_matrix_load(self):
        matrix = CondensedMatrix(numpy.array([1., 2., 3.]))
        tmp_dir = tempfile.mkdtemp()
        matrix_path = os.path.join(tmp_dir, "matrix")
        MatrixHandler.save_matrix(matrix_path, matrix)

        loaded_with_alias = MatrixCalculator.calculate(
            None,
            ProtocolParameters({
                "method": "load",
                "parameters": {"path": matrix_path}
            })
        ).distance_matrix
        loaded_with_full_name = MatrixCalculator.calculate(
            None,
            ProtocolParameters({
                "method": "matrix::load",
                "parameters": {"path": matrix_path}
            })
        ).distance_matrix

        numpy.testing.assert_array_equal(loaded_with_full_name.get_data(),
                                         loaded_with_alias.get_data())


if __name__ == "__main__":
    unittest.main()
