"""
Created on 13/02/2013

@author: victor
"""
import json
import math
import os

import numpy

from pyproct.data.matrix.condensedMatrix import CondensedMatrix


class MatrixHandler(object):

    def __init__(self, distance_matrix, matrix_params=None):
        """
        Class constructor.

        :param distance_matrix: The distance matrix to handle.
        :param matrix_params: The parameters used to build this matrix.
        """
        self.matrix_parameters = matrix_params
        self.distance_matrix = distance_matrix

    def getMatrix(self):
        return self.distance_matrix

    def saveMatrix(self, matrix_file_without_extension):
        return self.save_matrix(matrix_file_without_extension)

    def loadMatrix(self, matrix_file_without_extension):
        self.distance_matrix = MatrixHandler.load_matrix(matrix_file_without_extension)
        return self.distance_matrix

    def save_matrix(self, matrix_file_without_extension=None):
        """
        Supports both pyProCT wrapper calls and pyRMSD-style class calls:

        - handler.save_matrix(path)
        - MatrixHandler.save_matrix(path, distance_matrix)
        """
        if isinstance(self, MatrixHandler):
            return MatrixHandler._save_matrix(matrix_file_without_extension,
                                              self.distance_matrix)
        return MatrixHandler._save_matrix(self, matrix_file_without_extension)

    def save_statistics(self, matrix_base_path=None):
        """
        Supports both pyProCT wrapper calls and pyRMSD-style class calls:

        - handler.save_statistics(path)
        - MatrixHandler.save_statistics(path, distance_matrix)
        """
        if isinstance(self, MatrixHandler):
            return MatrixHandler._save_statistics(matrix_base_path,
                                                  self.distance_matrix)
        return MatrixHandler._save_statistics(self, matrix_base_path)

    @classmethod
    def _save_matrix(cls, matrix_file_without_extension, distance_matrix):
        folder = os.path.dirname(matrix_file_without_extension)
        if folder:
            os.makedirs(folder, exist_ok=True)
        numpy.save(matrix_file_without_extension, distance_matrix.get_data())

    @classmethod
    def load_matrix(cls, matrix_file_without_extension):
        data = numpy.load(matrix_file_without_extension + ".npy").astype(
            numpy.float64,
            copy=False
        )
        return CondensedMatrix(list(data))

    @classmethod
    def _save_statistics(cls, statistics_folder, distance_matrix):
        if statistics_folder is not None:
            print("Calculating statistics ...")
            os.makedirs(statistics_folder, exist_ok=True)
            stats_dic = {}
            stats_dic["Minimum"] = distance_matrix.calculateMin()
            stats_dic["Maximum"] = distance_matrix.calculateMax()
            stats_dic["Mean"] = distance_matrix.calculateMean()
            stats_dic["Std. Dev."] = math.sqrt(distance_matrix.calculateVariance())
            stats_dic["Skewness"] = distance_matrix.calculateSkewness()
            stats_dic["Kurtosis"] = distance_matrix.calculateKurtosis()
            stats_path = os.path.join(statistics_folder, "statistics.json")
            with open(stats_path, "w") as handler:
                handler.write(json.dumps(stats_dic, indent=4, separators=(',', ': ')))
            return stats_path
        return None
