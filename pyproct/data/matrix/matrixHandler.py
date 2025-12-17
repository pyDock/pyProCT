#"""
#Created on 13/02/2013
#
#@author: victor
#"""
##from pyRMSD.matrixHandler import MatrixHandler as pyRMSD_MatrixHandler
#
##class MatrixHandler(object):
##    
##    def __init__(self, distance_matrix, matrix_params):
##        """
##        Class constructor.
##        
##        :param distance_matrix: The distance matrix to handle.
##        
##        :param matrix_parameters: The parameters used to build this matrix.
##        """
##        self.matrix_parameters = matrix_params
##
##        self.distance_matrix = distance_matrix
##
##    def save_matrix(self, matrix_path):
##        """
##        Writes matrix contents to disk.
##
##        @param matrix_save_file: Complete path (with filename) where to save the matrix.
##        """
##        pyRMSD_MatrixHandler.save_matrix(matrix_path, self.distance_matrix)
##
##    def save_statistics(self, matrix_base_path):
##        """
##        Writes matrix statistics to disk in JSON format.
##
##        @param matrix_base_path: The folder where to save the 'statistics.json' file.
##        """
##        return pyRMSD_MatrixHandler.save_statistics(matrix_base_path, self.distance_matrix)
#    
#import numpy as np
#import os
#import json
#
#class MatrixHandler(object):
#    """
#    Handles condensed distance matrices (numpy 1D array).
#    Replaces pyRMSD MatrixHandler completely.
#    """
#
#    def __init__(self, distance_matrix, matrix_params):
#        """
#        :param distance_matrix: A condensed distance matrix (1D numpy array or list)
#        :param matrix_params: Parameters used to build the matrix
#        """
#        self.matrix_parameters = matrix_params
#        self.distance_matrix = np.array(distance_matrix, dtype=float)
#
#    # -------------------------------------------------------------
#    # Saving utilities
#    # -------------------------------------------------------------
#    def save_matrix(self, matrix_path):
#        """
#        Saves the condensed matrix to a .npy binary file.
#        """
#        np.save(matrix_path, self.distance_matrix)
#        return matrix_path
#
#    def save_statistics(self, matrix_base_path):
#        """
#        Saves simple matrix statistics in JSON format.
#
#        :param matrix_base_path: Folder where 'statistics.json' will be written
#        """
#        stats = {
#            "mean": float(np.mean(self.distance_matrix)),
#            "std":  float(np.std(self.distance_matrix)),
#            "min":  float(np.min(self.distance_matrix)),
#            "max":  float(np.max(self.distance_matrix)),
#            "count": int(self.distance_matrix.size)
#        }
#
#        stats_path = os.path.join(matrix_base_path, "statistics.json")
#        with open(stats_path, "w") as fh:
#            json.dump(stats, fh, indent=4)
#
#        return stats_path
#
#    # -------------------------------------------------------------
#    # Accessor
#    # -------------------------------------------------------------
#    def get_matrix(self):
#        return self.distance_matrix

import json
import os
from pyproct.driver.parameters import ProtocolParameters

class MatrixHandler:

    def __init__(self, distance_matrix, matrix_params):
        """
        distance_matrix: CondensedMatrix instance (NOT a numpy array)
        matrix_params: parameters used to generate the matrix
        """
        self.matrix_parameters = matrix_params
        self.distance_matrix = distance_matrix  # store CondensedMatrix directly

    def save_matrix(self, matrix_path):
        """
        Writes condensed matrix to disk.
        """
        data = self.distance_matrix.get_data()

        os.makedirs(os.path.dirname(matrix_path), exist_ok=True)

        with open(matrix_path, "w") as f:
            for value in data:
                f.write(f"{float(value)}\n")

        return matrix_path

    def save_statistics(self, matrix_base_path):
        """
        Writes matrix statistics to a JSON file.
        """
        data = self.distance_matrix.get_data()
    
        # flatten matrix parameters (remove ProtocolParameters objects)
        clean_params = ProtocolParameters.to_dict(self.matrix_parameters)
    
        stats = {
            "min": float(data.min()),
            "max": float(data.max()),
            "mean": float(data.mean()),
            "std": float(data.std()),
            "size": int(len(data)),
            "elements": int(self.distance_matrix.row_length),
            "parameters": clean_params
        }
    
        os.makedirs(matrix_base_path, exist_ok=True)
    
        out_file = os.path.join(matrix_base_path, "statistics.json")
        with open(out_file, "w") as fp:
            json.dump(stats, fp, indent=4)
    
        return out_file

   # def save_statistics(self, matrix_base_path):
   #     """
   #     Writes matrix statistics to a JSON file.
   #     Computes simple stats: min, max, mean, std.
   #     """
   #     data = self.distance_matrix.get_data()

   #     stats = {
   #         "min": float(data.min()),
   #         "max": float(data.max()),
   #         "mean": float(data.mean()),
   #         "std": float(data.std()),
   #         "size": int(len(data)),
   #         "elements": int(self.distance_matrix.row_length),
   #         "parameters": self.matrix_parameters.params_dic
   #     }

   #     os.makedirs(matrix_base_path, exist_ok=True)

   #     out_file = os.path.join(matrix_base_path, "statistics.json")
   #     with open(out_file, "w") as fp:
   #         json.dump(stats, fp, indent=4)

   #     return out_file

