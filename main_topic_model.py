import json
import gensim

json_file_location = "data_with_phrases.json"

with open(json_file_location) as f:
    data = json.load(f)

data_words = [x['bow_content'].split() for x in data]

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



doc_lda = lda_model[corpus]
print doc_lda
for topic in doc_lda:
    print(topic)