import joblib
import nltk
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn import metrics
from nltk import word_tokenize    
from scipy.sparse import hstack
import xml.etree.ElementTree as ET
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction import DictVectorizer
from nltk.tag.stanford import StanfordPOSTagger as POS_Tag
from sklearn.feature_extraction.text import CountVectorizer


_vect = CountVectorizer(max_df=1.0,stop_words='english')  
_pathToModel = r"D:\WorkMenu\PythonCode\TextAnalysis\ReviewEmotionAnalysis\resource\stanford-postagger-2017-06-09\models\english-bidirectional-distsim.tagger"
_pathToJar = r"D:\WorkMenu\PythonCode\TextAnalysis\ReviewEmotionAnalysis\resource\stanford-postagger-2017-06-09\stanford-postagger.jar"
stanfordTag = POS_Tag(model_filename=_pathToModel, path_to_jar=_pathToJar)

def _GetList(path):
    tree=ET.parse(path)
    root = tree.getroot()
    textList = []
    opinonList = []
    for review in root.findall('Review'):
        text=""
        opinion_inner_list=[]
        for sent in review.findall('./sentences/sentence'):
            text= text+ " "+ sent.find('text').text
        textList.append(text)
        for opinion in review.findall('./Opinions/Opinion'):
            opinion_dict = {
                opinion.get('category').replace('#','_'): opinion.get('polarity')
            }
            opinion_inner_list.append(opinion_dict)
        opinonList.append(opinion_inner_list)
    return textList,opinonList

def _GetMostCommonAspect(opinionList):
    opinion= []
    for i in opinionList:
        for _dict in i:
            for key in _dict:
                opinion.append(key)
    mostCommonAspect = [k for k,v in nltk.FreqDist(opinion).most_common(20)]
    return mostCommonAspect

def _GetDataframe(textList,opinionList,mostCommonAspect):
    data={'Review':textList}
    df = pd.DataFrame(data)
    if opinionList:
        for inner_list in opinionList:
            for _dict in inner_list:
                for key in _dict:
                    if key in mostCommonAspect:
                        df.loc[opinionList.index(inner_list),key]=_dict[key]
    return df

def _GetAspectDataframe(df,mostCommonAspect):
    for i in mostCommonAspect:
        df[i]=df[i].replace(['positive','negative','neutral','conflict'],[1,1,1,1])
    df = df.fillna(0)
    return df

def _GetPositiveDataframe(df,mostCommonAspect):
    for i in mostCommonAspect:
        df[i]=df[i].replace(['positive'],[1])
        df[i]=df[i].replace(['negative','neutral','conflict'],[0,0,0])
    df = df.fillna(0)
    return df

def _GetNegativeDataframe(df,mostCommonAspect):
    for i in mostCommonAspect:
        df[i]=df[i].replace(['negative'],[1])
        df[i]=df[i].replace(['positive','neutral','conflict'],[0,0,0])
    df = df.fillna(0)
    return df

def _GetNeuralDataframe(df,mostCommonAspect):
    for i in mostCommonAspect:
        df[i]=df[i].replace(['neutral','conflict'],[1,1])
        df[i]=df[i].replace(['negative','positive'],[0,0])
    df = df.fillna(0)
    return df

def _PosTag(review):
    taggedTextList=[]
    for text in review:
        taggedTextList.append(stanfordTag.tag(word_tokenize(text)))
    return taggedTextList

def _FilterTag(taggedReview):
    cleanTextList=[]
    for textList in taggedReview:
        texts=[]
        for word,tag in textList:
            if tag in ['NN','NNS','NNP','NNPS','RB','RBR','RBS','JJ','JJR','JJS','VB','VBD','VBG','VBN','VBP','VBZ']:
                texts.append(word)
        cleanTextList.append(' '.join(texts))
    return cleanTextList

def _GetDictAspect(y,mostCommonAspect):
    position=[]
    for innerlist in y:
        position.append([i for i, j in enumerate(innerlist) if j == 1])
    sortedCommon=sorted(mostCommonAspect)
    dictAspect=[]
    for innerlist in position:
        i={}
        for word in sortedCommon:
            if sortedCommon.index(word) in innerlist:
                i[word]= 5
            else:
                i[word]=0
        dictAspect.append(i)
    return dictAspect

