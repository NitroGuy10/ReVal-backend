import json
import gzip
import nltk
import pandas as pd
import nltk.corpus
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import timeit
from keybert import KeyBERT
from summa import keywords

## Open the dataset

# def parse(path):
#   g = gzip.open(path, 'rb')
#   for l in g:
#     yield json.loads(l)

# def getDF(path):
#   i = 0
#   df = {}
#   for d in parse(path):
#     df[i] = d
#     i += 1
#   return pd.DataFrame.from_dict(df, orient='index')

# df = pd.read_json('input/data/Electronics_5_small.json', lines = True)
# df = df[100:]
# df = df.drop('reviewTime', axis = 1)

# print(df.head())

## NLTK experimentation

# stopwords = set(nltk.corpus.stopwords.words("english"))

# sentence = "I might be gone for long, but long's just a piece of eternity. So just wait for me."
# sentence = "unbelievably happy"
# sentence_tokens = nltk.word_tokenize(sentence)
# filtered_tokens = []

# for token in sentence_tokens:
#     if token not in stopwords and token.isalpha():
#         filtered_tokens.append(token.lower())

# print(filtered_tokens)



## Sentiment analysis

# sid = SentimentIntensityAnalyzer()
# polarity_scores = sid.polarity_scores(sentence)
# print(polarity_scores)


# df = pd.read_json('Electronics_5_small.json', lines = True, encoding = 'UTF-8')
df = pd.read_json('input/data/by_product/140053271X.json', encoding = 'UTF-8')


df = df.drop('reviewTime', axis = 1)
df = df.drop('image', axis = 1)
print(df.head())
print(df.columns)

# df = pd.DataFrame(df[:100])

summaKeyWords = []
count = 0
for text in df['reviewText']:
    print(count)
    if(type(text) != str):
        print(type(text))
        summaKeyWords.append(None)
    else:
        TR_keywords = keywords.keywords(text, scores=True)
        print(text)
        tempArray = []
        for i in TR_keywords:
            tempArray.append(i[0])
        summaKeyWords.append(tempArray)
    count += 1


keyBERTWords = []
kw_model = KeyBERT(model='all-mpnet-base-v2')





for text in df['reviewText']:
    print(count)
    start = timeit.default_timer()

    keywords = kw_model.extract_keywords(text, 

                                        keyphrase_ngram_range=(1, 3), 

                                        stop_words='english', 

                                        highlight=False,

                                        top_n=15)

    keywords_list= list(dict(keywords).keys())
    keyBERTWords.append(keywords_list)
    count += 1
    stop = timeit.default_timer()

    print('Time: ', stop - start)   

df["summaKeyWords"] = summaKeyWords
df["keyBERTWords"] = keyBERTWords



#  140053271X.json





