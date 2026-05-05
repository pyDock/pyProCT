"""
Regression tests for the Python 3 driver/scheduler workflow contract.
"""
import json
import os
import shutil
import tempfile
import unittest

_MPLCONFIGDIR = None
if "MPLCONFIGDIR" not in os.environ:
    _MPLCONFIGDIR = tempfile.mkdtemp(prefix="pyproct_mpl_")
    os.environ["MPLCONFIGDIR"] = _MPLCONFIGDIR

import numpy

from pyproct.data.matrix.condensedMatrix import CondensedMatrix
from pyproct.data.matrix.matrixHandler import MatrixHandler
from pyproct.driver.driver import Driver
from pyproct.driver.observer.observer import Observer
from pyproct.driver.parameters import ProtocolParameters
from pyproct.driver.scheduling.tools import build_scheduler


def tearDownModule():
    if _MPLCONFIGDIR is not None:
        shutil.rmtree(_MPLCONFIGDIR, ignore_errors=True)


def return_value(value):
    return value


class TestDriverWorkflowCompatibility(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="pyproct_driver_test_")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_serial_scheduler_add_task_dependency_order(self):
        scheduler = build_scheduler({"scheduler_type": "Serial"}, Observer())

        scheduler.add_task(
            task_name="task_b",
            dependencies=["task_a"],
            target_function=return_value,
            function_kwargs={"value": "B"},
            description="Depends on task A"
        )
        scheduler.add_task(
            task_name="task_a",
            dependencies=[],
            target_function=return_value,
            function_kwargs={"value": "A"},
            description="Runs first"
        )

        self.assertEqual(scheduler.run(), ["A", "B"])

    def test_validation_bidimensional_loaded_matrix_serial_workflow(self):
        features_path = os.path.join(self.tmpdir, "features.txt")
        matrix_path = os.path.join(self.tmpdir, "distances")
        workspace = os.path.join(self.tmpdir, "workspace")

        numpy.savetxt(
            features_path,
            numpy.array([[0.0, 0.0], [0.5, 0.0], [0.0, 0.5], [0.5, 0.5]])
        )
        MatrixHandler(CondensedMatrix([1.0, 1.2, 1.4, 1.1, 1.3, 1.5])).save_matrix(matrix_path)

        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        base_script_path = os.path.join(repo_root, "validation", "bidimensional", "base_script.json")
        with open(base_script_path, "r") as handler:
            base_script = handler.read()
        parameters = ProtocolParameters.get_params_from_json(base_script % (workspace, matrix_path))

        parameters["data"]["type"] = "features::array"
        parameters["data"]["files"] = [features_path]
        parameters["clustering"]["algorithms"] = {
            "gromos": {
                "parameters": [{"cutoff": 2.0}]
            }
        }
        parameters["clustering"]["evaluation"]["minimum_clusters"] = 1
        parameters["clustering"]["evaluation"]["maximum_clusters"] = 4
        parameters["clustering"]["evaluation"]["minimum_cluster_size"] = 1
        parameters["clustering"]["evaluation"]["maximum_noise"] = 100
        parameters["clustering"]["evaluation"]["evaluation_criteria"] = {
            "default": {
                "Cohesion": {
                    "weight": 1,
                    "action": ">"
                }
            }
        }

        best_clustering = Driver(Observer()).run(parameters)
        results_path = os.path.join(workspace, "results", "results.json")
        with open(results_path, "r") as handler:
            results = json.loads(handler.read())
        best_id = results["best_clustering"]
        best_result = results["selected"][best_id]

        self.assertEqual(best_id, "clustering_0000")
        self.assertEqual(best_result["type"], "gromos")
        self.assertEqual(best_result["evaluation"]["Number of clusters"], 1)
        self.assertEqual(best_result["evaluation"]["Noise level"], 0.0)
        self.assertEqual(best_result["evaluation"]["Cohesion"], 0.0)
        self.assertEqual(best_clustering["type"], "gromos")


if __name__ == "__main__":
    unittest.main()
