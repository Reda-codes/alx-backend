#!/usr/bin/python3
""" LFUCache module
"""


BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class """
    frequency = {}

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                LFUCache.frequency[key] += 1
            elif (len(self.cache_data) >= BaseCaching.MAX_ITEMS):
                removed = min(LFUCache.frequency, key=LFUCache.frequency.get)
                self.cache_data.pop(removed)
                LFUCache.frequency.pop(removed)
                self.cache_data[key] = item
                LFUCache.frequency[key] = 1
                print('DISCARD: {}'.format(removed))
            else:
                self.cache_data[key] = item
                LFUCache.frequency[key] = 1
        return None

    def get(self, key):
        """ Get an item by key
        """
        try:
            item = self.cache_data[key]
            self.cache_data[key] = item
            LFUCache.frequency[key] += 1
            return item
        except KeyError:
            return None
