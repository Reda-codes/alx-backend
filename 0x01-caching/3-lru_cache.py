#!/usr/bin/python3
""" LRUCache module
"""


BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class """
    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            if key in self.cache_data:
                self.cache_data.pop(key)
                self.cache_data[key] = item
            elif (len(self.cache_data) >= BaseCaching.MAX_ITEMS):
                keys = list(self.cache_data.keys())
                removed = keys[-0]
                self.cache_data.pop(removed)
                self.cache_data[key] = item
                print('DISCARD: {}'.format(removed))
            else:
                self.cache_data[key] = item
        return None

    def get(self, key):
        """ Get an item by key
        """
        try:
            item = self.cache_data[key]
            self.cache_data.pop(key)
            self.cache_data[key] = item
            return item
        except KeyError:
            return None
