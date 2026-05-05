"""
Created on 19/04/2012

@author: victor
"""
import random
from pyproct.clustering.cluster import gen_clusters_from_class_list
from pyproct.clustering.clustering import Clustering
from pyproct.clustering.randomTools import py2_shuffle

class FakeDistributionRandomClusteringAlgorithm(object):

    def __init__(self,condensed_matrix,  **kwargs):
        """
        Constructor
        """
        self.condensed_matrix = condensed_matrix

    def perform_clustering(self,kwargs):
        """
        Creates a clustering where the clusters have been created by random selection of
        the elements in the dataset, following a cluster size distribution.
        """
        distribution = kwargs["distribution"]
        num_of_nodes = self.condensed_matrix.row_length
        node_class = []
        next_class = 0
        for d in distribution:
            node_class.extend([next_class]*int((d/100.)*num_of_nodes))
            next_class = next_class + 1
        py2_shuffle(random, node_class)
        clusters = gen_clusters_from_class_list(node_class[0:num_of_nodes])
        return Clustering(clusters, details = "Fake Distribution Random (distribution = "+str(distribution)+")")
