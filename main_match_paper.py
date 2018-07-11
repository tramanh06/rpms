import json
from pdf2bow import pdf2bow
import utils
from paper_matching import similarity
import logging


def main():
    # test_document_path = "/Users/nus/Dropbox/NUS/Papers/Gaussian Process Regression Networks.pdf"
    test_document_path = "/Users/nus/Dropbox/NUS/Papers/Scalable and accurate deep learning with electronic healthrecords.pdf"

    # Get tokenized for test file
    pdf2bow.run(input_path=test_document_path)

    # read data from json training file
    with open('data.json') as f:
        data = json.load(f)

    corpus = build_corpus_from_json(researchers_bow=data)
    dictionary, corpus_bow = similarity.build_dictionary(corpus)

    test_data_bow = dictionary.doc2bow(utils.read_file(test_document_path.split("/")[-1].replace("pdf", "bow")).split())
    logging.info("***********")
    logging.info("***** Paper: %s *****", test_document_path.split("/")[-1])
    logging.info("***********")
    logging.info("List of researchers in ranked order:")
    cosine_similarity = similarity.tfidf_transform(corpus_bow=corpus_bow, document=test_data_bow)
    zipped = zip(data, cosine_similarity)
    zipped.sort(key=lambda t: t[1], reverse=True)
    for author_bow, score in zipped:
        logging.info(": ".join([author_bow["researcher"], str(score)]))
 

def build_corpus_from_json(researchers_bow):
    corpus = [researcher_bow['bow_content'].split() for researcher_bow in researchers_bow]
    return corpus
    

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("gensim").setLevel(logging.ERROR)

    main()