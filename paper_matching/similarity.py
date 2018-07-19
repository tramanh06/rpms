from gensim import corpora, models, similarities
import os, sys
import glob
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import logging

# gensim reference is from https://gist.github.com/clemsos/7692685#file-gensim_workflow-py-L81 


def build_corpus(text_files_location):
    print 'Index of files:'
    print "\n".join([file for file in glob.glob(text_files_location + '*.bow')])
    # Build corpus
    corpus = [utils.read_file(filename).split(' ') for filename in glob.glob(text_files_location + '*.bow')]

    dictionary, doc_term_matrix = build_dictionary(corpus)
    return dictionary, doc_term_matrix


def build_dictionary(corpus):
    # BOW for each document
    dictionary = corpora.Dictionary(corpus)
    doc_term_matrix = [dictionary.doc2bow(t) for t in corpus]
    return dictionary, doc_term_matrix


def tfidf_transform(corpus_bow, document):
    '''
    Args:
        corpus_bow: BOW of the corpus 
        document: New document (in stemmed format) to calculate cosine similarity with 
    
    Returns:
        Similarity matrix
    '''
    # tf-idf
    tfidf = models.TfidfModel(corpus_bow)
    document_tfidf = tfidf[document]

    index = similarities.MatrixSimilarity(tfidf[corpus_bow])    # This needs to run against corpus
    sims = index[document_tfidf]
    logging.debug("Similarity matrix: %s", sims)
    return sims


def main():
    text_files_location = path.join(path.dirname(__file__), '../pdf2bow/output/')
    _, corpus_bow = build_corpus(text_files_location)
    tfidf_transform(corpus_bow, corpus_bow)


if __name__ == '__main__':
    main()
