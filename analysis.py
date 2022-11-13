import pandas as pd
from summa import keywords
from sentiment import get_sentiment

df = pd.read_json('input/data/by_product/140053271X.json', lines = True, encoding = 'UTF-8')


df = df.drop('reviewTime', axis = 1)
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
print(df.head())
print(df.columns)

df.to_json("df.json", 'index')


