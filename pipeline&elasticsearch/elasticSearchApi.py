import uuid
from es_pandas import es_pandas
from elastic_transport import ApiResponse
from elasticsearch import Elasticsearch, helpers


class esConnect:
    """
    statue:
    1:create success
    2:create failed
    3:delete success
    4:delete failed
    5:index exist
    6:index unexist
    7:index already existed,create failed
    8:index not existed,delete failed
    """
    def __init__(self):
        self.es_host = "http://localhost:9200"
        self.es=es = Elasticsearch(
                    hosts=self.es_host
                )
    
    def CheckIndexIsExist(self,indexName):
        if self.es.indices.exists(index=indexName):
            return {"statue":5}
        else:
            return {"statue":6}
    
    def CreateIndex(self,indexName):
        if self.CheckIndexIsExist(indexName)["statue"]==6:
            if self.es.indices.create(index=indexName):
                return {"statue":1}
            else:
                return {"statue":2}
        else:
            return {"statue":7}
    
    def DeleteIndex(self,indexName):
        if self.CheckIndexIsExist(indexName)["statue"]==5:
            if self.es.indices.delete(index=indexName):
                return {"statue":3}
            else:
                return {"statue":4}
        else:
            return {"statue":8}

class LoginEsConnect(esConnect):
    """
    9.exist usr name
    10:create usr success
    11:create usr failed
    12:pwd error
    13:pwd correct
    """
    def __init__(self):
        super().__init__()

    def CheckIsExist(self,usrId,indexName):
        body={
            "query":{
                "term":{
                    "usr":usrId
                }
            }
        }
        if self.es.search(index=indexName,body=body)['hits']['total']['value']==0:
            return False
        else:
            return True
        

    def AddUser(self,usrId,pwd,indexName):
        if self.CheckIsExist(usrId,indexName):
            return {"statue":9}

        else:
            body={
                "usr":usrId,
                "pwd":pwd
            }
        
            if self.es.index(index=indexName,body=body)['result']=="created":
                return {"statue":10}
            else:
                return {"statue":11}

    def CheckPwd(self,usrId,pwd,indexName):
        body={
            "query":{
                "bool":{
                    "must":{
                        "term":{
                                "usr":usrId,
                                
                            },
                        "term":{
                                "pwd":pwd
                            }
                            
                    }
                }
                
            }
        }

        if self.es.search(index=indexName,body=body)['hits']['total']['value']==0:
            return {"statue":12}
        else:
            return {"statue":13}

class UsrTableEsConnect(esConnect):
    def __init__(self):
        super().__init__()
    
    def CheckUsrIsExist(self,usrId,indexName):
        body={
            "query":{
                "term":{
                    "usr":usrId
                }
            }
        }
        if self.es.search(index=indexName,body=body)['hits']['total']['value']==0:
            return False
        else:
            return True
    
    def GetUsrProfile(self,usrId,indexName):
        body={
            "query":{
                "term":{
                    "usr":usrId
                }
            }
        }

        return self.es.search(index=indexName,body=body)['hits']['hits'][0]['_id'],self.es.search(index=indexName,body=body)['hits']['hits'][0]['_source']['profile']

    def AddUserProfile(self,usrId,profile,indexName):
        """
        14:update successful
        15:update failed
        16:error profile
        17:delete succes
        18:delete failed
        19:error delete,unexist usr
        """
        if self.CheckUsrIsExist(usrId,indexName):
            id,profiles=self.GetUsrProfile(usrId,indexName)

            profiles.append(profile)

            body={
                    "doc":{
                        "profile":profiles
                    }
                }

            if self.es.update(index=indexName,body=body,id=id)['result']=="updated":
                return {"statue":14}
            else:
                return {"statue":15}
        else:
            profiles=[profile]
            body={
                    "usr":usrId,
                    "profile":profiles
                }
            if self.es.index(index=indexName,body=body)['result']=="created":
                return {"statue":10}
            else:
                return {"statue":11}
    
    def DeleteUserProfile(self,usrId,profile,indexName):
        if self.CheckUsrIsExist(usrId,indexName):
            id,profiles=self.GetUsrProfile(usrId,indexName)

            if profile in profiles:
                #递归删除后续内容
                indexName="{}_{}".format(usrId,profile)
                temp=CommodityEsConnect()
                asin=temp.CheckAsin(usrId,profile)

                for i in asin:
                    dataframeIndexName="{}_{}".format(indexName,asin.lower())
                    temp.DeleteIndex(dataframeIndexName)
                self.DeleteIndex(indexName)

                if len(profiles)>1:
                    profiles.remove(profile)
                    body={
                        "doc":{
                            "profile":profiles
                        }
                    }
                    if self.es.update(index=indexName,body=body,id=id)['result']=="updated":
                        return {"statue":17}
                    else:
                        return {"statue":18}
                else:
                    if self.es.delete(index=indexName,id=id)['result']=="deleted":
                        return {"statue":17}
                    else:
                        return {"statue":18}
            else:
                return {"statue":16}
        else:
            return {"statue":19}

