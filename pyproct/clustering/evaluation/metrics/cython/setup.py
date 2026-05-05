"""
Created on 26/07/2012

@author: victor
"""
from pathlib import Path
from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy as np

HERE = Path(__file__).resolve().parent
PACKAGE = "pyproct.clustering.evaluation.metrics.cython"

if __name__ == '__main__': # Comp. with sphynx
    include_dirs = [np.get_include()]
    setup(
        ext_modules = cythonize([
                       Extension(PACKAGE + ".cohesion", [str(HERE / "cohesion.pyx")], include_dirs=include_dirs, extra_compile_args=["-O3","-ffast-math"]),
                       Extension(PACKAGE + ".silhouette", [str(HERE / "silhouette.pyx")], include_dirs=include_dirs, extra_compile_args=["-O3","-ffast-math"]),
                       Extension(PACKAGE + ".graph.tools", [str(HERE / "graph/tools.pyx")], include_dirs=include_dirs, extra_compile_args=["-O3","-ffast-math"]),
                       Extension(PACKAGE + ".graph.ratioCut", [str(HERE / "graph/ratioCut.pyx")], include_dirs=include_dirs, extra_compile_args=["-O3","-ffast-math"]),
                       Extension(PACKAGE + ".graph.minMaxCut", [str(HERE / "graph/minMaxCut.pyx")], include_dirs=include_dirs, extra_compile_args=["-O3","-ffast-math"]),
                       Extension(PACKAGE + ".graph.nCut", [str(HERE / "graph/nCut.pyx")], include_dirs=include_dirs, extra_compile_args=["-O3","-ffast-math"])
        ], compiler_directives={"language_level": "3"}))
