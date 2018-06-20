import arxiv
from urllib import urlencode

# Reference for arxiv python is at https://github.com/lukasschwab/arxiv.py

title = '"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large-Scale Distributed Cooperative Perception"' # title must be exact
title = title.replace('-', ' ')
title_prepended = 'ti:'+title
results = arxiv.query(title_prepended)

print results

arxiv.download(results[0], slugify=True)    # When slugify is True, the paper title will be stripped of non-alphanumeric characters before being used as a filename.

# For debugging purposes
# url_args = urlencode({"search_query": 'ti:"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception"',
#                       "id_list": ','.join([]),
#                       "start": 0,
#                       "max_results": 10})
# print url_args
# Working URL: http://export.arxiv.org/api/query?search_query=ti%3A%22Decentralized+High+Dimensional+Bayesian+Optimization+with+Factor+Graphs%22&max_results=10&start=0&id_list=
