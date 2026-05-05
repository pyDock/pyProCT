"""
Created on 07/02/2013

@author: victor
"""
import unittest
import os
from pyproct.driver.parameters import ProtocolParameters
from pyproct.data.matrix.condensedMatrix import CondensedMatrix
import pyproct.clustering.algorithms.gromos.parametersGeneration as gromosParametersGeneration
import pyproct.clustering.algorithms.kmedoids.parametersGeneration as kmedoidsParametersGeneration
import pyproct.clustering.algorithms.random.parametersGeneration as randomParametersGeneration

class MatrixHandlerMock:
    def __init__(self, matrix):
        self.distance_matrix = matrix

class MatrixMock:
    def __init__(self):
        self.row_length = 2000
    
    def calculateMean(self):
        return 2.5
    
    def calculateMax(self):
        return 4.0

@unittest.skip("Legacy algorithm parameter generation expectations need a dedicated generator block.")
class TestParameterGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        params_path = os.path.join(os.path.dirname(__file__), "data", "params.json")
        cls.parameters = ProtocolParameters.get_default_params(params_path)
        distances = [94, 6, 43, 14, 96,
                        18, 59, 54, 69,
                            56, 96, 69,
                                54, 50,
                                     8]
        cls.matrix_1 = CondensedMatrix(distances)

    def test_get_gromos_parameters(self):
        expected = ([{'cutoff': 8.15},
                    {'cutoff': 16.3},
                    {'cutoff': 24.45},
                    {'cutoff': 32.6},
                    {'cutoff': 40.75},
                    {'cutoff': 48.9},
                    {'cutoff': 57.05},
                    {'cutoff': 65.2},
                    {'cutoff': 73.35},
                    {'cutoff': 81.5},
                    {'cutoff': 89.65}], [])
        
        parametersGenerator = gromosParametersGeneration.ParametersGenerator(self.parameters, 
                                                                             MatrixHandlerMock(self.matrix_1))
        parameters = parametersGenerator.get_parameters()[0]
        for i in  range(len(parameters)):
            self.assertAlmostEqual(parameters[i]["cutoff"], expected[0][i]["cutoff"]) 

    @unittest.skip("Spectral parameter generation belongs to the pending spectral block.")
    def test_get_spectral_parameters(self):
        import pyproct.clustering.algorithms.spectral.parametersGeneration as spectralParametersGeneration
        expected = ([{'k': 10, 'use_k_medoids': True}, 
                     {'k': 12, 'use_k_medoids': True}, 
                     {'k': 14, 'use_k_medoids': True}, 
                     {'k': 16, 'use_k_medoids': True}, 
                     {'k': 18, 'use_k_medoids': True}, 
                     {'k': 20, 'use_k_medoids': True}, 
                     {'k': 22, 'use_k_medoids': True}, 
                     {'k': 24, 'use_k_medoids': True}, 
                     {'k': 26, 'use_k_medoids': True}, 
                     {'k': 28, 'use_k_medoids': True},
                     {'k': 30, 'use_k_medoids': True}], [])
        
        parametersGenerator = spectralParametersGeneration.ParametersGenerator(self.parameters, 
                                                                             MatrixHandlerMock(MatrixMock()))
        self.assertCountEqual(expected,parametersGenerator.get_parameters())
     
    def test_get_kmedoids_parameters(self):
        expected = ([{'seeding_type': 'EQUIDISTANT', 'k': 10, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 12, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 14, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 16, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 18, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 20, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 22, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 24, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 26, 'seeding_max_cutoff': None}, 
                     {'seeding_type': 'EQUIDISTANT', 'k': 28, 'seeding_max_cutoff': None},
                     {'seeding_type': 'EQUIDISTANT', 'k': 30, 'seeding_max_cutoff': None}], [])
        
        parametersGenerator = kmedoidsParametersGeneration.ParametersGenerator(self.parameters, 
                                                                             MatrixHandlerMock(MatrixMock()))
        self.assertCountEqual(expected, parametersGenerator.get_parameters())
     
    def test_get_random_parameters(self):
        expected = ([{'num_clusters': 10}, 
                     {'num_clusters': 12}, 
                     {'num_clusters': 14}, 
                     {'num_clusters': 16}, 
                     {'num_clusters': 18}, 
                     {'num_clusters': 20}, 
                     {'num_clusters': 22}, 
                     {'num_clusters': 24}, 
                     {'num_clusters': 26}, 
                     {'num_clusters': 28},
                     {'num_clusters': 30}], [])

        parametersGenerator = randomParametersGeneration.ParametersGenerator(self.parameters, 
                                                                             MatrixHandlerMock(MatrixMock()))
        self.assertCountEqual(expected, parametersGenerator.get_parameters())
    
    ## get_hierarchical_parameters and get_dbscan_parameters depend on functions that have been tested apart.
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
