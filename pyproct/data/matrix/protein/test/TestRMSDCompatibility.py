"""
Small RMSD compatibility checks against pyRMSD Python 2 reference values.
"""
import unittest

import numpy

from pyRMSD.RMSDCalculator import RMSDCalculator
from pyproct.data.handler.dataHandler import DataHandler
from pyproct.data.matrix.protein.rmsdMatrixCalculator import RMSDMatrixCalculator
from pyproct.driver.parameters import ProtocolParameters


class TestRMSDCompatibility(unittest.TestCase):

    def test_pairwise_matrix_matches_pyRMSD_reference(self):
        coords = numpy.array([
            [[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]],
            [[10., 10., 5.], [10., 11., 5.], [9., 10., 5.]],
            [[0., 0., 0.], [2., 0., 0.], [0., 2., 0.]],
        ], dtype=numpy.float64)

        expected_qtrfit = numpy.array([
            9.019494489765868e-16,
            0.6666666666666667,
            0.6666666666666669,
        ])
        expected_qcp = numpy.array([
            1.2166747166629524e-08,
            0.6666666666666669,
            0.6666666666666666,
        ])

        qtrfit = RMSDCalculator(
            calculatorType="QTRFIT_SERIAL_CALCULATOR",
            fittingCoordsets=numpy.array(coords, copy=True)
        ).pairwiseRMSDMatrix()
        qcp = RMSDCalculator(
            calculatorType="QCP_SERIAL_CALCULATOR",
            fittingCoordsets=numpy.array(coords, copy=True)
        ).pairwiseRMSDMatrix()

        numpy.testing.assert_allclose(qtrfit, expected_qtrfit, atol=1e-12, rtol=1e-12)
        numpy.testing.assert_allclose(qcp, expected_qcp, atol=1e-7, rtol=1e-7)

    def test_calculation_coordsets_match_pyRMSD_reference(self):
        fitting = numpy.array([
            [[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]],
            [[10., 10., 5.], [10., 11., 5.], [9., 10., 5.]],
            [[0., 0., 0.], [2., 0., 0.], [0., 2., 0.]],
        ], dtype=numpy.float64)
        calculation = numpy.array([
            [[0., 0., 0.], [2., 0., 0.]],
            [[10., 10., 5.], [10., 12., 5.]],
            [[0., 0., 0.], [3., 0., 0.]],
        ], dtype=numpy.float64)
        expected = numpy.array([
            1.0385185452638062e-15,
            0.6236095644623236,
            0.6236095644623237,
        ])

        rmsd = RMSDCalculator(
            calculatorType="QTRFIT_SERIAL_CALCULATOR",
            fittingCoordsets=numpy.array(fitting, copy=True),
            calculationCoordsets=numpy.array(calculation, copy=True)
        ).pairwiseRMSDMatrix()

        numpy.testing.assert_allclose(rmsd, expected, atol=1e-12, rtol=1e-12)

    def test_protein_rmsd_matrix_builder_uses_fitted_rmsd(self):
        import pyproct.data.matrix.protein.test.data as test_data

        path = test_data.__path__[0] + "/3_models.pdb"
        data_params = ProtocolParameters({
            "type": "protein::ensemble",
            "files": [path],
            "matrix": {"parameters": {"fit_selection": "name CA"}}
        })
        data_handler = DataHandler(data_params)
        matrix_params = ProtocolParameters({
            "fit_selection": "name CA",
            "calculator_type": "QTRFIT_SERIAL_CALCULATOR"
        })

        matrix = RMSDMatrixCalculator.calculate(data_handler, matrix_params)
        expected = numpy.array([
            1.2135376,
            1.7320968,
            7.625242,
            1.0422597,
            7.2189245,
            6.8910093,
        ])

        self.assertEqual(matrix.row_length, 4)
        numpy.testing.assert_allclose(matrix.get_data(), expected, atol=1e-6, rtol=1e-7)


if __name__ == "__main__":
    unittest.main()
