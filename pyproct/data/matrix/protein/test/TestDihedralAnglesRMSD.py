"""
Created on 08/07/2014

@author: victor
"""
import unittest
from pyproct.data.matrix.protein.test.data.dihedral_angles_pdb_data import pdb1, expected_dihedrals
import pyproct.data.matrix.protein.test.data as test_data
import prody
import io
from pyproct.data.handler.protein.proteinEnsembleData import ProteinEnsembleData
from pyproct.data.matrix.protein.cases.rmsd.dihedralsCase import DihedralRMSDBuilder
from pyproct.tools.mathTools import angular_rmsd as rmsd
import numpy
import os


class Test(unittest.TestCase):

    def test_get_dihedrals(self):
        input = io.StringIO(pdb1)
        pdb_structure = prody.parsePDBStream(input)
        structure_data = ProteinEnsembleData(pdb_structure, [1], [[]], {"fit_selection": "all"})
        dihedrals = structure_data.get_dihedrals_for_conformation(0)
        # We have to get rid off the unknown values!
        numpy.testing.assert_array_almost_equal(numpy.array(expected_dihedrals[1:-1]), numpy.array(dihedrals[2:-2]), 2)

    def test_calc_matrix(self):
        pdb_structure = prody.parsePDB(os.path.join(test_data.__path__[0], "3_models.pdb"))
        structure_data = ProteinEnsembleData(pdb_structure, list(range(1, 5)), [[]] * 4, {"fit_selection": "all"})
        expected = [35.04086448, 47.63790625, 91.43562283, 33.05575908, 89.97637041, 88.62190166]
        product_matrix = DihedralRMSDBuilder.build(structure_data)
#         print "out", product_matrix.get_data()
#         print "out", product_matrix.get_data()
#         print product_matrix.get_data()[0]
#         print product_matrix[0,1]
        numpy.testing.assert_almost_equal(expected, product_matrix.get_data(),8)

    def test_rmsd(self):
        a = [1,2,3,4,5]
        b = [10,20,30,40,50]
        self.assertAlmostEqual(29.8496231132, rmsd(numpy.array(a),numpy.array(b)), 8)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_build']
    unittest.main()
