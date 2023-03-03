import preprocess
from nltk.tag import pos_tag
from collections import Counter
import gensim.corpora as corpora
from gensim.models import LdaModel


def LDA(reviewData):
    reviewData["reviewToken"]=reviewData["cleanReview"].apply(preprocess._wordTokenizer)
    
    dataWords=reviewData["reviewToken"].values.tolist()
    id2word = corpora.Dictionary(dataWords)
    corpus = [id2word.doc2bow(text) for text in dataWords]
    
    numTopics = 10
    ldaModel = LdaModel(corpus=corpus, id2word=id2word,
                        num_topics=numTopics, iterations=400)
    topTopic=ldaModel.top_topics(corpus)
    
    topic=[]
    for i in topTopic:
        for j in i[0]:
            topic.append(j[1])
    
    filterTag=["JJ","JJR","JJS"]
    topic=pos_tag(topic)
    topic=[i[0] for i in topic if i[1] in filterTag]
    topicWord=Counter(topic).most_common(10)
    topicWord=[i[0] for i in topicWord]
    
    return topicWord