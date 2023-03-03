import json

def LoadJson(path):
    """
    this function is for local text
    """
    with open(path, 'r', encoding="utf-8") as f:
        reviewJson = f.read()
        reviewJson = json.loads(reviewJson)

    return reviewJson

def AnalyseRating(data):
    rating_dict_count = {}
    rating_dict = {}
    rating_positive_dict = {}
    average_type = {}
    sum = 0
    count = 0
    for review in data['review']:
        for key, value in review.items():
            if key != 'review':
                if key in rating_dict.keys():
                    rating_dict[key] = rating_dict[key] + review[key]
                    rating_dict_count[key] = rating_dict_count[key] + 1

                    if review[key] >= 3:
                        if key not in rating_positive_dict.keys():
                            rating_positive_dict[key] = 1

                        rating_positive_dict[key] = rating_positive_dict[key] + 1

                if key not in rating_dict.keys():
                    rating_dict[key] = review[key]
                    rating_dict_count[key] = 1

                count = count + 1
                sum = sum + review[key]

    sum_average_type = sum / count

    summ = 0
    for k, v in rating_dict_count.items():
        summ = summ + rating_dict_count[k]

    single_property_rating = {}
    for k, v in rating_dict.items():
        if k in rating_positive_dict.keys():
            average_type[k] = 5 * (rating_positive_dict[k] / summ)
            single_property_rating[k] = 5 * (rating_positive_dict[k] / rating_dict_count[k])
        else:
            average_type[k] = 0

    for k, v in average_type.items():
        sum_average_type = sum_average_type + average_type[k]

    single_asin_dict = {}
    single_asin_dict['asin'] = data['asin']
    single_asin_dict['recommend_rating'] = sum_average_type
    single_asin_dict['single_property_rating'] = average_type
    single_property_rating['topic_words'] = data['topicwords']



    return single_asin_dict



if __name__=="__main__":
    data = LoadJson("/Users/uu/dsta_project/product-review-identification-and-generation-platform-main/model/B0B3C57XLR_Result.json")

    data2 = AnalyseRating(data)
    return_json = json.dumps(data2)
    print(return_json)

    with open("{}_Result2.json".format('1234'),'w',encoding='utf-8') as f:
        json.dump(return_json, f,ensure_ascii=False)