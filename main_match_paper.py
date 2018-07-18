import json
from pdf2bow import pdf2bow, bow_phrases
import utils
from paper_matching import similarity
import logging
import pickle


def main():
    # test_document_path = "/Users/nus/Dropbox/NUS/Papers/Gaussian Process Regression Networks.pdf"
    test_document_path = "/Users/nus/Dropbox/NUS/Papers/Scalable and accurate deep learning with electronic healthrecords.pdf"

    TOKENS_PHRASE = False  # Toggle whether to detect phrase at tokenization step

    data_json_file = "data_with_phrases.json" if TOKENS_PHRASE else "data.json"
    dictionary_file = "dictionary_phrases.dict" if TOKENS_PHRASE else "dictionary_unigram.dict"

    # read data from json training file
    with open(data_json_file) as f:
        data = json.load(f)

    bow_file_location = pdf2bow.run(input_path=test_document_path)
    corpus = build_corpus_from_json(researchers_bow=data)
    dictionary, corpus_bow = similarity.build_dictionary(corpus)
    dictionary.save(fname_or_handle=dictionary_file)
    corpora.MmCorpus.serialize("corpus.mm", corpus_bow)

    if not TOKENS_PHRASE:
        # Get tokenized for test file
        test_data_preprocessed = utils.read_file(bow_file_location).split()
    else:
        bigram_mod = pickle.load(open("bigram_model.p", "rb"))
        data_lemmatized, _ = bow_phrases.text_preprocess_with_phrases([utils.read_file(bow_file_location.replace(".bow", ".txt"))], bigram_mod=bigram_mod)
        test_data_preprocessed = data_lemmatized[0]

    test_data_bow = dictionary.doc2bow(test_data_preprocessed)

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