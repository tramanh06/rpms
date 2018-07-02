import json
from pdf2bow import pdf2bow
import utils
from paper_matching import similarity


def main():
    test_document_path = "/Users/nus/Dropbox/NUS/Papers/The Bayesian Case Model - A Generative Approach for Case-Based Reasoning and Prototype Classification.pdf"

    # Get tokenized for test file
    pdf2bow.run(input_path=test_document_path)

    # read data from json training file
    with open('data.json') as f:
        data = json.load(f)

    dictionary, corpus_bow = similarity.build_corpus_from_json(researchers_bow=data)

    test_data_bow = dictionary.doc2bow(utils.read_file(test_document_path.split("/")[-1].replace("pdf", "bow")).split())
    print "List of researchers in ranked order:"
    cosine_similarity = similarity.tfidf_transform(corpus_bow=corpus_bow, document=test_data_bow)
    zipped = zip(data, cosine_similarity)
    zipped.sort(key=lambda t: t[1], reverse=True)
    for author_bow, score in zipped:
        print ": ".join([author_bow["researcher"], str(score)])
    

if __name__ == '__main__':
    main()