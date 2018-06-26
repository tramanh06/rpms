'''
Author: TramAnh Nguyen 
File Created: Monday, 25th June 2018 9:22:16 am
-----
Last Modified: Monday, 25th June 2018 10:07:50 am
Modified By: TramAnh Nguyen 
-----
'''
import glob
import logging
import os
from logging.config import fileConfig

import gensim

import utils
from paper_crawling import arxiv_crawler, dblp_crawler
from paper_matching import similarity
from pdf2bow import pdf2bow

import json

fileConfig('logging_config.ini')
logger = logging.getLogger()

researchers = ["Leong Tze Yun", "Bryan Low"]


def prepare_bow_content(researcher):
    # Look up researcher from dblp to get list of publications
    author_results = dblp_crawler.dblp_crawler(researcher)
    dblp_crawler.print_publication_list(author_results)

    papers_DIR = "papers/" + researcher.replace(" ", "_") + "/"  # Only works when python file is run in the project root location
    bow_DIR = "bow/" + researcher.replace(" ", "_") + "/"

    # Download papers from arxiv, store in papers_DIR
    for author, publications in author_results.items():
        papers = [pub['title'] for pub in publications]

        utils.is_folder_exists_create_otherwise(papers_DIR)

        logging.info("Downloading paper...")
        arxiv_crawler.download_list_of_papers(papers[0:5], dirname=papers_DIR)

    # Run BOW
    pdf2bow.run(input_path=papers_DIR, output_dir=bow_DIR)

    # Concatenate all BOWs
    all_bows = ' '.join([utils.read_file(filename) for filename in glob.glob(bow_DIR + '*.bow')])

    # Return a dictionary
    return {'researcher': researcher, 'bow_content': all_bows}


researchers_to_bows = [prepare_bow_content(researcher) for researcher in researchers]  # List of dictionary {researcher: all their papers' bow}

with open("data.json", 'wb') as outfile:
    json.dump(researchers_to_bows, outfile)


    
    # _, bow_corpus = similarity.build_corpus(bow_DIR)
    # similarity.tfidf_transform(bow_corpus)

# LDA IMPLEMENTATION USING GENSIM (TBC)
# Lda = gensim.models.ldamodel.LdaModel
# ldamodel = Lda(bow_corpus, num_topics=10, id2word=dictionary, passes=50)

# print(ldamodel.print_topics(num_topics=5, num_words=3))
