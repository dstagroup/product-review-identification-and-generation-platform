import json
from collections import Counter
import os

import pandas as pd
import numpy as np
import spacy
import matplotlib
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from collections import Counter

from nltk.corpus import wordnet

get_ipython().run_line_magic('matplotlib', 'inline')




def generate_word_cloud(words_set, i):
    entities_counter = Counter(words_set)
    e_dict = {}
    entities_names = []
    
    for k, v in entities_counter.items():
        if wordnet.synsets(k):
            e_dict[k] = v

    fig = plt.figure(figsize=(5, 3), dpi=200)

    cloud = WordCloud(scale=1, 
                          margin=2,
                          background_color='white',
                          max_font_size=60,
                          random_state=50).generate_from_frequencies(e_dict)
    
    plt.title(i, y=-0.1, size=7)
    plt.axis('off')
    plt.imshow(cloud)
    plt.savefig("../img/"+i+".png")
    


if __name__ == '__main__':
    with open("../data/train_data_clean.json","r",encoding='UTF-8') as f:
        load_dict = json.load(f)
    positive = []
    negative = []
    neutral = []
    for i in load_dict['data']:
        if i['Rating'] == 1:
            positive.extend(i['Review'])
        if i['Rating'] == -1:
            negative.extend(i['Review'])
        if i['Rating'] == 0:
            neutral.extend(i['Review'])

    emotions = ['positive', 'negative', 'neutral']
    
    words_list = []
    words_list.append(positive)
    words_list.append(negative)
    words_list.append(neutral)
    for i in range(3):
        generate_word_cloud(words_list[i], emotions[i])




