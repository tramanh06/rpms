'''
This package calls the dblp REST api to retrieve structured list of
publications given an author name
'''

import dblp
import requests
import json
import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()


def query_dblp_by_author(author):
    # TODO: put check to abort if len(authors) > 2
    author = author.replace(' ', '_')
    url_template = "http://dblp.org/search/publ/api?q=author%3A<AUTHOR_NAME>%3A&format=json"
    query = url_template.replace("<AUTHOR_NAME>", author)
    logging.info('Query dblp API: ' + query)
    response = requests.get(query)
    return response


def query_dblp_for_author_freetext_name(author_name):
    authors = dblp.search(author_name)
    logging.info('Found ' + str(len(authors)) + ' authors:')
    logging.info(', '.join(map(lambda x: str(x), authors)))
    return authors


def print_publication_list(pub_dict):
    for author, publications in pub_dict.items():
        logging.info(" ************* ")
        logging.info(" * AUTHOR: " + author)
        logging.info(" ************* ")
        logging.info(" List of publications")
        for pub in publications:
            logging.info(pub['title'] + "(" + pub['venue'] + ")")


def dblp_crawler(author_name):
    ''' Returns list of dictionary: [{'author': {'publications': 'details'}}]'''

    authors = query_dblp_for_author_freetext_name(author_name)
    logging.info('List of publications:')
    result = {}
    for author in authors:
        response = query_dblp_by_author(str(author))
        if response.ok:
            parsed_json = response.json()
            pubs = [pub['info'] for pub in parsed_json['result']['hits']['hit']]
            result[str(author)] = pubs
    return result

if __name__ == "__main__":
    author_name = 'Bryan Low'
    crawler_result = dblp_crawler(author_name)
    print_publication_list(crawler_result)





