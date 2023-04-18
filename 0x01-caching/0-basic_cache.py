#!/usr/bin/python3
""" BasicCache module
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ BasicCache class """
    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        try:
            item = self.cache_data[key]
            return item
        except KeyError:
            return None