def _ClassifySentiment(trainData,testData,XTrainAspect,XTestAspect,tag):
    
    trainData = trainData.reindex(sorted(trainData.columns), axis=1)
    testData = testData.reindex(sorted(testData.columns), axis=1)

    XTrain = trainData.Review
    YTrain = trainData.drop('Review',1)
    YTrain = np.asarray(YTrain, dtype=np.int64)

    XTest = testData.Review
    YTest = testData.drop('Review',1)
    YTest = np.asarray(YTest, dtype=np.int64)

    vecSen = CountVectorizer(stop_words='english',ngram_range=(1,2))  
    XTrainDtm = vecSen.fit_transform(XTrain)
    XTestDtm = vecSen.transform(XTest)

    XTrainDtm=hstack((XTrainDtm, XTrainAspect))
    XTestDtm=hstack((XTestDtm, XTestAspect))

    C = 1.0 #SVregularization parameter
    svc = OneVsRestClassifier(svm.SVC(kernel='linear', C=C)).fit(XTrainDtm, YTrain)

    YPredict = svc.predict(XTestDtm)

    if tag=="positive":
        joblib.dump(vecSen,"vecSenPostive.pkl")
        joblib.dump(svc, 'SVCModelPositive.pkl')
    if tag=="negative":
        joblib.dump(vecSen,"vecSenNegative.pkl")
        joblib.dump(svc, 'SVCModelNegative.pkl')
    if tag=="neural":
        joblib.dump(vecSen,"vecSenNural.pkl")
        joblib.dump(svc, 'SVCModelNeural.pkl')

    return (YTest,YPredict)

def _PrintMetrices(YTest,YPredict):
    print("Accuracy:")
    print(metrics.accuracy_score(YTest,YPredict))

    print("\nAverage precision:")
    print(metrics.precision_score(YTest,YPredict,average='micro'))

    print("\nAverage recall:")
    print(metrics.recall_score(YTest,YPredict,average='micro'))
    
    print("\nAverage f1:")
    print(metrics.f1_score(YTest,YPredict,average='micro'))

    print("\nClassification report:")
    print(metrics.classification_report(YTest, YPredict))

def Train(trainFilePath,testFilePath):
    trainTextList,trainOpinionList = _GetList(trainFilePath)
    mostCommonAspect = _GetMostCommonAspect(trainOpinionList)
    joblib.dump(mostCommonAspect,"MostCommonAspect.pkl")

    taggedTrainTextList=_PosTag(trainTextList)
    cleanTrainTextList=_FilterTag(taggedTrainTextList)

    trainDataframe = _GetDataframe(cleanTrainTextList,trainOpinionList,mostCommonAspect)
    trainAspectDataframe = _GetAspectDataframe(trainDataframe,mostCommonAspect)
    trainAspectDataframe = trainAspectDataframe.reindex(sorted(trainAspectDataframe.columns), axis=1)

    testTextList,testOpinionList = _GetList(testFilePath)

    taggedTestTextList=_PosTag(testTextList)
    cleanTestTextList=_FilterTag(taggedTestTextList)

    testDataframe = _GetDataframe(cleanTestTextList,testOpinionList,mostCommonAspect)
    testAspectDataframe = _GetAspectDataframe(testDataframe,mostCommonAspect)
    testAspectDataframe = testAspectDataframe.reindex(sorted(testAspectDataframe.columns), axis=1)

    XTrain= trainAspectDataframe.Review
    YTrain = trainAspectDataframe.drop('Review',1)

    XTest = testAspectDataframe.Review
    YTest = testAspectDataframe.drop('Review',1)

    YTrain = np.asarray(YTrain, dtype=np.int64)
    YTest = np.asarray(YTest, dtype=np.int64)

    
    XTrainDtm = _vect.fit_transform(XTrain)
    XTestDtm = _vect.transform(XTest)
    joblib.dump(_vect,"vect.pkl")

    C = 1.0 
    svc = OneVsRestClassifier(svm.SVC(kernel='linear', C=C)).fit(XTrainDtm, YTrain)
    joblib.dump(svc, 'SVCModel.pkl')

    YPredict = svc.predict(XTestDtm)

    train_dict_aspect=_GetDictAspect(YTrain, mostCommonAspect)
    d_train=DictVectorizer() 
    X_train_aspect_dtm = d_train.fit_transform(train_dict_aspect)

    test_dict_aspect=_GetDictAspect(YTest,mostCommonAspect)
    d_test=DictVectorizer() 
    X_test_aspect_dtm = d_test.fit_transform(test_dict_aspect)

    trainDataframe = _GetDataframe(cleanTrainTextList,trainOpinionList,mostCommonAspect)
    testDataframe = _GetDataframe(cleanTestTextList,testOpinionList,mostCommonAspect)

    df_train_positive = _GetPositiveDataframe(trainDataframe,mostCommonAspect)
    df_test_positive = _GetPositiveDataframe(testDataframe,mostCommonAspect)
    y_test_pos,y_pred_class_svc_pos=_ClassifySentiment(df_train_positive,df_test_positive,X_train_aspect_dtm,X_test_aspect_dtm,"positive")

    trainDataframe = _GetDataframe(cleanTrainTextList,trainOpinionList,mostCommonAspect)
    testDataframe = _GetDataframe(cleanTestTextList,testOpinionList,mostCommonAspect)

    df_train_neg = _GetNegativeDataframe(trainDataframe,mostCommonAspect)
    df_test_neg = _GetNegativeDataframe(testDataframe,mostCommonAspect)

    y_test_neg,y_pred_class_svc_neg=_ClassifySentiment(df_train_neg,df_test_neg,X_train_aspect_dtm,X_test_aspect_dtm,"negative")

    trainDataframe = _GetDataframe(cleanTrainTextList,trainOpinionList,mostCommonAspect)
    testDataframe = _GetDataframe(cleanTestTextList,testOpinionList,mostCommonAspect)

    df_train_neu = _GetNeuralDataframe(trainDataframe,mostCommonAspect)
    df_test_neu = _GetNeuralDataframe(testDataframe,mostCommonAspect)

    y_test_neu,y_pred_class_svc_neu=_ClassifySentiment(df_train_neu,df_test_neu,X_train_aspect_dtm,X_test_aspect_dtm,"neural")

