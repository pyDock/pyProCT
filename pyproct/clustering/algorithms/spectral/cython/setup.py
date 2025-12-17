"""
Created on 26/07/2012

@author: victor
"""
#from distutils.core import setup
#from distutils.extension import Extension
#from Cython.Distutils import build_ext
#import numpy as np
#if __name__ == '__main__': # Comp. with sphynx
#    setup(
#        cmdclass = {'build_ext': build_ext},
#        include_dirs = [np.get_include()],
#        ext_modules = [Extension("spectralTools", ["spectralTools.pyx"],extra_compile_args=["-O3","-ffast-math"])])
#
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent

ext_modules = [
    Extension(
        "pyproct.clustering.algorithms.spectral.cython.spectralTools",
        [str(HERE / "spectralTools.pyx")],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3", "-ffast-math"],
    )
]

setup(
    name="pyproct-spectralTools",
    ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
)

#from setuptools import setup, Extension
#from Cython.Build import cythonize
#import numpy as np
#
#ext_modules = [
#    Extension(
#        "pyproct.clustering.algorithms.spectral.cython.spectralTools",
#        ["spectralTools.pyx"],
#        include_dirs=[np.get_include()],
#        extra_compile_args=["-O3", "-ffast-math"],
#    )
#]
#
#setup(
#    name="pyproct-spectralTools",
#    ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
#)

