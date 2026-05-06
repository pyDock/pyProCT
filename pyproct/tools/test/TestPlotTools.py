"""
Created on 13/12/2012

@author: victor
"""
import os
import tempfile
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="pyproct_mpl_"))
import unittest
import numpy
import pyproct.tools.plotTools
from pyproct.data.matrix.condensedMatrix import CondensedMatrix

class Test(unittest.TestCase):

    def test_normalize(self):
        test_list = [-3,-2,-1,0,1,2,3]
        rescaled = [-2.0, -1.333, -0.666, 0.0, 0.666, 1.333, 2.0]
        numpy.testing.assert_array_almost_equal(pyproct.tools.plotTools.normalize(test_list, 2), rescaled, 3)
   
    def test_normalize_in_range(self):
        mylist =[255,40,35,2,245]
        norm = pyproct.tools.plotTools.normalize_in_range(mylist,0.3,1)
        numpy.testing.assert_array_almost_equal(norm,[1.0, 0.409, 0.396, 0.305, 0.972],3)
    
    def test_remove_zeros(self):
        mylist = [1,0,1,0,0,0,2,2,0,2,3,4]
        expected = [1,1,2,2,2,3,4]
        numpy.testing.assert_array_almost_equal(pyproct.tools.plotTools.remove_zeros(mylist), expected)
        
    def test_tuple_to_int(self):
        self.assertCountEqual(pyproct.tools.plotTools.tuple_to_int((0.1,0.6,7.3,-3.2)), (0,0,7,-3))
    
    def test_shorten_name(self):
        text = "En un lugar de la mancha de cuyo nombre no quiero acordarme"
        self.assertEqual(pyproct.tools.plotTools.shorten_name(text, max_length = 5), "...darme")
        self.assertEqual(pyproct.tools.plotTools.shorten_name(text), "... acordarme")

    def test_matrix_to_image_creates_file(self):
        matrix = CondensedMatrix(numpy.array([1., 2., 3.]))
        with tempfile.TemporaryDirectory(prefix="pyproct_plot_") as tmpdir:
            output_path = os.path.join(tmpdir, "matrix.png")
            pyproct.tools.plotTools.matrixToImage(matrix, output_path)
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)

    def test_pie_chart_creation_returns_image(self):
        image = pyproct.tools.plotTools.pieChartCreation(
            (240, 160),
            [1, 2, 3],
            "Trajectory A",
            "Trajectory B",
            {"A": "#ff0000", "B": "#00ff00", "M": "#0000ff"}
        )
        self.assertEqual(image.size, (200, 100))
        
    @unittest.skip("TODO legacy test; plot matrix shrinking has no assertion yet.")
    def test_shrink_matrix(self):
        self.fail("TODO")
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
