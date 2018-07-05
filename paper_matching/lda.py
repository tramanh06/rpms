import gensim
from os import path

# LDA code
dictionary = gensim.corpora.Dictionary.load(path.join(path.dirname(__file__), '../dictionary.dict'))
bow_corpus = gensim.corpora.MmCorpus(path.join(path.dirname(__file__), "../corpus.mm"))
# lda = models.LdaModel.load("model.lda") #result from running online lda (training)

# LDA IMPLEMENTATION USING GENSIM (TBC)
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(bow_corpus, num_topics=20, id2word=dictionary, passes=50)

print(ldamodel.print_topics(num_topics=10, num_words=3))

# index = similarities.MatrixSimilarity(lda[corpus])
# index.save("simIndex.index")

# docname = "docs/the_doc.txt"
# doc = open(docname, 'r').read()
# vec_bow = dictionary.doc2bow(doc.lower().split())
# vec_lda = lda[vec_bow]

# sims = index[vec_lda]
# sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print sims

    

