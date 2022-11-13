import pandas as pd
from summa import keywords
from sentiment import get_sentiment
from io import StringIO
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.corpus import wordnet
import json


def create_product_df (json_str):    
    # df = pd.read_json('input/data/by_product/140053271X.json', orient="records", encoding = 'UTF-8')
    df = pd.read_json(json_str, orient="records", encoding='UTF-8')
    print(df.head())
    print(df.columns)

    df = df.drop('reviewTime', axis = 1)
    if "image" in df.columns:
        df = df.drop('image', axis = 1)
    df = df.drop('verified', axis = 1)
    df = df.drop('reviewerID', axis = 1)
    df["index"] = range(len(df.index))

    summaKeyWords = []
    sentiments = []
    for text in df['reviewText']:
        if(type(text) != str):
            summaKeyWords.append(None)
            sentiments.append(0)
        else:
            TR_keywords = keywords.keywords(text, scores=True, ratio=0.9)
            summaKeyWords.append([i[0] for i in TR_keywords])
            sentiments.append(get_sentiment(text))


    df["summaKeyWords"] = summaKeyWords
    df["sentiment"] = sentiments
    # print(df.head())
    # print(df.columns)

    return df

def create_product_df_json (json_str):
    df = create_product_df(json_str)
    return df.to_json(orient='index')

def mentions_of (json_str, keywords, or_search=False):    
    print("BINGUS!!!!!")

    keywords_synonyms = []
    for keyword in keywords:
        for syn in wordnet.synsets(keyword):
            for l in syn.lemmas():
                keywords_synonyms.append(l.name())

    # df = pd.read_json('input/data/by_product/140053271X.json', orient="records", encoding = 'UTF-8')
    df = pd.read_json(json_str, orient="index", encoding='UTF-8')

    ps = PorterStemmer()
    df["reviewTextStemmed"] = df["reviewText"].map(lambda text: " ".join([ps.stem(word.lower()) for word in word_tokenize(text)]))
    #print(df["reviewTextStemmed"].head())

    indices_to_include = set()
    if or_search:
        for keyword in keywords:
            keyword_stemmed = ps.stem(keyword)
            indices = df[df.reviewText.str.contains(keyword) | df.reviewText.str.contains(keyword_stemmed) | df.reviewTextStemmed.str.contains(keyword_stemmed)].index
            for index in indices:
                indices_to_include.add(int(index))
    else:
        hits = {}
        for keyword in keywords:
            keyword_stemmed = ps.stem(keyword)
            indices = df[df.reviewText.str.contains(keyword) | df.reviewText.str.contains(keyword_stemmed) | df.reviewTextStemmed.str.contains(keyword_stemmed)].index
            for index in indices:
                if int(index) in hits:
                    hits[int(index)] += 1
                else:
                    hits[int(index)] = 1
        for hit in hits:
            if hits[hit] == len(keywords):
                indices_to_include.add(hit)

    # SYNONYMS!!!
    synonym_indices = set()
    synonym_indices_to_include = set()
    for keyword in keywords_synonyms:
            keyword_stemmed = ps.stem(keyword)
            indices = df[df.reviewText.str.contains(keyword) | df.reviewText.str.contains(keyword_stemmed) | df.reviewTextStemmed.str.contains(keyword_stemmed)].index
            for index in indices:
                synonym_indices.add(int(index))
    for index in synonym_indices:
        if index not in indices_to_include:
            synonym_indices_to_include.add(index)


    return json.loads(df.iloc[list(indices_to_include)].to_json(orient='records')) + json.loads(df.iloc[list(synonym_indices_to_include)].to_json(orient='records'))

def evaluation(json_str, key):
    df = pd.read_json(json_str, orient="index", encoding='UTF-8')
    ps = PorterStemmer()

    all_keywords = {}
    # keyword_stems = {}
    for i in range(len(df["summaKeyWords"].index)):
        keywords_list = df["summaKeyWords"][i]

        if type(keywords_list) == str:
            keywords_list = [keywords_list]

        if type(keywords_list) == list:
            for keyword in keywords_list:
                # if keyword not in keyword_stems:
                #     keyword_stems[keyword] = ps.stem(keyword)

                if keyword in all_keywords:
                    all_keywords[keyword][1].append(df["index"][i])
                else:
                    all_keywords[keyword] = (get_sentiment(keyword), [df["index"][i]])
        
    all_keywords_list = [(kw, info) for kw, info in all_keywords.items()]
    all_keywords_list.sort(reverse=True, key=lambda keyword: len(keyword[1][1]))
    # print(all_keywords_list)

    top10Overall = []
    top10Positive = []
    top10Negative = []
    for keyword_item in all_keywords_list:
        kw_word = keyword_item[0]
        kw_sentiment = keyword_item[1][0]
        kw_reviews = [int(num) for num in keyword_item[1][1]]
        kw_object = {"keyword": kw_word, "sentiment": kw_sentiment, "reviewsMentionedIn": kw_reviews}
        if len(top10Overall) < 10:
            top10Overall.append(kw_object)
        if len(top10Positive) < 10 and kw_sentiment > 0:
            top10Positive.append(kw_object)
        if len(top10Negative) < 10 and kw_sentiment < 0:
            top10Negative.append(kw_object)
    
    top10Positive.sort(reverse=True, key=lambda keyword: keyword["sentiment"])
    top10Negative.sort(key=lambda keyword: keyword["sentiment"])

    # Final thing to return
    evaluation_dict = {
        "dataset_key" : key,
        "reviews": json.loads(df.to_json(orient='records')),
        "keywords": {
            "top10Overall": top10Overall,
            "top10Positive": top10Positive,
            "top10Negative": top10Negative
        }
    }

    return evaluation_dict




