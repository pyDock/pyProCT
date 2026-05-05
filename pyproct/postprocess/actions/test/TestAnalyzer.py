"""
Created on 23/12/2013

@author: victor
"""
import unittest
import scipy.spatial.distance
import numpy
from pyproct.data.matrix.condensedMatrix import CondensedMatrix
from pyproct.postprocess.actions.confSpaceComparison.comparator import Analyzer
import json

# Force smarter float rep. to compare
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.4f')


class TestAnalizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.separated_decomposed_clusters = {
                                            "mixed":{
                                                "cluster_1": {
                                                     "traj_A":[0,1,2,3,4],
                                                     "traj_B":[5,6,7,8,9],
                                                     "traj_C":[10,11,12,13,14]
                                                }
                                            },
                                           "pure":{
                                               "cluster_2": {
                                                     "traj_A":[0,1,2,3,4]
                                               },
                                               "cluster_3": {
                                                    "traj_B":[5,6,7,8,9]
                                               }
                                            }
                                        }

        # 4 points forming a square with another point in its center
        square_points = numpy.array([[0,0], [0,2], [2,0], [2,2], [1,1]])

        # move the square to the right and up-right
        square_points_2 = square_points+numpy.array([0,5])
        square_points_3 = square_points+numpy.array([5,0])

        cls.square_points = square_points.tolist()
        cls.square_points.extend(square_points_2.tolist())
        cls.square_points.extend(square_points_3.tolist())
        cls.matrix = CondensedMatrix(scipy.spatial.distance.pdist(cls.square_points))

    def test_analyze_clustering(self):
        separated_decomposed_clusters = {
            'mixed': {
                      '1': {
                            'traj_A': [3],
                            'traj_B': [8, 10]
                            },
                      '2': {
                            'traj_A': [4],
                            'traj_B': [14, 15]
                            }
                      },
            'pure': {
                     '0': {
                           'traj_A': [0, 1, 2]
                           },
                     '3': {
                           'traj_A': [5, 6]
                           },
                     '4': {
                           'traj_B': [9, 11, 12, 13, 7]
                           }
                     }
        }

        expected_analysis = {
                             'num_pure': 3,
                             'num_mixed': 2,
                             'num_mixed_elements': 6,
                             'total_num_clusters': 5,
                             'num_pure_elements': 10,
                             'total_num_elements': 16,
                             'overlap': 0.10986121892929068,
                             'mixed_overlap': 0.2929632504781088,
                             }
        analysis = {}
        Analyzer.analyze_clustering(separated_decomposed_clusters, self.matrix, analysis)
        self.assertCountEqual(expected_analysis.keys(), analysis.keys())
        for key in expected_analysis:
            if isinstance(expected_analysis[key], float):
                self.assertAlmostEqual(expected_analysis[key], analysis[key], 12)
            else:
                self.assertEqual(expected_analysis[key], analysis[key])

    def test_analyze_clusters(self):

        expected_analysis = {
            'cluster_2': {
                'components': ['traj_A'],
                'global': {
                    'std': 0.5656854152679444,
                    'max': 1.4142135381698608,
                    'num_elements': 5,
                    'mean': 1.1313708305358887,
                    "traj_A":{
                        "max":1.4142135381698608,
                        "mean":1.1313708305358887,
                        "num_elements":5,
                        "std":0.5656854152679444
                    }
                }
            },
            'cluster_3': {
                'components': ['traj_B'],
                'global': {
                    'std': 0.56568541526794436,
                    'max': 1.4142135381698608,
                    'num_elements': 5,
                    'mean': 1.1313708305358887,
                    "traj_B":{
                        "max":1.4142135381698608,
                        "mean":1.1313708305358887,
                        "num_elements":5,
                        "std":0.5656854152679444
                    }
                }
            },
            'cluster_1': {
                'components': ['traj_A', 'traj_B', 'traj_C'],
                'centers_mean_diff': 5.6903559366861982,
                'global': {
                    'std': 1.5095995219901064,
                    'num_elements': 15,
                    'max': 5.385164737701416,
                    'overlap': 0.22174244562784828,
                    'traj_C': {
                        'std': 0.5656854152679444,
                        'max': 1.4142135381698608,
                        'num_elements': 5,
                        'mean': 1.1313708305358887
                    },
                    'traj_A': {
                        'std': 0.5656854152679444,
                        'max': 1.4142135381698608,
                        'num_elements': 5,
                        'mean': 1.1313708305358887
                    },
                    'traj_B': {
                        'std': 0.5656854152679444,
                        'max': 1.4142135381698608,
                        'num_elements': 5,
                        'mean': 1.1313708305358887
                    },
                    'mean': 3.3646855751673379
                }
            }
        }

        analysis = {}
        Analyzer.analyze_clusters(self.separated_decomposed_clusters, self.matrix, analysis)
        self.maxDiff = None
        self.assertCountEqual(expected_analysis.keys(), analysis.keys())
        for cluster_id in expected_analysis:
            self.assertCountEqual(expected_analysis[cluster_id]["components"], analysis[cluster_id]["components"])
            self.assertAlmostEqual(expected_analysis[cluster_id].get("centers_mean_diff", 0),
                                   analysis[cluster_id].get("centers_mean_diff", 0),
                                   12)
            self.assert_global_stats_almost_equal(expected_analysis[cluster_id]["global"],
                                                  analysis[cluster_id]["global"])

    def assert_global_stats_almost_equal(self, expected, observed):
        for key in ["std", "max", "num_elements", "mean", "overlap"]:
            if key in expected:
                if isinstance(expected[key], float):
                    self.assertAlmostEqual(expected[key], observed[key], 12)
                else:
                    self.assertEqual(expected[key], observed[key])
        for key in expected:
            if isinstance(expected[key], dict):
                self.assert_global_stats_almost_equal(expected[key], observed[key])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_']
    unittest.main()
