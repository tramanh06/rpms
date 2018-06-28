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
from logging.config import fileConfig

import gensim
from tqdm import tqdm

import utils
from paper_crawling import arxiv_crawler, dblp_crawler
from paper_matching import similarity
from pdf2bow import pdf2bow

fileConfig('logging_config.ini')
logger = logging.getLogger()


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
        arxiv_crawler.download_list_of_papers(papers[0:5], dirname=papers_DIR)

    # Run BOW
    pdf2bow.run(input_path=papers_DIR, output_dir=bow_DIR)

    # Concatenate all BOWs
    all_bows = ' '.join([utils.read_file(filename) for filename in glob.glob(bow_DIR + '*.bow')])

    # Return a dictionary
    return {'researcher': researcher, 'bow_content': all_bows}


if __name__ == '__main__':
    # researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu", "Kuldeep S. Meel", "Lee Wee Sun"]
    researchers = ["Leong Tze Yun", "Bryan Low", "Harold Soh", "David Hsu"]
    test_document_path = "/Users/nus/Dropbox/NUS/Papers/Scalable and accurate deep learning with electronic healthrecords.pdf"

    # researchers_to_bows = [prepare_bow_content(researcher) for researcher in researchers]  # List of dictionary {researcher: all their papers' bow}
    # pool = mp.Pool()
    # # researchers_to_bows = list(tqdm(pool.imap(prepare_bow_content, researchers)))
    # researchers_to_bows = pool.map(prepare_bow_content, researchers)

    # write data to json file
    # with open("data.json", 'wb') as outfile:
    #     json.dump(researchers_to_bows, outfile)

    # Get tokenized for test file
    pdf2bow.run(input_path=test_document_path)

    # read data from json training file
    with open('data.json') as f:
        data = json.load(f)

    dictionary, corpus_bow = similarity.build_corpus_from_json(researchers_bow=data)

    test_data_bow = dictionary.doc2bow(utils.read_file(test_document_path.split("/")[-1].replace("pdf", "bow")).split())
    print "List of researchers"
    cosine_similarity = similarity.tfidf_transform(corpus_bow=corpus_bow, document=test_data_bow)
    for author_bow, score in zip(data, cosine_similarity):
        print ": ".join([author_bow["researcher"], str(score)])
    





# dictionary = corpora.Dictionary.load('dictionary.dict')
# corpus = corpora.MmCorpus("corpus.mm")
# lda = models.LdaModel.load("model.lda") #result from running online lda (training)

# index = similarities.MatrixSimilarity(lda[corpus])
# index.save("simIndex.index")

# docname = "docs/the_doc.txt"
# doc = open(docname, 'r').read()
# vec_bow = dictionary.doc2bow(doc.lower().split())
# vec_lda = lda[vec_bow]

# sims = index[vec_lda]
# sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print sims

    
# LDA IMPLEMENTATION USING GENSIM (TBC)
# Lda = gensim.models.ldamodel.LdaModel
# ldamodel = Lda(bow_corpus, num_topics=10, id2word=dictionary, passes=50)

# print(ldamodel.print_topics(num_topics=5, num_words=3))
