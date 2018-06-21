import re
import nltk
from nltk.stem.snowball import SnowballStemmer


def read_file(file_location):
    # Read text file, concatenate all lines into 1
    with open(file_location, 'rb') as f:
        data = f.read().replace('\n', " ")
    return data


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


def write_to_file(file_location, data):
    with open(file_location, 'w') as f:
        f.write(data)


def main():
    inputfile = "paper.txt"
    outputfile = "paper.preprocessing"
    
    data = read_file(inputfile)
    words = tokenize(data)
    meaningful_words = remove_stopwords(words)
    stemmed_words = stem_words(meaningful_words)
    stemmed = ' '.join(stemmed_words)
    write_to_file(outputfile, stemmed)

if __name__ == '__main__':
    main()