class  CommodityEsConnect(esConnect):
    """
    20:add commodity success
    21:add commodity failed
    """
    def __init__(self):
        super().__init__()

    def CheckAsin(self,usrID,profile):
        indexName="{}_{}".format(usrID,profile)

        body={
                "query":{
                    "terms":{
                       "usrID":usrID 
                    }
            }
            }
        res = self.es.search(index=indexName,body=body)

        asin=[]
        for i in res['hits']['hits']:
            asin.append(i['_source']['asin'])
        return asin
    
    def GetUserInfo(self,usrID,profile):
        indexName="{}_{}".format(usrID,profile)
        body={
                "query":{
                    "term":{
                        "usrID":usrID
                    }
            }
            }
        
        return self.es.search(index=indexName,body=body)['hits']['hits']

    def CheckAsinIsExist(self,usrID,profile,asin):
        indexName="{}_{}".format(usrID,profile)
        body={
            "query":{
                "term":{
                    "asin":asin
                }
            }
        }
        if self.es.search(index=indexName,body=body)['hits']['total']['value']==0:
            return False
        else:
            return True

    def AddCommodity(self,asin,usrID,detail,profile,topicWord,reviewData,posRating):
        try:
            indexName="{}_{}".format(usrID,profile)
            dataframeIndexName="{}_{}".format(indexName,asin.lower())

            if self.CheckIndexIsExist(indexName)["statue"]!=5:
                self.CreateIndex(indexName)
            body={
                "usrID":usrID,
                "asin":asin,
                "detail":detail,
                "topicword":topicWord,
                "posrating":posRating
            }
            body2={
                "query":{
                    "term":{
                        "asin":asin
                    }
                }
            }
            if self.CheckAsinIsExist(usrID,profile,asin):
                self.es.update(index=indexName,body=body,id=self.es.search(index=indexName,body=body2)['hits']['hits'][0]['_id'])
            else:
                self.es.index(index=indexName,body=body)

            if self.CheckIndexIsExist(dataframeIndexName)["statue"]==5:
                self.DeleteIndex(dataframeIndexName)
            
            self.CreateIndex(dataframeIndexName)

            ep = es_pandas(self.es_host)
            ep.to_es(reviewData, dataframeIndexName, doc_type="_doc", thread_count=2, chunk_size=10000)

            return {"statue":20}
        except:
            return {"statue":21}
    
    def DeleteCommodity(self,usrID,profile,asin):
        indexName="{}_{}".format(usrID,profile)
        dataframeIndexName="{}_{}".format(indexName,asin.lower())

        self.DeleteIndex(dataframeIndexName)

        body={
            "query":{
                "term":{
                    "asin":asin
                }
            }
        }

        id=self.es.search(index=indexName,body=body)['hits']['hits'][0]['_id']

        if self.es.delete(index=indexName,id=id)['result']=="deleted":
            return {"statue":17}
        else:
            return {"statue":18}
    
    def QueryCommodity(self,usrID,profile,asin,attibute,tag):
        indexName="{}_{}".format(usrID,profile)
        dataframeIndexName="{}_{}".format(indexName,asin.lower())
        if tag==1:
            body={
                "query":{
                    "range":{
                        attibute:{
                            "gt":0
                        }
                    }
            }
            }
            res = self.es.search(index=dataframeIndexName,body=body)

            review=[]
            for i in res['hits']['hits']:
                review.append(i['_source']['review'])
            return review
        
        elif tag==-1:
            body={
                "query":{
                    "range":{
                        attibute:{
                            "lt":0
                        }
                    }
            }
            }
            res = self.es.search(index=dataframeIndexName,body=body)

            review=[]
            for i in res['hits']['hits']:
                review.append(i['_source']['review'])
            return review
        
        else:
            return [""]



if __name__=="__main__":
    es=CommodityEsConnect()
    a=es.GetUserInfo("abc","cms5058122924439")
    print(a)


