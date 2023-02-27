if __name__ == '__main__':
    import pandas as pd
    import torch
    import numpy as np
    import sqlite3
    import matplotlib.pyplot as plt
    import seaborn as sns
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.stem.porter import PorterStemmer
    from sklearn.feature_extraction.text import CountVectorizer

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    import warnings

    data=pd.read_csv("reviews(B0BGYFDQJX)_1677452682203.csv")
    print(data.info())

    data=data.drop(labels=["date.unix","date.date","name","media","asin.variant","date.unix","media","verified_purchase"],axis=1)
    data.dropna(inplace=True, axis=0)

    import re


    def remove_url(text):
        text = re.sub(r"http\S+", "", text)
        return text

    import demoji


    def handle_emoji(string):
        emojis = demoji.findall(string)

        for emoji in emojis:
            string = string.replace(emoji, " " + emojis[emoji].split(":")[0])

        return string

    def word_tokenizer(text):
        text = text.lower()
        text = text.split()

        return text

    from nltk.corpus import stopwords

    en_stopwords = set(stopwords.words('english'))
    
    def remove_stopwords(text):
        text = [word for word in text if word not in en_stopwords]
        return text

    from nltk.stem.porter import PorterStemmer
    from nltk.stem.lancaster import LancasterStemmer

    stemmer = PorterStemmer()
    # stemmer = LancasterStemmer()


    def stemming(text):

        text = [stemmer.stem(word) for word in text]
        return text

    import spacy

    sp = spacy.load("en_core_web_sm")

    def lemmatization(text):

        # text = [sp(word).lemma_ for word in text]

        text = " ".join(text)
        token = sp(text)

        text = [word.lemma_ for word in token]
        return text


    # print(f"Before Lemmatization : {word_tokenizer(sample)}")
    # print(f"After Lemmatization : {lemmatization(word_tokenizer(sample))}")

    import unicodedata as uni

    df_temp2 = data[(data['rating'] >=3)]
    positive = list(df_temp2[(df_temp2['review'].str.len() > 50) & (df_temp2['review'].str.len() < 350)]['review'])
    df_temp3 = data[(data['rating'] <3)]
    negative = list(df_temp3[(df_temp3['review'].str.len() > 50) & (df_temp3['review'].str.len() < 350)]['review'])
    print(len(positive))
    print(len(negative))

    import nlpaug.augmenter.word as naw

    aug = naw.AntonymAug(name='Antonym_Aug', aug_min=1, aug_max=10, aug_p=0.3, lang='eng', stopwords=en_stopwords, tokenizer=None, 
                        reverse_tokenizer=None, stopwords_regex=None, verbose=0)
    aug_negative = aug.augment(positive)
    df_negative = pd.DataFrame({"review" : aug_negative, 'y' : [0]*len(aug_negative)})
    df_negative2 = pd.DataFrame({"review" : negative, 'y' : [0]*len(negative)})
    df_positive = pd.DataFrame({"review" : positive, 'y' : [1]*len(positive)})
    df_temp = pd.concat([df_negative, df_positive,df_negative2]).sample(frac = 1, random_state = 11).reset_index(drop=True)
    data = df_temp

    def preprocessing(text):
        
        text = remove_url(text) 
        text = uni.normalize('NFKD', text)
        text = handle_emoji(text)
        text = text.lower() 
        text = re.sub(r'[^\w\s]', '', text)
        text = word_tokenizer(text)
        # text = stemming(text)
        text = lemmatization(text)
        text = [word.lower() for word in text]
        text = remove_stopwords(text)
        text = " ".join(text)

        return text
    from tqdm import tqdm

    tqdm.pandas()

    data['clean_review'] = data['review'].progress_map(preprocessing)
    print(data.head())

    reviews = data.clean_review.values.tolist()
    from tqdm import tqdm

    tqdm.pandas()

    data['clean_review2'] = data['clean_review'].progress_map(word_tokenizer)

    data.head()

    data_words = data['clean_review2'].values.tolist()
    len(data_words)
    import gensim.corpora as corpora

    # Create Dictionary
    id2word = corpora.Dictionary(data_words)
    # Create Corpus
    texts = data_words
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    # View
    print(corpus[:1][0][:30])

    from gensim.models import LdaMulticore
    from gensim.models import LdaModel
    from pprint import pprint

    # number of topics
    num_topics = 10
    # Build LDA model
    #可以用其他数据更新训练模型，也就是可以多个数据一起训练。
    lda_model = LdaModel(corpus=corpus, id2word=id2word,
                        num_topics=num_topics, iterations=400)
    # Print the Keyword in the 10 topics
    b=lda_model.print_topics()
    doc_lda = lda_model[corpus]
    a=0