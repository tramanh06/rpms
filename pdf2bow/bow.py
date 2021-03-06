import re
import nltk
from nltk.stem.snowball import SnowballStemmer
import gensim
import spacy
import bow_service
import logging
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils


def tokenize(data):
    # Remove non-letters
    letters_only = re.sub("[^\w\s]", " ", data)

    # tokenize
    try:
        words = nltk.tokenize.word_tokenize(letters_only.lower())
    except LookupError:
        nltk.download('punkt')
        words = nltk.tokenize.word_tokenize(letters_only.lower())

    return words


def remove_stopwords(words):
    # Remove stop words from nltk stopwords
    # Also remove numbers and words that have length 1

    try:
        stops = set(nltk.corpus.stopwords.words("english"))
        meaningful_words = [
            w for w in words if w not in stops and not w.isdigit() and len(w) > 1]
    except LookupError:
        nltk.download('stopwords')
        stops = set(nltk.corpus.stopwords.words("english"))
        meaningful_words = [
            w for w in words if w not in stops and not w.isdigit() and len(w) > 1]

    return meaningful_words


def stem_words(meaningful_words):
    # Stem words
    stemmer = SnowballStemmer("english")
    stemmed_words = [stemmer.stem(w) for w in meaningful_words]

    return stemmed_words


def preprocess_text(inputfile, outputfile):
    data = utils.read_file(inputfile)
    words = tokenize(data)
    meaningful_words = remove_stopwords(words)
    stemmed_words = stem_words(meaningful_words)
    stemmed = ' '.join(stemmed_words)
    utils.write_to_file(outputfile, stemmed)


def preprocess_gensim(inputfile, outputfile):
    data = utils.read_file(inputfile)
    data_words = gensim.utils.simple_preprocess(data, deacc=True)
    data_words_nostop = bow_service.remove_stopwords([data_words])
    data_lemmatized = bow_service.lemmatization(data_words_nostop, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    # print ' '.join(data_lemmatized[0])
    utils.write_to_file(outputfile, ' '.join(data_lemmatized[0]))


if __name__ == '__main__':
    from os import path
    output_dir = path.join(path.dirname(__file__), 'output/')
    inputfile = output_dir + "paper.txt"
    # outputfile = output_dir + "paper.bow"
    outputfile = output_dir + "paper_gensim.bow"

    preprocess_gensim(inputfile, outputfile)
