import pandas as pd
import jieba
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def data_init(filename):
    """
    function name: data load
    description  : Initialize the dataset and divide the data into three categories: positive, negative, and neutral
                   based on the rating
    param        : filename
    """
    data = pd.read_csv(filename, header=None, encoding='utf-8', names=['Rating', 'Title', 'Review'])
    data[['Rating']] = data[['Rating']].astype(int)

    data_positive_4 = data.loc[data['Rating'] == 4].iloc[0:4999]
    data_positive_5 = data.loc[data['Rating'] == 5].iloc[0:4999]
    data_negative_1 = data.loc[data['Rating'] == 1].iloc[0:4999]
    data_negative_2 = data.loc[data['Rating'] == 2].iloc[0:4999]
    data_neutral_3 = data.loc[data['Rating'] == 3].iloc[0:9999]

    data_frames = [data_positive_5, data_positive_4, data_neutral_3, data_negative_1, data_negative_2]
    data_mini = pd.concat(data_frames, ignore_index=True, axis=0)
    data_mini.loc[data_mini['Rating'] <= 2, 'Rating'] = -1
    data_mini.loc[data_mini['Rating'] >= 4, 'Rating'] = 1
    data_mini.loc[data_mini['Rating'] == 3, 'Rating'] = 0

    data_mini.to_csv("../data/train_mini.csv")


def data_split(filename):
    """
    function name: data split
    description  : Divide the data set into a training set and a test set according to 8:2
    param        : filename
    """
    data = pd.read_csv(filename, header=None, encoding='utf-8')
    data.drop(index=0, axis=0, inplace=True)
    data.drop(columns=0, axis=1, inplace=True)
    train_data = data.sample(frac=0.8, random_state=0, axis=0)
    test_data = data[~data.index.isin(train_data.index)]

    # save the training and test data set
    train_data.to_csv("../data/train_data.csv")
    test_data.to_csv("../data/test_data.csv")


def load_data(data='train'):
    """
       function name: data load
       description  : Load training data set or test data set according to parameters
       param        : data, Specify the type of dataset to be loaded
       return       : dataset
       """
    train_data_path = '../data/train_data.csv'
    test_data_path = '../data/test_data.csv'
    if data == 'train':
        dataset = pd.read_csv(train_data_path, header=None, encoding='utf-8')
    else:
        dataset = pd.read_csv(test_data_path, header=None, encoding='utf-8')
    dataset.drop(index=0, axis=0, inplace=True)
    dataset.drop(columns=0, axis=1, inplace=True)
    return dataset


def remove_stopwords(text):
    """
          function name: remove stopwords
          description  : remove stopwords and special characters
          param        : text as a string
          return       : a word list after removing the stopwords
          """
    stopwords_list = stopwords.words('english')

    # remove special word
    for special_word in ['!', '?', '[', '-', '(', ')', '\'', '"', '#', '@',
                         ';', ':', '<', '>', '{', '}', '+', '=', '~', '|', '.', ',', ']', ' ']:
        stopwords_list.append(special_word)

    word_tokens = jieba.cut(text, cut_all=False)
    # print(word_tokens)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stopwords_list:
            filtered_sentence.append(w.lower())
    return filtered_sentence


def word_stemming(filtered_word_list):
    """
          function name: word stemming
          description  : Stemming for each verb
          param        : word list
          return       : stemmed word list
          """
    # word stemming
    stemmed_sentence = []
    ps = PorterStemmer()
    for w in filtered_word_list:
        root_word = ps.stem(w)
        stemmed_sentence.append(root_word)
    return stemmed_sentence


def data_clean(data='train'):
    """
       function name: data clean
       description  : remove stopwords and stemming
       param        : data
       return       : clean dataset
       """
    train_data = load_data(data)
    train_data.columns = ['Rating', 'Title', 'Review']
    train_data['Review'] = train_data['Review'].map(lambda x: word_stemming(remove_stopwords(x)))
    train_data.to_csv("../data/train_data_clean.csv")


if __name__ == '__main__':
    # dataset_path = '../ReviewSentimentAnalysis/data/train.csv'
    # data_load(dataset_path)

    # dataset_path2 = '../ReviewSentimentAnalysis/data/train_mini.csv'
    # data_split(dataset_path2)

    # load_train_data()
    data_clean()
