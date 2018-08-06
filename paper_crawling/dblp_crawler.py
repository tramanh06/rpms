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
    author = author.replace(' ', '_')
    url_template = "http://dblp.org/search/publ/api?q=author%3A<AUTHOR_NAME>%3A&format=json"
    query = url_template.replace("<AUTHOR_NAME>", author)
    logging.info('Query dblp API: ' + query)
    response = requests.get(query)
    return response


def query_dblp_for_author_freetext_name(author_name):
    authors = dblp.search(author_name)
    logging.info('Found %s authors for %s:', str(len(authors)), author_name)
    logging.info(get_list_of_authors(authors))

    if len(authors) > 2:
        logging.warn("Too many authors found for %s. Complete list found by dblp: %s",
                     author_name,
                     get_list_of_authors(authors))
        logging.warn("Going to pick the exact name: %s", author_name)
        return [author_name]

    return authors


def get_list_of_authors(authors):
    return ', '.join(map(lambda x: str(x), authors))


def print_publication_list(pub_dict):
    for author, publications in pub_dict.items():
        logging.info(" ************* ")
        logging.info(" * AUTHOR: " + author)
        logging.info(" ************* ")
        logging.info(" List of publications")
        for pub in publications:

            logging.info(pub['title'] + "(" + str(pub['venue']) + ")")


def dblp_crawler(author_name):
    """Find author's record by hitting dblp API

    Args:
        author_name (str): Full name of the author

    Returns:
        List of dictionary: [{'author': {'publications': 'details'}}]
        
    """
    authors = query_dblp_for_author_freetext_name(author_name)
    logging.info('List of publications:')
    result = {}
    for author in authors:
        response = query_dblp_by_author(str(author))
        if response.ok:
            parsed_json = response.json()
            pubs = [pub['info'] for pub in parsed_json['result']['hits']['hit']]
            if len(pubs) > 2:   # Filter out author's version that has 1 or 2 publications
                result[str(author)] = pubs
    return result

if __name__ == "__main__":
    # author_name = 'Bryan Low'
    author_name = 'David Hsu'
    crawler_result = dblp_crawler(author_name)
    print_publication_list(crawler_result)





