'''
Author: TramAnh Nguyen 
File Created: Monday, 25th June 2018 9:22:16 am

Read pdf from /papers and parse into .txt files under /bow folder

For each pdf file, 2 things will be produced:
- raw txt file verbatim from pdf2txt function
- a .bow file that stores words after stemming and preprocessing
'''
import glob
import json
import logging
import multiprocessing as mp
import os

import gensim
from tqdm import tqdm

import utils
from paper_crawling import arxiv_crawler, dblp_crawler
from paper_matching import similarity
from pdf2bow import pdf2bow
import configparser

def prepare_bow_content(pdf_DIR, bow_DIR):
    # Run BOW
    pdf2bow.run(input_path=pdf_DIR, output_dir=bow_DIR)

    # Concatenate all BOWs
    all_bows = [utils.read_file(filename) for filename in glob.glob(bow_DIR + '*.bow')]

    return all_bows


if __name__ == '__main__':
    # researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu", "Kuldeep S. Meel", "Lee Wee Sun"]
    papers_DIR = "papers/"
    bow_DIR = "bow/"
    master_output_file = 'data.json'
    config = configparser.ConfigParser()
    config.read('config.ini')

    researchers_to_bows = []
    papers = []

    for author in os.listdir(papers_DIR):
        papers_sub_dir = os.path.join(papers_DIR, author, "")
        if os.path.isdir(papers_sub_dir) and os.listdir(papers_sub_dir):
            bow_sub_DIR = os.path.join(bow_DIR, author, "")
            all_texts = prepare_bow_content(papers_sub_dir, bow_sub_DIR)

            # Persist to intermediate file under subfolder
            outfile_location = os.path.join(bow_sub_DIR, "_.json")
            content = {author: ' '.join(all_texts)}

            utils.write_to_json_file(file_location=outfile_location, data=content)

            # Add to master list
            researchers_to_bows.append({'researcher': author, 'bow_content': ' '.join(all_texts)})
            papers.extend(all_texts)

    RESET_BOW = config['PREPROCESSING'].getboolean('RESET_BOW')

    try:
        if RESET_BOW:
            data = []
        else:
            data = utils.read_json_file(master_output_file)
    except IOError:  # When data.json is not available
        data = []

    existing_researchers = [x["researcher"] for x in data]

    # merge content of data and researchers_to_bow
    data.extend(filter(lambda x: x["researcher"] not in existing_researchers, researchers_to_bows))

    # write data to json file
    utils.write_to_json_file(file_location=master_output_file, data=data)
    utils.write_to_json_file(file_location="papers.json", data=papers)
