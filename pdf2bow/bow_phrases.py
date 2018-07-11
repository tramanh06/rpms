'''
Transform txt files to simple preprocessed text
'''

import glob
import gensim
import spacy
from nltk.corpus import stopwords
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import nltk
nltk.download('words')


def read_tokenized_files(directory="./"):
    all_tok = [utils.read_file(filename) for filename in glob.glob(directory + '*.tokenize')]
    return all_tok


def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(sentence, deacc=True))  # deacc=True removes punctuations


# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    # english_words = set(nltk.corpus.words.words())
    return [[word for word in gensim.utils.simple_preprocess(str(doc), deacc=True) if word not in stop_words] for doc in texts]


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    nlp = spacy.load('en', disable=['parser', 'ner'])

    texts_out = []
    for sent in texts:
        doc = nlp(unicode(" ".join(sent))) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def text_preprocess_with_phrases(docs, bigram_mod=None):
    '''
    Do phrase tokenization + stopword removal

    docs (list): List of string
    '''

    print "len(docs) = " + str(len(docs))

    # Split sentences into words
    docs = list(sent_to_words(docs))

    print "First document: " 
    print docs[:1]

    if not bigram_mod:
        # Create bigram phrases when necessary
        bigram = gensim.models.Phrases(docs)
        bigram_mod = gensim.models.phrases.Phraser(bigram)

    # Remove Stop Words
    data_words_nostops = remove_stopwords(docs)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    print(data_lemmatized[:1])

    return data_lemmatized, bigram_mod


