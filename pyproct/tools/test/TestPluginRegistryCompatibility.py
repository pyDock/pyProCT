"""
Checks for Python 3 plugin registry compatibility with the original pyProCT
source discovery behavior.
"""
import json
import os
import unittest

from pyproct.data.handler.dataHandler import DataHandler
from pyproct.data.matrix.matrixCalculator import MatrixCalculator
from pyproct.tools.plugins import PluginHandler


class TestPluginRegistryCompatibility(unittest.TestCase):

    def get_registry(self, root_package, selection_keyword, skip_list,
                     plugin_name, attribute):
        classes = PluginHandler.get_classes(root_package,
                                            selection_keyword=selection_keyword,
                                            skip_list=skip_list,
                                            plugin_name=plugin_name)
        registry = {}
        for registry_class in classes:
            key = getattr(registry_class, attribute, None)
            path = "%s.%s" % (registry_class.__module__,
                              registry_class.__name__)
            registry.setdefault(key, set()).add(path)
        return registry

    def test_matrix_calculator_plugins_are_discoverable(self):
        registry = self.get_registry("pyproct.data.matrix",
                                     "MatrixCalculator",
                                     ["test", "cases"],
                                     "matrix",
                                     "CALCULATION_METHOD")

        self.assertIn("matrix::load", registry)
        self.assertIn("matrix::combination", registry)
        self.assertIn("array::euclidean", registry)
        self.assertIn("euclidean_distance::ensemble", registry)
        self.assertIn("rmsd::ensemble", registry)

    def test_data_loader_plugins_are_discoverable(self):
        registry = self.get_registry("pyproct.data.handler",
                                     "DataLoader",
                                     ["test"],
                                     "data_loader",
                                     "LOADER_TYPE")

        self.assertIn("protein::ensemble", registry)
        self.assertIn("features::array", registry)

    def test_data_handler_uses_plugin_loader_registry(self):
        data_handler = DataHandler.__new__(DataHandler)

        protein_loader = data_handler.get_loader("protein::ensemble")
        self.assertEqual("ProteinEnsembleDataLoader", protein_loader.__name__)

        feature_loader = data_handler.get_loader("features::array")
        self.assertEqual("FeatureArrayDataLoader", feature_loader.__name__)

    def test_importable_postprocess_actions_are_discoverable(self):
        registry = self.get_registry("pyproct.postprocess.actions",
                                     "PostAction",
                                     ["test"],
                                     "postprocess",
                                     "KEYWORD")

        self.assertIn("atomic_distances", registry)
        self.assertIn("centers_and_trace", registry)
        self.assertIn("cluster_stats", registry)
        self.assertIn("clusters", registry)
        self.assertIn("compression", registry)
        self.assertIn("conformational_space_comparison", registry)
        self.assertIn("kullback_liebler", registry)
        self.assertIn("protein_dihedral_2D_plot", registry)
        self.assertIn("representatives", registry)

    def test_validation_bidimensional_matrix_methods_resolve(self):
        validation_script = os.path.join("validation", "bidimensional",
                                         "base_script.json")
        with open(validation_script) as handler:
            parameters = json.load(handler)

        self.assertEqual("load", parameters["data"]["matrix"]["method"])

        load_calculator = MatrixCalculator.get_calculator(
            parameters["data"]["matrix"])
        matrix_load_calculator = MatrixCalculator.get_calculator(
            {"method": "matrix::load"})

        self.assertIs(load_calculator, matrix_load_calculator)


if __name__ == "__main__":
    unittest.main()
