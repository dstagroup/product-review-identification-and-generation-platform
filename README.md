# Product-review-identification-and-generation-platform

## Team Members

- Yong Wu (yong.wu@stud.uni-heidelberg.de) 
- Jiufeng Li (jiufeng.li@stud.uni-heidelberg.de) 
- Ke Ren (ke.ren@stud.uni-heidelberg.de) 
- Yu Wang (yu.wang01@stud.uni-heidelberg.de) 

## Project Discription

Process the review text of Amazon and deduce the emotional tendency in the review text. Based on the inference results, the valuable texts are classified to help consumers make good shopping decisions. In addition, it can also help identify the validity of reviews and help consumers to judge the authenticity of reviews. 

If we have enough time, we will try to expand an automatic review generation functionality which allows users to generate a review by simply submitting the items they want to review. 

## Project State

### Current State

We are struggling for fetching the evaluations of iPhones from Amazon. We have collected 100 reviews of iPhone 14. These evaluations will be used for our deeper analysis. 

### Planning State

We are trying to integrate the code, in order to provide an interface of the crawler for users so people can fetch whaterver they want. The next step is to organize the evaluations in Elasticsearch by size, color, service provider, and product grade after the crawled data is first categorized by Brand ModelName to form a broad category.

### Future Planning

1. Data cleanup and deduplication
   To start, duplicate comments must be eliminated. Additionally, assessments that are too brief typically lack information, thus these facts are eliminated. Then, utilize the ratings as labels, using 1-2 stars for the data set of negative reviews and 3-5 stars for the data set of favorable reviews. Here, there might be a category imbalance issue, which might then require human labeling etc.
2. Tokenization and deactivation
   The tokenization and deactivation tables here will use common word lists, the dictionaries that come with the open source thesaurus, and will add custom words as required. In particular, for short texts, we may introduce Internet buzzwords, words that differ significantly from the traditional definition.
3. Normalisation
   Considering the global nature of the Amazon platform, the reviews may include a variety of languages, so reviews other than English will be blocked out and only English reviews will be considered for the time being. In addition, reviews may include emojis, face emoticons, etc., which will need to be removed. Lowercase all comments. Replace word abbreviations. Convert word numbers to Arabic numerals. Replacement of special symbols. Spelling corrections etc. These will all be further normalised to the text as appropriate. Most of these can be assisted by open source libraries.
4. Lemmatization and stemming
   As the sentiment analysis we do is more focused on natural language processing, we need more accurate text analysis and representation. Therefore, we do not consider introducing stemming for the time being. The main focus is on the implementation of Lemmatization, and this step of the open source library can be very helpful in accomplishing this task.
5. Part-of-Speech (PoS)
   Here again we will call the python open source library **nltk** to assist with this. Once this is done, we will have the list of serialised words.
6. Data format
   Here we use the **Word2Vec** method to transform the word sequences processed in the above steps into word vectors. PCA is then used to reduce the dimensionality of the data to avoid long training times for multi-dimensional features.
7. Model training
    Here we use the SVM method, which divides the previously constructed dataset into a training set and a test set, and use a ten-fold cross-test to train the model and test its performance.
8. Model Deployment
    The trained model is deployed to the server and the web framework is built via FastApi, using Svelte as the front end. Of course, if we have enough time, we can develop a local application with an embedded CEF to call the web framework, making it easier and faster to call the model.

### Data Analysis

- Data Sources

  Amazon: We fetch the evaluations of iPhones from Amazon. First, as the product's category, the Brand and ModelName may be found in the product interface's details. After that, we can see that each review is extremely formatted, even though we require content like Size, Colour, Service Provider, Product grade, rating, and comments.  Crawlers and regular expressions can retrieve all of this. 
