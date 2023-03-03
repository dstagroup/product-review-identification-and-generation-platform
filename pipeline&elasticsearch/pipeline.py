import json
import LDAModel
import ABSAModel
import preprocess
import elasticSearchApi

def Pipeline(reviewJson):
    asin,usrID,detail,profile,reviewData=preprocess.Json2Dataframe(reviewJson)
    reviewData["cleanReview"]=reviewData.apply(preprocess.Preprocess,axis=1)
    topicWord=LDAModel.LDA(reviewData)
    reviewData,posRating=ABSAModel.Predict(reviewData)

    es=elasticSearchApi.CommodityEsConnect()
    es.AddCommodity(asin,usrID,detail,profile,topicWord,reviewData,posRating)
    return asin,usrID,detail,profile,topicWord,posRating

if __name__=="__main__":
    reviewJson=preprocess.LoadJson(r"D:\WorkMenu\PythonCode\TextAnalysis\ReviewEmotionAnalysis\input_data\final.json")
    Pipeline(reviewJson)