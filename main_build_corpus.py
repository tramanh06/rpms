'''
Author: TramAnh Nguyen 
File Created: Monday, 25th June 2018 9:22:16 am
-----
Last Modified: Monday, 25th June 2018 10:07:50 am
Modified By: TramAnh Nguyen 
-----
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


def prepare_bow_content(pdf_DIR, bow_DIR):
    # Run BOW
    pdf2bow.run(input_path=pdf_DIR, output_dir=bow_DIR)

    # Concatenate all BOWs
    all_bows = ' '.join([utils.read_file(filename) for filename in glob.glob(bow_DIR + '*.bow')])

    return all_bows


if __name__ == '__main__':
    # researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu", "Kuldeep S. Meel", "Lee Wee Sun"]
    papers_DIR = "papers/"
    bow_DIR = "bow/"
    master_output_file = 'data.json'

    researchers_to_bows = []
    for o in os.listdir(papers_DIR):
        papers_sub_dir = os.path.join(papers_DIR, o, "")
        if os.path.isdir(papers_sub_dir):
            bow_sub_DIR = os.path.join(bow_DIR, o, "")
            all_texts = prepare_bow_content(papers_sub_dir, bow_sub_DIR)

            # Persist to intermediate file 
            outfile_location = os.path.join(bow_sub_DIR, "_.json")
            content = {o: all_texts}
            with open(outfile_location, 'wb') as f:
                json.dump(content, f)

            # Add to master list
            researchers_to_bows.append({'researcher': o, 'bow_content': all_texts})

    try:
        with open(master_output_file) as f:
            data = json.load(f)
    except IOError:  # When data.json is not available
        data = []

    existing_researchers = [x["researcher"] for x in data]

    # merge content of data and researchers_to_bow
    data.extend(filter(lambda x: x["researcher"] not in existing_researchers, researchers_to_bows))

    # write data to json file
    with open(master_output_file, 'wb') as outfile:
        json.dump(data, outfile)
