from gensim import corpora, models, similarities
import os, sys
import glob
from os import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

# gensim reference is from https://gist.github.com/clemsos/7692685#file-gensim_workflow-py-L81 


def build_corpus(text_files_location):
    print 'Index of files:'
    print "\n".join([file for file in glob.glob(text_files_location + '*.bow')])
    # Build corpus
    corpus = [utils.read_file(filename).split(' ') for filename in glob.glob(text_files_location + '*.bow')]

    dictionary, corpus_bow = build_dictionary(corpus)
    return dictionary, corpus_bow


def build_corpus_from_json(researchers_bow):
    corpus = [researcher_bow['bow_content'].split() for researcher_bow in researchers_bow]
    
    dictionary, corpus_bow = build_dictionary(corpus)
    return dictionary, corpus_bow


def build_dictionary(corpus):
    # BOW for each document
    dictionary = corpora.Dictionary(corpus)
    corpus_bow = [dictionary.doc2bow(t) for t in corpus]
    return dictionary, corpus_bow


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
    print sims  
    return sims


def main():
    text_files_location = path.join(path.dirname(__file__), '../pdf2bow/output/')
    _, corpus_bow = build_corpus(text_files_location)
    tfidf_transform(corpus_bow, corpus_bow)


if __name__ == '__main__':
    main()


# LDA code
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