from gensim import corpora, models, similarities
import os, sys
import glob
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# gensim reference is from https://gist.github.com/clemsos/7692685#file-gensim_workflow-py-L81 


def build_corpus(file_directory=None):
    bow_dir = path.join(path.dirname(__file__), '../pdf2bow/output/')

    # Build corpus
    corpus = [utils.read_file(filename).split(' ') for filename in glob.glob(bow_dir + '*.bow')]

    # BOW for each document
    dictionary = corpora.Dictionary(corpus)
    corpus_bow = [dictionary.doc2bow(t) for t in corpus]
    return corpus_bow


def tfidf_transform(corpus_bow):
    # tf-idf
    tfidf = models.TfidfModel(corpus_bow)
    corpus_tfidf = tfidf[corpus_bow]

    index = similarities.MatrixSimilarity(tfidf[corpus_bow])
    sims = index[corpus_tfidf]
    print sims  


def main():
    tfidf_transform(build_corpus())

if __name__ == '__main__':
    main()

