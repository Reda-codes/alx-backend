#!/usr/bin/env python3
'''
function named index_range that takes two integer arguments page and page_size.
'''
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    ''' index_range function '''
    if page == 1:
        return (0, page_size)
    else:
        start = page_size * (page - 1)
        return (start, start + page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        ''' method to get the requested data '''
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        data = self.dataset()
        index = index_range(page, page_size)
        return data[index[0]:index[1]]

    def get_hyper(self, page: int = 1, page_size: int = 10):
        ''' method to get the requested data with more details '''
        index = index_range(page, page_size)
        data = self.get_page(page, page_size)
        sizePage = len(data)

        nextPage = page + 1 if index[1] < len(self.dataset()) else None
        prevPage = page - 1 if index[0] > 0 else None
        totalPages = round(len(self.dataset())/page_size)

        return {
                    'page_size': sizePage,
                    'page': page,
                    'data': data,
                    'next_page': nextPage,
                    'prev_page': prevPage,
                    'total_pages': totalPages
                }
