from collections import OrderedDict
from textblob import TextBlob

# Sentiment is judged on two factors:
#   polarity (how positive/negative it is) in [-1.0, 1.0]
#       -1 means negative
#       +1 means positive
#   subjectivity (how subjective it is) in [0.0, 1.0]
#       0 means objective
#       1 means subjective


def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return OrderedDict([
        ('polarity', sentiment.polarity),
        ('subjectivity', sentiment.subjectivity)
    ])
