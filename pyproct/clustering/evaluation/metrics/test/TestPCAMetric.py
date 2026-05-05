"""
Created on 20/12/2012

@author: victor
"""
import unittest
import numpy
import prody

from pyproct.tools.test.data.amber_short_ca import amber_short_ca_contents
from pyproct.clustering.cluster import Cluster
from pyproct.clustering.clustering import Clustering
import os
from pyproct.clustering.evaluation.metrics.pcaMetrics import PCAMetric

class TrajectoryHandlerStub:
    def __init__(self, coords, apc):
        self.coordinates = coords
        self.atoms_per_conformation = apc

    def getFittingCoordinates(self):
        return self.coordinates
            
    def getCalculationCoordinates(self):
        return None

    def get_data(self):
        return self
    
class testPCAMetric(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate and read the pdb
        cls.pdb_path = "tmp_pdb.pdb"
        with open(cls.pdb_path,"w") as pdb_handler:
            pdb_handler.write(amber_short_ca_contents)
        try:
            prody.confProDy(verbosity='none')#setVerbosity('none')
        except Exception :
            print("Impossible to silent prody") 
        cls.pdb = prody.parsePDB(cls.pdb_path, subset='calpha')
        
        # Save coordsets before superposition
        cls.not_iterposed_coordsets = numpy.array(cls.pdb.getCoordsets())
        
        # Do Prody iterposition
        cls.ensemble = prody.Ensemble('pca_test_ensemble')
        cls.ensemble.setCoords( cls.pdb.getCoords())
        cls.ensemble.addCoordset(cls.pdb.getCoordsets())
        #prody.setVerbosity('info')
        cls.ensemble.iterpose()
        cls.coordsets = cls.ensemble.getCoordsets()
        
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.pdb_path)
        
    def test_covariance_matrix_vs_prody(self):
        # do it with PCA metric
        my_cov_matrix = PCAMetric.create_covariance_matrix(testPCAMetric.coordsets)
         
        # Do it with prody
        pca = prody.PCA('pcametric_pca')
        pca.buildCovariance(testPCAMetric.ensemble)
        prody_cov_matrix = pca._cov
         
        # Compare
        numpy.testing.assert_almost_equal(my_cov_matrix, prody_cov_matrix,10)
     
    def test_eigenvalues(self):
        # do it with PCA metric
        my_cov_matrix = PCAMetric.create_covariance_matrix(testPCAMetric.coordsets)
        biggest_eigenvalue = PCAMetric.calculate_biggest_eigenvalue(my_cov_matrix)
         
        # Do it with prody
        pca = prody.PCA('pcametric_pca')
        pca.buildCovariance(testPCAMetric.ensemble)
        pca.calcModes(n_modes=1)
        self.assertAlmostEqual(pca.getEigvals()[0], biggest_eigenvalue,10)
         
    def test_PCA(self):
        """
        Regression test.
        """
        trajectory_handler = TrajectoryHandlerStub(testPCAMetric.not_iterposed_coordsets,66)
        clustering = Clustering([Cluster(None,list(range(6))),Cluster(None,list(range(6,12)))], "a clustering")
        pcaMetric = PCAMetric(trajectory_handler)
        self.assertAlmostEqual(pcaMetric.evaluate(clustering), 1.4305370646743, 12)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
