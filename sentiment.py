from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()


def get_sentiment_full(text):
    return sid.polarity_scores(text)

def get_sentiment(text):
    return get_sentiment_full(text)["compound"]
