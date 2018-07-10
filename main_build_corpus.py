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

    researchers_to_bows = []
    for o in os.listdir(papers_DIR):
        papers_sub_dir = os.path.join(papers_DIR, o, "")
        if os.path.isdir(papers_sub_dir):
            bow_sub_DIR = os.path.join(bow_DIR, o, "")
            all_texts = prepare_bow_content(papers_sub_dir, bow_sub_DIR)
            utils.write_to_file(bow_sub_DIR + "bow.txt", all_texts)
            researchers_to_bows.append({'researcher': o, 'bow_content': all_texts})

    # pool = mp.Pool()
    # researchers_to_bows = pool.map(prepare_bow_content, researchers)
    # researchers_to_bows = list(tqdm(pool.imap(prepare_bow_content, researchers)))

    try:
        with open('data.json') as f:
            data = json.load(f)
    except IOError:  # When data.json is not available
        data = []

    existing_researchers = [x["researcher"] for x in data]

    # merge content of data and researchers_to_bow
    data.extend(filter(lambda x: x["researcher"] not in existing_researchers, researchers_to_bows))

    # write data to json file
    with open("data.json", 'wb') as outfile:
        json.dump(data, outfile)
