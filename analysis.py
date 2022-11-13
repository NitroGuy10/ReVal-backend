import pandas as pd
from summa import keywords
from sentiment import get_sentiment
from io import StringIO
from nltk.stem import PorterStemmer
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

def mentions_of (json_str, keywords):    
    print("BINGUS!!!!!")
    # df = pd.read_json('input/data/by_product/140053271X.json', orient="records", encoding = 'UTF-8')
    df = pd.read_json(json_str, orient="index", encoding='UTF-8')

    tempView = df
    for keyword in keywords:
        tempView = tempView[df.reviewText.str.contains(keyword)]

    return json.loads(tempView.to_json(orient='records'))

