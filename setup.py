"""
Created on 25/02/2013

@author: victor
"""

if __name__ == '__main__': # Compatibility with sphynx
    from setuptools import setup, Extension
    from Cython.Build import cythonize
    import numpy
    import distutils.sysconfig
    import os

    def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

    include_dirs = [numpy.get_include(),
                    distutils.sysconfig.get_python_inc()]

    cython_extensions = [
        Extension(
            'pyproct.clustering.algorithms.dbscan.cython.cythonDbscanTools',
            ['pyproct/clustering/algorithms/dbscan/cython/cythonDbscanTools.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.algorithms.spectral.cython.spectralTools',
            ['pyproct/clustering/algorithms/spectral/cython/spectralTools.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.evaluation.metrics.cython.cohesion',
            ['pyproct/clustering/evaluation/metrics/cython/cohesion.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.evaluation.metrics.cython.silhouette',
            ['pyproct/clustering/evaluation/metrics/cython/silhouette.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.evaluation.metrics.cython.graph.tools',
            ['pyproct/clustering/evaluation/metrics/cython/graph/tools.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.evaluation.metrics.cython.graph.ratioCut',
            ['pyproct/clustering/evaluation/metrics/cython/graph/ratioCut.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.evaluation.metrics.cython.graph.minMaxCut',
            ['pyproct/clustering/evaluation/metrics/cython/graph/minMaxCut.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        ),
        Extension(
            'pyproct.clustering.evaluation.metrics.cython.graph.nCut',
            ['pyproct/clustering/evaluation/metrics/cython/graph/nCut.pyx'],
            include_dirs=include_dirs,
            extra_compile_args=["-O3", "-ffast-math"]
        )
    ]

    setup(
          name='pyProCT',
          version='1.7.3',
          description='pyProCT is an open source cluster analysis software especially adapted for jobs related with structural proteomics',
          author='Victor Alejandro Gil Sepulveda',
          author_email='victor.gil.sepulveda@gmail.com',
          url='https://github.com/victor-gil-sepulveda/pyProCT',
          license = 'LICENSE.txt',
          long_description = read('README.md'),
          long_description_content_type='text/markdown',
          packages=[
                    'pyRMSD',
                    'pyproct',
                    'pyproct.clustering',
                    'pyproct.clustering.algorithms',
                    'pyproct.clustering.algorithms.dbscan',
                    'pyproct.clustering.algorithms.dbscan.cython',
                    'pyproct.clustering.algorithms.gromos',
                    'pyproct.clustering.algorithms.hierarchical',
                    'pyproct.clustering.algorithms.kmedoids',
                    'pyproct.clustering.algorithms.random',
                    'pyproct.clustering.algorithms.spectral',
                    'pyproct.clustering.algorithms.spectral.cython',
                    'pyproct.clustering.evaluation',
                    'pyproct.clustering.evaluation.analysis',
                    'pyproct.clustering.evaluation.metrics',
                    'pyproct.clustering.evaluation.metrics.cython',
                    'pyproct.clustering.evaluation.metrics.cython.graph',
                    'pyproct.clustering.filtering',
                    'pyproct.clustering.protocol',
                    'pyproct.clustering.protocol.exploration',
                    'pyproct.clustering.protocol.refinement',
                    'pyproct.clustering.selection',
                    'pyproct.data',
                    'pyproct.data.handler',
                    'pyproct.data.handler.featurearray',
                    'pyproct.data.handler.protein',
                    'pyproct.data.matrix',
                    'pyproct.data.matrix.featurearray',
                    'pyproct.data.matrix.combination',
                    'pyproct.data.matrix.protein',
                    'pyproct.data.matrix.protein.cases',
                    'pyproct.data.matrix.protein.cases.rmsd',
                    'pyproct.data.matrix.protein.cases.euclidean',
                    'pyproct.driver',
                    'pyproct.driver.observer',
                    'pyproct.driver.results',
                    'pyproct.driver.scheduling',
                    'pyproct.driver.time',
                    'pyproct.driver.workspace',
                    'pyproct.postprocess',
                    'pyproct.postprocess.actions',
                    'pyproct.postprocess.actions.confSpaceComparison',
                    'pyproct.tools'
                    
          ],

          include_dirs = include_dirs,
          ext_modules=cythonize(cython_extensions,
                                compiler_directives={"language_level": "3"}),

          install_requires=[
            #"pyRMSD>=4.0.0",
            #"pyScheduler>=0.1.0",
            "fastcluster>=1.1.6",
            "ProDy>=1.4.2",
            "numpy>=1.6.1",
            "scipy>=0.9.0",
            "scikit-learn>=0.12",
            "Pillow>=2.6.2",
            "matplotlib>=1.1.1rc",
            "mpi4py>=1.3"
          ]
    )
