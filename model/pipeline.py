import json
import LDAModel
import ABSAModel
import preprocess

def Pipeline(reviewJson):
    asin,reviewData=preprocess.Json2Dataframe(reviewJson)
    reviewData["cleanReview"]=reviewData.apply(preprocess.Preprocess,axis=1)
    topicWord=LDAModel.LDA(reviewData)
    aspectCategory=ABSAModel.Predict(reviewData)

    return asin,reviewData,topicWord,aspectCategory
    

def ReturnResult(asin,reviewData,topicWord,aspectCategory):
    res={}
    res["asin"]=asin
    res["topicwords"]=topicWord
    review=reviewData["review"].values.tolist()
    for i in range(len(aspectCategory)):
        aspectCategory[i]["review"]=review[i]
    res["review"]=aspectCategory
    
    with open("{}_Result.json".format(asin),'w',encoding='utf-8') as f:
        json.dump(res, f,ensure_ascii=False)

if __name__=="__main__":
    reviewJson=preprocess.LoadJson("D:\WorkMenu\PythonCode\TextAnalysis\ReviewEmotionAnalysis\example.json")
    asin,reviewData,topicWord,aspectCategory=Pipeline(reviewJson)
    ReturnResult(asin,reviewData,topicWord,aspectCategory)