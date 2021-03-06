# THIS FILE IS DEPRECATED AND WAS ONLY USED FOR EXPERIMENT. 
# It is not the main Topic Modelling file to be used.
# Please see notebooks/Author-Topic_Model_2.ipynb for the working code

import json
import gensim
import utils
import logging


# Train LDA
class TopicModel():

    def __init__(self, source_file="papers.json", prune_dictionary=False, num_topics=5):
        data = utils.read_json_file(source_file)

        data_words = [x.split() for x in data]

        self.dictionary = gensim.corpora.Dictionary(data_words)

        if prune_dictionary:
            self.dictionary.filter_extremes(no_below=0, no_above=0.90, keep_n=None)

        corpus = [self.dictionary.doc2bow(text) for text in data_words]

        self.lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                         id2word=self.dictionary,
                                                         num_topics=num_topics, 
                                                         random_state=100,
                                                         update_every=1,
                                                         chunksize=100,
                                                         passes=10,
                                                         alpha='symmetric',
                                                         per_word_topics=False)
            
        # Print the Keyword in the 10 topics
        logging.info("Topics discovered (%s topics): ", num_topics)
        logging.info(self.lda_model.print_topics())

    # Inference
    def inference_topic(self, file_location="data.json"):
        data = utils.read_json_file(file_location)
        data_words = [x["bow_content"].split() for x in data]

        termdoc_vector = [self.dictionary.doc2bow(text) for text in data_words]

        doc_lda = self.lda_model[termdoc_vector]

        print doc_lda
        for topic in doc_lda:
            print(topic)


def main():
    topicModel = TopicModel(source_file="papers.json", prune_dictionary=True, num_topics=5)
    topicModel.inference_topic(file_location="data.json")


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("gensim").setLevel(logging.ERROR)

    main()