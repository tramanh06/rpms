from googleapiclient.discovery import build
import pprint
import urllib
import os
import configparser
import logging
import PyPDF2
from PyPDF2 import PdfFileReader
import requests
import socket
import ssl 

def search_google(search_term, api_key, cse_id, **kwargs):
    """Search query from google API.

    Args:
        search_term (str): string of query 
        api_key: API key provided by Google Cloud
        cse_id: Custom Search Engine ID provided by Google Cloud

    Returns:
        List of results. Each element is one search result item.
        If no results returned, return None.

    """

    logging.info("Searching Google with search term: %s", search_term)
    service = build("customsearch", "v1", developerKey=api_key, cache_discovery=False)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if res['searchInformation']['totalResults'] == '0':
        logging.error("Google Search returns zero result. Search term: %s", search_term)
        return None
    return res['items']


def get_num_pages(pdf_path):
    with open(pdf_path, 'rb') as pdf:
        try:
            num_pages = PyPDF2.PdfFileReader(pdf).getNumPages()
        except PyPDF2.utils.PdfReadError:
            num_pages = float("inf")  # Arbitrarily large number
    
    return num_pages


def is_valid_pdf(urllib_result, filepath):
    return urllib_result and \
        'content-type' in urllib_result[1] and \
        urllib_result[1]['content-type'] == 'application/pdf' and \
        1 < get_num_pages(filepath) < 50


def download_link_from_google(results, outfile, search_terms):
    """Iterate through results to download the relevant file. 
    Ignore files that are not pdf and are more than 50 pages.

    Args:
        results (list): list of results returned by Google Custom Search API
        outfile (string): filename and directory of the downloaded file

    Returns:
        Boolean. True if file can be found and downloaded. False otherwise.
        
    """

    socket.setdefaulttimeout(30)

    for result in results:
        pdf_url = result['link']
        logging.info("Downloading paper %s from url: %s", outfile, pdf_url)
        try:
            urllib_result = urllib.urlretrieve(pdf_url, outfile, context=ssl._create_unverified_context())
        except IOError as e:
            logging.warn("File takes too long to download. Timeout...")
            urllib_result = None

        if is_valid_pdf(urllib_result, outfile):
            return True
            break

    logging.error("Cannot find valid pdf file on Google for %s", search_terms)
    try:
        os.remove(outfile)
    except OSError as exc:
        if exc.errno == 63:
            logging.error("File name is too long. Ignoring this file.")
        if exc.errno == 2:
            logging.error("File hadn't been created. No need to remove file %s", outfile)
        else:
            raise

    return False


def main():
    logging.getLogger().setLevel(logging.INFO)

    config = configparser.ConfigParser()
    config.read('venv/keys.ini')

    my_api_key = config['GOOGLE']['API_KEY']
    my_cse_id = config['GOOGLE']['CSE_ID']

    # Test for those cases
    # "Concept Based Hybrid Fusion of Multimodal Event Signals" filetype:PDF
    # "Scalable Decision-Theoretic Coordination and Control for Real-time Active Multi-Camera Surveillance" filetype:pdf
    # Supermodular mean squared error minimization for sensor scheduling in optimal Kalman Filtering -- still can't retrieve the nus link for this
    # "Act to See and See to Act POMDP planning for objects search in clutter" filetype:pdf
    search_query = '"Multiway analysis of EEG artifacts based on Block Term Decomposition."' + ' filetype:PDF'
    results = search_google(
        search_query,
        my_api_key, my_cse_id)

    downloaded_pdf = "abc.pdf"
    download_link_from_google(results, downloaded_pdf, search_query)


if __name__ == '__main__':
    main()
