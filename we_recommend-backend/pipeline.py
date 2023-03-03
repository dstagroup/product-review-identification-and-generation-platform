import json
import LDAModel
import ABSAModel
import preprocess
import elasticSearchApi

def GenerateFinalResult(data):
    # rating_dict_count = {}
    # rating_dict = {}
    # rating_positive_dict = {}
    # average_type = {}
    # sum = 0
    count = 0

    listt = []
    listt = data['reviews']
    list_len = len(listt)

    for review in data['reviews']:
        if review['rating'] >=3:
            count = count + 1

        # for key, value in review.items():
        #     len()
        #     if key != 'review' and key != 'title' and key != 'review':
        #         if key in rating_dict.keys():
        #             rating_dict[key] = rating_dict[key] + review[key]
        #             rating_dict_count[key] = rating_dict_count[key] + 1
        #
        #             if review[key] >= 3:
        #                 if key not in rating_positive_dict.keys():
        #                     rating_positive_dict[key] = 1
        #
        #                 rating_positive_dict[key] = rating_positive_dict[key] + 1
        #
        #         if key not in rating_dict.keys():
        #             rating_dict[key] = review[key]
        #             rating_dict_count[key] = 1
        #
        #         count = count + 1
        #         sum = sum + review[key]

    sum_average_type = 5 * count / list_len

    # summ = 0
    # for k, v in rating_dict_count.items():
    #     summ = summ + rating_dict_count[k]
    #
    # single_property_rating = {}
    # for k, v in rating_dict.items():
    #     if k in rating_positive_dict.keys():
    #         average_type[k] = 5 * (rating_positive_dict[k] / summ)
    #         single_property_rating[k] = 5 * (rating_positive_dict[k] / rating_dict_count[k])
    #     else:
    #         average_type[k] = 0
    #
    # for k, v in average_type.items():
    #     sum_average_type = sum_average_type + average_type[k]
    #
    # single_asin_dict = {}
    # single_asin_dict['asin'] = data['asin']
    # single_asin_dict['total_average_rating'] = sum_average_type
    # single_asin_dict['single_property_rating'] = single_property_rating

    return sum_average_type

def Pipeline(reviewJson):
    asin,usrID,detail,profile,reviewData=preprocess.Json2Dataframe(reviewJson)
    reviewData["cleanReview"]=reviewData.apply(preprocess.Preprocess,axis=1)
    topicWord=LDAModel.LDA(reviewData)
    reviewData,posRating=ABSAModel.Predict(reviewData)

    es=elasticSearchApi.CommodityEsConnect()
    result = es.AddCommodity(asin,usrID,detail,profile,topicWord,reviewData,posRating)
    return result

if __name__=="__main__":
    reviewJson=preprocess.LoadJson(r"/Users/uu/Documents/product-review-identification-and-generation-platform-main 2/pipeline&elasticsearch/input_data/final.json")
    Pipeline(reviewJson)