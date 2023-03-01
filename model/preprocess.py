import re
import json
import spacy
import demoji
import pandas as pd
import unicodedata as uni
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

sp = spacy.load("en_core_web_sm")
stemmer = PorterStemmer()
en_stopwords = set(stopwords.words('english'))

def _removeUrl(text):
    text = re.sub(r"http\S+", "", text)
    
    return text

def _handleEmoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji].split(":")[0])

    return string

def _wordTokenizer(text):
    text = text.lower()
    text = text.split()

    return text

def _removeStopwords(text):
    text = [word for word in text if word not in en_stopwords]
    
    return text

def _stemming(text):
    text = [stemmer.stem(word) for word in text]
    
    return text

def _lemmatization(text):
    text = " ".join(text)
    token = sp(text)

    text = [word.lemma_ for word in token]
    return text

def Preprocess(series):
    """
    This function is the process of preprocessing the data
    """
    text=series["review"]
    text = _removeUrl(text) 
    text = uni.normalize('NFKD', text)
    text = _handleEmoji(text)
    text = text.lower() 
    text = re.sub(r'[^\w\s]', '', text)
    text = _wordTokenizer(text)
    text = _lemmatization(text)
    text = [word.lower() for word in text]
    text = _removeStopwords(text)
    text = " ".join(text)

    return text


def LoadJson(path):
    """
    this function is for local text
    """
    with open(path,'r',encoding="utf-8") as f:
        reviewJson=f.read()
        reviewJson=json.loads(reviewJson)
    
    return reviewJson

def Json2Dataframe(reviewJson):
    """
    This function is to convert the json file received from the front end into a df file for subsequent processing 
    """
    asin=reviewJson["asin"]
    reviewData=reviewJson["reviews"]
    
    title=[]
    reviews=[]
    rating=[]
    
    for i in reviewData:
        title.append(i["title"])
        reviews.append(i["review"])
        rating.append(i["rating"])
    
    reviewData=pd.DataFrame(title,columns=["title"])
    reviewData=pd.concat([reviewData,pd.DataFrame(reviews,columns=["review"])],axis=1)
    reviewData=pd.concat([reviewData,pd.DataFrame(rating,columns=["rating"])],axis=1)
    reviewData.dropna(inplace=True,axis=0)
    print(reviewData.head())
    
    return asin,reviewData

if __name__=="__main__":
    reviewJson=LoadJson("D:\WorkMenu\PythonCode\TextAnalysis\ReviewEmotionAnalysis\example.json")
    asin,reviewData=Json2Dataframe(reviewJson)
    reviewData["cleanReview"]=reviewData.apply(Preprocess,axis=1)

