import arxiv
from urllib import urlencode
import logging

# Reference for arxiv python is at https://github.com/lukasschwab/arxiv.py
# Download any paper on arxiv from the title 
# Paper downloaded is stored inside this code's folder


def download_from_arxiv(title, dirname='./'):
    title = title.replace('-', ' ')
    title_prepended = 'ti:' + title
    results = arxiv.query(title_prepended)

    logging.debug(results)

    logging.info("Downloading " + title)
    arxiv.download(results[0], dirname=dirname, slugify=True)    # When slugify is True, the paper title will be stripped of non-alphanumeric characters before being used as a filename.


def download_list_of_papers(titles, dirname='./'):
    for paper in titles:
        download_from_arxiv(paper, dirname)


def main():
    title = '"Multi-robot active sensing of non-stationary gaussian process-based environmental phenomena"'  # title must be exact
    
    download_from_arxiv(title)

if __name__ == '__main__':
    main()


# For debugging purposes
# url_args = urlencode({"search_query": 'ti:"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception"',
#                       "id_list": ','.join([]),
#                       "start": 0,
#                       "max_results": 10})
# print url_args
# Working URL: http://export.arxiv.org/api/query?search_query=ti%3A%22Decentralized+High+Dimensional+Bayesian+Optimization+with+Factor+Graphs%22&max_results=10&start=0&id_list=
