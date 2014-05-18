import logging
import itertools
import operator

# Get an instance of a logger
logger = logging.getLogger(__name__)

def most_common(L, top_n):
    """
        helper function to find the most popular elements in a list
    """
    # get an iterable of (item, iterable) pairs
    res = []
    SL = sorted((x, i) for i, x in enumerate(L))
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        res.append((item, count))
        print 'item %r, count %r, minind %r' % (item, count, min_index)
        return count, -min_index
    max(groups, key=_auxfun)[0]
    return res
    sorted_lst = sorted(res, key=lambda tup: tup[1], reverse=True)[:top_n]
    return [i[0] for i in sorted_lst]