def Predict(reviewData):
    reviews=reviewData["review"].values.tolist()
    reviews = _PosTag(reviews)
    cleanReviewData = _FilterTag(reviews)

    reviewSeries=pd.Series(cleanReviewData)
    _vect=joblib.load("vect.pkl")
    reviewSeriesDtm=_vect.transform(reviewSeries)

    svc=joblib.load("SVCModel.pkl")
    predictAspect= svc.predict(reviewSeriesDtm)

    svcPositve=joblib.load("SVCModelPositive.pkl")
    svcNegative=joblib.load("SVCModelNegative.pkl")
    vecSenPostive=joblib.load("vecSenPostive.pkl")
    vecSenNegative=joblib.load("vecSenNegative.pkl")
    mostCommonAspect=joblib.load("MostCommonAspect.pkl")

    extraFeature=_GetDictAspect(predictAspect, mostCommonAspect)
    extraFeatureDtm=DictVectorizer().fit_transform(extraFeature)
    opinionList=[]
    data = _GetDataframe(cleanReviewData,opinionList,mostCommonAspect)
    data=data.Review

    dataDtm = vecSenPostive.transform(data)
    dataDtm=hstack((dataDtm, extraFeatureDtm))
    YPositivePredict = svcPositve.predict(dataDtm)

    dataDtm = vecSenNegative.transform(data)
    dataDtm=hstack((dataDtm, extraFeatureDtm))
    YNegativePredict = svcNegative.predict(dataDtm)


    res=[]
    for j in range(len(YPositivePredict)):
        indexPositive=[]
        for i, (a, b) in enumerate(zip(predictAspect[j], YPositivePredict[j])):
            if a ==1 and b==1:
                indexPositive.append(i)
    
        indexNegative=[]
        for i, (a, b) in enumerate(zip(predictAspect[j], YNegativePredict[j])):
            if a ==1 and b==1:
                indexNegative.append(i)
    
        r={}
        if indexPositive:
            for index in indexPositive:
                r[sorted(mostCommonAspect)[index]]=1
        if indexNegative:
            for index in indexNegative:
                r[sorted(mostCommonAspect)[index]]=-1
        res.append(r)

    reviewData.drop("cleanReview",axis=1,inplace=True)
    reviewData.drop("reviewToken",axis=1,inplace=True)

    aspectDict={}
    for i in res:
        aspectDict={**aspectDict,**i}

    aspect=list(set(aspectDict))

    res=pd.DataFrame(res,columns=aspect)
    res.fillna(0,inplace=True)

    posRating={}
    for i in aspect:
        pos=list(res[i]).count(1)
        neg=list(res[i]).count(-1)
        rating=pos/(pos+neg)
        posRating[i]=rating

    df=reviewData.join(res,how="outer")
    return df,posRating
    
if __name__=="__main__":
    Train("data\ABSA16_Laptops_Train_English_SB2.xml","data\EN_LAPT_SB2_TEST_label.xml")


