"""
Created on 2/9/2014

@author: victor
"""
from pyproct.data.matrix.matrixHandler import MatrixHandler
from pyproct.tools.plugins import PluginHandler
import traceback


class MatrixCalculator(object):

    CALCULATION_METHOD = "None"  # Hack that allow us to work with matrix combination.

    def __init__(self):
        pass

    @classmethod
    def calculate(cls, data_handler, matrix_params):

        calculator_class = cls.get_calculator(matrix_params)

        try:
            distance_matrix = calculator_class.calculate(
                data_handler,
                matrix_params["parameters"]
            )
        except Exception as e:
            print("[ERROR][Driver::postprocess] Impossible to perform matrix calculation for method: %s"
                  % calculator_class.CALCULATION_METHOD)
            print("Message: %s" % str(e))
            traceback.print_exc()
            exit()

        return MatrixHandler(distance_matrix, matrix_params)

    @classmethod
    def get_calculator(cls, matrix_params):
        """
        Python 3 static registry replacement.
        The original plugin system is disabled, so we manually register calculators.
        """
        # Import here to avoid circular imports
        from pyproct.data.matrix.protein.rmsdMatrixCalculator import RMSDMatrixCalculator
        from pyproct.data.matrix.protein.euclideanMatrixCalculator import EuclideanMatrixCalculator
        from pyproct.data.matrix.loaderMatrixCalculator import LoaderMatrixCalculator

        STATIC_CALCULATORS = {
            "rmsd::ensemble": RMSDMatrixCalculator,
            "rmsd::load": LoaderMatrixCalculator,
            "euclidean_distance::ensemble": EuclideanMatrixCalculator,
        }

        calculation_method = matrix_params["method"]

        if calculation_method not in STATIC_CALCULATORS:
            print(f"[ERROR][MatrixCalculator::calculate] '{calculation_method}' is not a registered matrix calculation method.")
            exit()

        return STATIC_CALCULATORS[calculation_method]

# @classmethod
   # def get_calculator(cls, matrix_params):
   #     # Get all available calculators
   #     available_calculators = PluginHandler.get_classes('pyproct.data.matrix', 
   #                                                       selection_keyword = "MatrixCalculator", 
   #                                                       skip_list = ["test", "cases"],
   #                                                       plugin_name = "matrix")
   #     # Choose the calculator we need
   #     calculation_method = matrix_params["method"]
   #     calculator_classes = [x for x in available_calculators if x.CALCULATION_METHOD == calculation_method]
   #     
   #     if len(calculator_classes) == 0:
   #         print("[ERROR][MatrixCalculator::calculate] %s is not a registered matrix calculation method."%(calculation_method))
   #         exit()
   #     else:
   #         return calculator_classes[0] 
