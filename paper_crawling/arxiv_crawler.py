# coding: utf-8
import arxiv
from urllib import urlencode
import logging
import multiprocessing as mp
import os
import google_custom_search
import configparser

# Reference for arxiv python is at https://github.com/lukasschwab/arxiv.py
# Download any paper on arxiv from the title 
# Paper downloaded is stored inside this code's folder


def get_filename(dirname, title):
    return dirname + arxiv.to_slug(title) + ".pdf"


def paper_available_on_arxiv(results):
    return len(results)


def download_from_google(query, my_api_key, my_cse_id, outfile):
    results = google_custom_search.search_google(query,
                                                 my_api_key, my_cse_id, num=10)
    if results:
        google_custom_search.download_link_from_google(results, outfile, query)


def remove_non_ascii(str):
    return ''.join([i if ord(i) < 128 else '' for i in str])


def download_from_arxiv(title, my_api_key, my_cse_id, dirname='./'):
    """Download arxiv paper from the title

    Args:
        title (str): Full title of the paper
        dirname (str): Output directory of the pdf after downloaded

    Returns:
        Filename of the downloaded pdf

    """
    title = '"' + title.replace('-', ' ') + '"'  # Put quote for exact search
    title = remove_non_ascii(title)

    title_prepended = 'ti:' + title
    results = arxiv.query(title_prepended)

    logging.debug(results)
    outfile = get_filename(dirname, title)
    if not os.path.isfile(outfile):
        if paper_available_on_arxiv(results):
            logging.info("Downloading from arxiv: " + title)
            return arxiv.download(results[0], dirname=dirname, slugify=True)    # When slugify is True, the paper title will be stripped of non-alphanumeric characters before being used as a filename.
        else:
            google_query = title + ' filetype:PDF'
            logging.info("Paper is not on arxiv, downloading from google: " + google_query)
            download_from_google(google_query, my_api_key, my_cse_id, outfile)
    else:
        logging.info("Paper has already been downloaded previously. Will skip downloading this file (%s)", title)
        return None


def download_list_of_papers_parallel(titles, my_api_key, my_cse_id, dirname='./'):
    print("There are %d CPUs on this machine" % mp.cpu_count())
    pool = mp.Pool(processes=5)
    filenames = [pool.apply(download_from_arxiv, args=(title, my_api_key, my_cse_id, dirname)) for title in titles]


def download_list_of_papers_serial(titles, my_api_key, my_cse_id, dirname='./'):
    for paper in titles:
        download_from_arxiv(paper, my_api_key, my_cse_id, dirname)


def main():
    logging.getLogger().setLevel(logging.INFO)

    ##### Google Custom Search API Config #####
    config = configparser.ConfigParser()
    config.read('venv/keys.ini')

    my_api_key = config['GOOGLE']['API_KEY']
    my_cse_id = config['GOOGLE']['CSE_ID']
    ###########################################

    # title_positive = 'Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception'  # title must be exact
    # title_negative = 'seaPoT RL Selective Exploration Algorithm for Policy Transfer in RL'
    # title_ambiguous = 'Knowledge-Driven Interpretation of Multi-View Data in Medicine'
    # title = "Autonomous Driving among Many Pedestrians   Models and Algorithms."
    title_nonascii = "Artificial Potential-Based AdaptiveH∞ Synchronized Tracking Control for Accommodation Vessel.(IEEE Trans. Industrial Electronics)"

    download_from_arxiv(title_nonascii, my_api_key, my_cse_id)

if __name__ == '__main__':
    main()


# For debugging purposes
# url_args = urlencode({"search_query": 'ti:"Gaussian Process Decentralized Data Fusion Meets Transfer Learning in Large Scale Distributed Cooperative Perception"',
#                       "id_list": ','.join([]),
#                       "start": 0,
#                       "max_results": 10})
# print url_args
# Working URL: http://export.arxiv.org/api/query?search_query=ti%3A%22Decentralized+High+Dimensional+Bayesian+Optimization+with+Factor+Graphs%22&max_results=10&start=0&id_list=

# http://export.arxiv.org/api/query?search_query=ti%3A%22Autonomous+Driving+among+Many+Pedestrians+++Models+and+Algorithms%22&max_results=10&start=0&id_list=
