"""
Created on 7/8/2014

@author: victor
"""
import importlib
import inspect
import pkgutil

try:
    import pkg_resources
except ImportError:
    pkg_resources = None


class PluginHandler(object):

    def __init__(self):
        pass

    @classmethod
    def get_classes(cls, root_package_p, selection_keyword=None, skip_list=None,
                    plugin_name=None, *args, **kwargs):
        """
        Gets all possible plugin classes, from source tree and installed plugins.

        The positional API mirrors the original Python 2 implementation. A few
        keyword fallbacks are accepted so partially migrated call sites using the
        interim Python 3 stub keep working.
        """
        if selection_keyword is None:
            selection_keyword = kwargs.get("selection_keyword",
                                           kwargs.get("class_suffix"))
        if skip_list is None:
            skip_list = kwargs.get("skip_list", [])
        if plugin_name is None:
            plugin_name = kwargs.get("plugin_name")

        available_classes = cls.get_classes_from_source(root_package_p,
                                                        selection_keyword,
                                                        skip_list)
        if plugin_name is not None:
            available_classes.extend(cls.get_classes_from_plugins(plugin_name))
        return available_classes

    @classmethod
    def get_classes_from_source(cls, root_package_p, selection_keyword, skip_list):
        """
        Gets all possible plugin classes from the source tree of a given package.
        """
        classes = []
        try:
            root_package = importlib.import_module(root_package_p)

            for pkg_info in pkgutil.walk_packages(root_package.__path__,
                                                  prefix=root_package_p + '.',
                                                  onerror=lambda x: None):
                pckg_name = pkg_info[1]
                is_module = not pkg_info[2]
                if is_module and not cls.skip_submodule(pckg_name, skip_list):
                    try:
                        module = importlib.import_module(pckg_name)
                        for element_name, obj in inspect.getmembers(module):
                            if selection_keyword in element_name:
                                classes.append(obj)
                    except ImportError:
                        print("Error loading plugin: %s" % pckg_name)
        except ImportError:
            print("Error loading root package: %s" % root_package_p)

        return classes

    @classmethod
    def get_classes_from_plugins(cls, name, entry_point_group="pyproct.plugin"):
        """
        Iterates over available entry points and captures plugin classes.
        """
        classes = []
        if pkg_resources is None:
            return classes

        for plugin_handler in pkg_resources.iter_entry_points(entry_point_group,
                                                              name=name):
            classes.append(plugin_handler.load()())
        return classes

    @classmethod
    def get_class(cls, root_package_p, selection_keyword=None, skip_list=None,
                  plugin_name=None, *args, **kwargs):
        """
        Convenience wrapper kept for compatibility with the interim Python 3 API.
        """
        classes = cls.get_classes(root_package_p, selection_keyword, skip_list,
                                  plugin_name, *args, **kwargs)
        if len(classes) == 0:
            return None
        return classes[0]

    @classmethod
    def skip_submodule(cls, this_module, skip_list):
        """Checks if a module/package must be skipped."""
        if skip_list is None:
            return False
        for submodule in this_module.split("."):
            if submodule in skip_list:
                return True
        return False
