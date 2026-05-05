'''
Created on Sep 3, 2014

@author: victor
'''
import copy

class DataSource(object):
    
    def __init__(self, source):
        if isinstance(source, str):
            self.source = {"source": source}
        else:
            self.source = source
    
    def __cmp__(self, other):
        cmp_string = self.__get_cmp_string(other)

        # lexicographical ordering
        if self.source["source"] > cmp_string:
            return 1
        elif self.source["source"] < cmp_string:
            return -1
        else:
            return 0

    def __get_cmp_string(self, other):
        if isinstance(other, str):
            return other
        else:
            return other.source["source"]

    def __eq__(self, other):
        try:
            return self.source["source"] == self.__get_cmp_string(other)
        except Exception:
            return False

    def __lt__(self, other):
        return self.source["source"] < self.__get_cmp_string(other)

    def __gt__(self, other):
        return self.source["source"] > self.__get_cmp_string(other)

    def __hash__(self):
        return hash(self.source["source"])

    def get_path(self):
        return self.source["source"]
    
    def clone(self):
        return DataSource(copy.deepcopy(self.source))

    def add_info(self, key, info):
        self.source[key] = info
    
    def get_info(self, key):
        return self.source[key]
    
    def has_info(self, key):
        return key in self.source
