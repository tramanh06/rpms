import json
import gensim
import utils

# Train LDA
json_file_location = "papers.json"

data = utils.read_json_file(json_file_location)

data_words = [x.split() for x in data]

dictionary = gensim.corpora.Dictionary(data_words)
corpus = [dictionary.doc2bow(text) for text in data_words]


lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=dictionary,
                                            num_topics=5, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=100,
                                            passes=10,
                                            alpha='symmetric',
                                            per_word_topics=False)
    
# Print the Keyword in the 10 topics
print(lda_model.print_topics())


# Inference 
papers_by_author_location = "data.json"
data = utils.read_json_file(papers_by_author_location)
data_words = [x["bow_content"].split() for x in data]

termdoc_vector = [dictionary.doc2bow(text) for text in data_words]

doc_lda = lda_model[termdoc_vector]
print doc_lda
for topic in doc_lda:
    print(topic)