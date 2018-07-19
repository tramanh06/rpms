'''
Transform txt files to simple preprocessed text
'''

import glob
import os
import sys

import gensim

import bow_service
import utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read_tokenized_files(directory="./"):
    all_tok = [utils.read_file(filename) for filename in glob.glob(directory + '*.tokenize')]
    return all_tok


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


def text_preprocess_with_phrases(docs, bigram_mod=None):
    '''
    Do phrase tokenization + stopword removal

    docs (list): List of string
    '''

    print "len(docs) = " + str(len(docs))

    # Split sentences into words
    docs = list(bow_service.sent_to_words(docs))

    # print "First document: " 
    # print docs[:1]

    if not bigram_mod:
        # Create bigram phrases when necessary
        bigram = gensim.models.Phrases(docs)
        bigram_mod = gensim.models.phrases.Phraser(bigram)

    # Remove Stop Words
    data_words_nostops = bow_service.remove_stopwords(docs)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = bow_service.lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    # print(data_lemmatized[:1])

    return data_lemmatized, bigram_mod
