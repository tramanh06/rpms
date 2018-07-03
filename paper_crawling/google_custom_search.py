from googleapiclient.discovery import build
import pprint
import urllib
import os
import configparser
import logging


def google_search(search_term, api_key, cse_id, **kwargs):
    """Search query from google API.

    Args:
        search_term (str): string of query 
        api_key: API key provided by Google Cloud
        cse_id: Custom Search Engine ID provided by Google Cloud

    Returns:
        List of results. Each element is one search result item.
        If no results returned, return None.

    """

    service = build("customsearch", "v1", developerKey=api_key, cache_discovery=False)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if res['searchInformation']['totalResults'] == '0':
        logging.error("Could not find pdf version on Google. Search term: %s", search_term)
        return None
    return res['items']


def download_link_from_google(results, outfile):
    """Iterate through results to download the relevant file. 
    Ignore files that are less than 10Kb.

    Args:
        results (list): list of results returned by Google Custom Search API
        outfile (string): filename and directory of the downloaded file

    Returns:
        Boolean. True if file can be found and downloaded. False otherwise.
        
    """
    for result in results:
        pdf_url = result['link']
        logging.info("Downloading paper %s from url: %s", outfile, pdf_url)
        urllib.urlretrieve(pdf_url, outfile)
        if os.path.getsize(outfile) > 10000:
            return True
            break

    logging.error("Cannot find downloadable pdf file on Google.")
    return False


def main():
    config = configparser.ConfigParser()
    config.read('venv/keys.ini')

    my_api_key = config['GOOGLE']['API_KEY']
    my_cse_id = config['GOOGLE']['CSE_ID']

    results = google_search(
        '"SEAPoT RL   Selective Exploration Algorithm for Policy Transfer in RL"' + ' filetype:PDF', 
        my_api_key, my_cse_id, num=10)

    if results:
        downloaded_pdf = "abc.pdf"
        download_link_from_google(results, downloaded_pdf)


if __name__ == '__main__':
    main()
