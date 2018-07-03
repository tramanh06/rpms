'''
Author: TramAnh Nguyen 
File Created: Monday, 25th June 2018 9:22:16 am
-----
Last Modified: Monday, 25th June 2018 10:07:50 am
Modified By: TramAnh Nguyen 
-----
'''
import configparser
import glob
import json
import logging
import multiprocessing as mp
import os
from logging.config import fileConfig

import gensim
from tqdm import tqdm

import utils
from paper_crawling import arxiv_crawler, dblp_crawler
from paper_matching import similarity
from pdf2bow import pdf2bow

fileConfig('logging_config.ini')
logger = logging.getLogger()

config = configparser.ConfigParser()
config.read('venv/keys.ini')

my_api_key = config['GOOGLE']['API_KEY']
my_cse_id = config['GOOGLE']['CSE_ID']


def prepare_bow_content(researcher):
    # Look up researcher from dblp to get list of publications
    author_results = dblp_crawler.dblp_crawler(researcher)
    dblp_crawler.print_publication_list(author_results)

    papers_DIR = "papers/" + researcher.replace(" ", "_") + "/"  # Only works when python file is run in the project root location
    bow_DIR = "bow/" + researcher.replace(" ", "_") + "/"

    # Download papers from arxiv, store in papers_DIR="papers/AUTHOR_NAME"
    for author, publications in author_results.items():
        papers = [pub['title'] for pub in publications]

        utils.is_folder_exists_create_otherwise(papers_DIR)

        logging.info("Downloading paper...")
        arxiv_crawler.download_list_of_papers_serial(
            titles=papers,
            dirname=papers_DIR,
            my_api_key=my_api_key,
            my_cse_id=my_cse_id)

    # Run BOW
    pdf2bow.run(input_path=papers_DIR, output_dir=bow_DIR)

    # Concatenate all BOWs
    all_bows = ' '.join([utils.read_file(filename) for filename in glob.glob(bow_DIR + '*.bow')])

    # Return a dictionary
    return {'researcher': researcher, 'bow_content': all_bows}


if __name__ == '__main__':
    # researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu", "Kuldeep S. Meel", "Lee Wee Sun"]
    researchers = ["Leong Tze Yun"]

    researchers_to_bows = [prepare_bow_content(researcher) for researcher in researchers]  # List of dictionary, ie [{researcher: all their papers' bow}]
    # pool = mp.Pool()
    # researchers_to_bows = pool.map(prepare_bow_content, researchers)
    # researchers_to_bows = list(tqdm(pool.imap(prepare_bow_content, researchers)))

    try:
        with open('data.json') as f:
            data = json.load(f)
    except IOError:  # When data.json is not available
        data = []

    researchers = [x["researcher"] for x in data]

    # merge content of data and researchers_to_bow
    data.extend(filter(lambda x: x["researcher"] not in researchers, researchers_to_bows))

    # write data to json file
    with open("data.json", 'wb') as outfile:
        json.dump(data, outfile)
