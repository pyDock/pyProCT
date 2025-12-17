"""
PLUGIN LOADER for Python 3.
Instead of pkg_resources (deprecated and requires entry_points),
we load plugins by importing all known calculator modules manually.
"""

#def load_all_plugins():
#    # Matrix calculators - explicit imports
#    import pyproct.data.matrix.combination.combinationMatrixCalculator
#    import pyproct.data.matrix.featurearray.euclideanMatrixCalculator
#    import pyproct.data.matrix.loaderMatrixCalculator
#    import pyproct.data.matrix.protein.euclideanMatrixCalculator
#    import pyproct.data.matrix.protein.rmsdMatrixCalculator
#load_all_plugins()
def load_all_plugins():
    # Load ONLY the plugins that do NOT require pyRMSD
    import pyproct.data.matrix.protein.rmsdMatrixCalculator
    import pyproct.data.matrix.protein.euclideanMatrixCalculator
    import pyproct.data.matrix.featurearray.euclideanMatrixCalculator
    import pyproct.data.matrix.loaderMatrixCalculator
    # combinationMatrixCalculator uses pyRMSD → do NOT import it

load_all_plugins()
class PluginHandler:
    """
    Stub version for Python3: dynamic plugin loading (pkg_resources)
    is disabled, so this handler simply returns empty lists.
    """

    @staticmethod
    def get_classes(module_root,
                    class_suffix=None,
                    selection_keyword=None,
                    recursive=True,
                    ignore_errors=True):
        # Always return empty list. We now manually register calculators
        if module_root == "pyproct.postprocess.actions":
            actions = []

            def safe_add(import_stmt, clsname):
                try:
                    ns = {}
                    exec(import_stmt, ns, ns)
                    actions.append(ns[clsname])
                except Exception:
                    pass
            
            safe_add("from pyproct.postprocess.actions.representatives import RepresentativesPostAction", "RepresentativesPostAction")
            safe_add("from pyproct.postprocess.actions.clusters import SaveAllClustersPostAction", "SaveAllClustersPostAction")
            safe_add("from pyproct.postprocess.actions.clusterStats import ClusterStatsPostAction", "ClusterStatsPostAction")
            safe_add("from pyproct.postprocess.actions.proteinAtomDistances import AtomicDistancesPostAction", "AtomicDistancesPostAction")
            safe_add("from pyproct.postprocess.actions.redundanceElimination import RedundanceEliminationPostAction", "RedundanceEliminationPostAction")
            safe_add("from pyproct.postprocess.actions.proteinDihedralPlot import proteinDihedralPlotPostAction", "proteinDihedralPlotPostAction")
            safe_add("from pyproct.postprocess.actions.centersAndTrace import CentersAndTracePostAction", "CentersAndTracePostAction")
            safe_add("from pyproct.postprocess.actions.kullbackLiebler import KullbackLieblerPostAction", "KullbackLieblerPostAction")
            
            # confSpaceComparison subpackage
            safe_add("from pyproct.postprocess.actions.confSpaceComparison.confSpaceComparison import ConfSpaceComparisonPostAction", "ConfSpaceComparisonPostAction")
            safe_add("from pyproct.postprocess.actions.confSpaceComparison.confSpaceOverlap import ConfSpaceOverlapPostAction", "ConfSpaceOverlapPostAction")
            
            # ESTA es la conflictiva: solo se añadirá si pyRMSD existe
            safe_add("from pyproct.postprocess.actions.rmsf import RmsfPostAction", "RmsfPostAction")
            
            return actions

        
        return []

    @staticmethod
    def get_class(module_root,
                  class_suffix=None,
                  selection_keyword=None,
                  recursive=True,
                  ignore_errors=True):
        # Return None: no dynamic plugins.
        return None

#"""
#Created on 7/8/2014
#
#@author: victor
#"""
#import pkgutil
#import importlib
#import inspect
#import pkg_resources 
#
#class PluginHandler(object):
#    
#    def __init__(self):
#        pass
#    
#    @classmethod
#    def get_classes(cls, root_package_p, selection_keyword, skip_list, plugin_name):
#        """
#        Gets all possible plugin classes (from source tree and from installed plugins)
#        
#        :param root_package_p: A dot-separated string with the name of the package where 
#        the search is going to be started. Ex: "numpy.testing"
#        
#        :param selection_keyword: A common keyword that the class we want to get has.
#        
#        :param skip_list: A list of module names that if found will not be inspected.
#        Ex. ["test"] will make get_classes ignore "test.mytest", "lots.of.tests" and 
#        "this_is.a.test.in_the.middle".
#        
#        :param plugin_name: The name of the plugin family to be loaded.
#        
#        :return: The list of available classes. 
#        """
#        available_classes = cls.get_classes_from_source(root_package_p, selection_keyword, skip_list)
#        available_classes.extend(cls.get_classes_from_plugins(plugin_name))
#        return available_classes
#    
#    @classmethod
#    def get_classes_from_source(cls, root_package_p, selection_keyword, skip_list):
#        """
#        Gets all possible plugin classes from the source tree of a given package.
#        
#        :param root_package_p: A dot-separated string with the name of the package where \
#        the search is going to be started. \
#            Ex: ``"numpy.testing"``
#        
#        :param selection_keyword: A common keyword that the class we want to get has.
#        
#        :param skip_list: A list of module names that if found will not be inspected.
#        Ex. ["test"] will make get_classes ignore "test.mytest", "lots.of.tests" and 
#        "this_is.a.test.in_the.middle".
#        
#        :return: The list of available classes. 
#        """
#        classes = []
#        try:
#            root_package = importlib.import_module(root_package_p)
#    
#            for pkg_info in pkgutil.walk_packages(root_package.__path__, prefix = root_package_p + '.', onerror=lambda x: None):
#                pckg_name = pkg_info[1]
#                is_module = not pkg_info[2]
#                if is_module and not cls.skip_submodule(pckg_name, skip_list):
#                    module_import_path = pckg_name
#                    try:
#                        module = importlib.import_module(module_import_path)
#                        for element_name, obj in inspect.getmembers(module):
#                            if selection_keyword in element_name:
#                                classes.append(obj)
#                    except ImportError: 
#                        print("Error loading plugin: %s"%(pckg_name))
#        except ImportError:
#            print("Error loading root package: %s"%(root_package_p))
#        
#        return classes
#            
#    @classmethod
#    def get_classes_from_plugins(cls, name, entry_point_group = "pyproct.plugin"):
#        """
#        Iterates over the available entry points and captures the classes
#        that implement the plugin.
#        
#        :param entry_point: The entry point we want to use. By default is "pyproct.plugin",
#        which is the generic plugin entry point for pyproct. This entry point pointers to a
#        that must return 
#        
#        :returns: The list of classes available through plugins. 
#        """
#        classes = []
#        for plugin_handler in pkg_resources.iter_entry_points( entry_point_group, name = name):
#            classes.append(plugin_handler.load()())
#        return classes
#    
#    @classmethod
#    def skip_submodule(cls, this_module, skip_list):
#        """Checks if a module/package must be skipped. A submodule will be skipped if the module
#        or any of its subpackages is inside skip_list.
#        
#        :param this_module: A string with the complete name of the module/package we want to test.\
#        Ex: ``"pyproct.clustering.algorithms".``
#        
#        :param skip_list: A list of packages/module we want to skip.
#    
#        :return: True or False depending if the module/package must be skipped.
#        """
#        for submodule in this_module.split("."):
#            if submodule in skip_list:
#                return True
#        return False
#    
