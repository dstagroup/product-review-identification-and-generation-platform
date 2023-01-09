import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier as SGD
from sklearn.model_selection import GridSearchCV
import numpy as np

savePath="./ReviewEmotionAnalysis/"

def load_data(data='train'):
    """
       function name: data load
       description  : Load training data set or test data set according to parameters
       param        : data, Specify the type of dataset to be loaded
       return       : dataset
       """
    train_data_path = savePath+"train_data_clean.csv"
    test_data_path = savePath+"test_data_clean.csv"
    if data == 'train':
        dataset = pd.read_csv(train_data_path, header=None, encoding='utf-8')
    else:
        dataset = pd.read_csv(test_data_path, header=None, encoding='utf-8')
    dataset.drop(index=0, axis=0, inplace=True)
    dataset.drop(columns=0, axis=1, inplace=True)
    return dataset



def model_train():
    train_data=load_data('train')
    test_data=load_data('test')
    train_data.columns = ['Rating', 'Title', 'Review']
    test_data.columns = ['Rating', 'Title', 'Review']
    
    x_all=pd.concat([train_data,test_data])
    len_train=len(train_data)

    x_all_review=x_all['Review'].tolist()

    tfv = TfidfVectorizer(  strip_accents='unicode', analyzer='word',token_pattern=r"(?u)\b\w+\b",
        ngram_range=(1, 2), use_idf=1,smooth_idf=1,sublinear_tf=1,
        stop_words = 'english')
    tfv.fit(x_all_review)
    x_all_review= tfv.transform(x_all_review)

    x_train = x_all_review[:len_train]
    x_test=x_all_review[len_train:]
    y_train=train_data['Rating']
    y_test=test_data['Rating'].tolist()


    model_NB = MultinomialNB()
    model_NB.fit(x_train, y_train)
    y_pre=model_NB.predict(x_test)
   
    print("accuracy:{}".format( sum([1 for i in range(0,len(y_pre)) if y_pre[i] ==y_test[i] ])/len(y_pre)))

if __name__ == '__main__':
    model_train()

