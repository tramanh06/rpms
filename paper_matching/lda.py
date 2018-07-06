import gensim
import nltk
from os import path
import re
import io
from nltk.corpus import stopwords
import spacy
import gensim.corpora as corpora

def lda_unigram():
    # LDA code
    dictionary = gensim.corpora.Dictionary.load(path.join(path.dirname(__file__), '../dictionary.dict'))
    bow_corpus = gensim.corpora.MmCorpus(path.join(path.dirname(__file__), "../corpus.mm"))
    # lda = models.LdaModel.load("model.lda") #result from running online lda (training)

    # LDA IMPLEMENTATION USING GENSIM (TBC)
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(bow_corpus, num_topics=5, id2word=dictionary, passes=50)

    print(ldamodel.print_topics(num_topics=5, num_words=5))


def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


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


def bigram():
    file_location_1 = "/Users/nus/git/tpms/paper_matching/A_Unifying_Framework_of_Anytime_Sparse_Gaussian_Process_Regression_Models_with_Stochastic_Variational_Inference_for_Big_Data.txt"
    file_location_2 = "/Users/nus/git/tpms/paper_matching/Learning_Dynamic_Robot_to_Human_Object_Handover_from_Human_Feedback.txt"
    file_location_3 = "/Users/nus/git/tpms/paper_matching/Gaussian_Process_Based_Decentralized_Data_Fusion_and_Active_Sensing_for_Mobility_on_Demand_System.txt"
    data = []
    with io.open(file_location_1, 'r', encoding='utf-8', errors='ignore') as f:
        data.append(f.read())
    with io.open(file_location_2, 'r', encoding='utf-8', errors='ignore') as f:
        data.append(f.read())
    with io.open(file_location_3, 'r', encoding='utf-8', errors='ignore') as f:
        data.append(f.read())

    # print data
    # split document into sentences
    # sentences = nltk.sent_tokenize(data)
    sentences = data

    # Split sentences into words
    data_words = list(sent_to_words(sentences))
    # print data_words[:1]

    # Create bigram phrases when necessary
    bigram = gensim.models.Phrases(data_words)
    bigram_mod = gensim.models.phrases.Phraser(bigram)

    # print(bigram_mod[bigram_mod[data_words[0]]])

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    print(data_lemmatized[:1])

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    # print(corpus[:1])

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=3, 
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=False)
    
    # Print the Keyword in the 10 topics
    print(lda_model.print_topics())

    doc_lda = lda_model[corpus]
    print doc_lda
    for topic in doc_lda:
        print(topic)


def main():
    bigram()
    

if __name__ == '__main__':
    main()    






# index = similarities.MatrixSimilarity(lda[corpus])
# index.save("simIndex.index")

# docname = "docs/the_doc.txt"
# doc = open(docname, 'r').read()
# vec_bow = dictionary.doc2bow(doc.lower().split())
# vec_lda = lda[vec_bow]

# sims = index[vec_lda]
# sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print sims

    

