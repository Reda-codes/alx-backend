#!/usr/bin/env python3
'''
function named index_range that takes two integer arguments page and page_size.
'''


def index_range(page: int, page_size: int) -> tuple:
    ''' index_range function '''
    if page == 1:
        return (0, page_size)
    else:
        start = page_size * (page - 1)
        return (start, start + page_size)
