import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
#from random import sample
from collections import defaultdict
import re
from nltk.corpus import stopwords



USER = '_@user_'
HTTP = '_web_'

coronavirus = '#coronavirus'
chinese_virus = '#chinesevirus'
wuhan_virus = '#wuhanvirus'
covid19 = '#covid19'

hts = [ coronavirus, chinese_virus, wuhan_virus, covid19]

stop_words = set(stopwords.words('english'))
filter_words = set(['chinese', 'virus', 'wuhan', 'china', 'coronavirus' , 'rt', USER, HTTP,
                     'covid', '19' 'covid19'])

# Load from csv, replacing user tags and hyperlinks with generic labels. Also
# removing punctuation, lowercasing, and tokenizing.
def load_tweets(fname):
    tweets = pd.read_csv(fname, names=['date','sep','tweet'])
    tweets = tweets['tweet']
    punc_reg = '[.?!,\'\`\"\-\&\:\;\(\)]+'

    for i, tweet in enumerate(tweets):
        tweet = re.sub(punc_reg, '', tweet)
        tokens = [w for w in tweet.lower().split(' ') if w != '']

        for j, w in enumerate(tokens, 0):
            if w[0] == '@':
                tokens[j] = USER
            if w[:4] == 'http':
                tokens[j] = HTTP
        tweets[i] = tokens

    return tweets


# Remove generic stopwords from tweets as well as some highly common key words that were muting other
# signals in the data. Could remove that part depending on use case.
def clean(tweets):
    return [[w for w in tweet if w not in stop_words and w not in filter_words] for tweet in tweets]


# Build a list of frequency tables. The first one is a dict of hashtag counts while
# the second is a list of word counts.
def freq_dicts(tweets):
    hashtags, words = defaultdict(int), defaultdict(int)

    for tweet in tweets:
        for w in tweet:
            if w[0] == '#':
                hashtags[w] += 1
            else:
                words[w] += 1
    return hashtags, words

# Takes in a dictionary of word frequency counts and returns a tuple sorting
# those words from most to least common.
def sort_freq_dict(freqs):
    pairs = list(freqs.items())
    pairs.sort(key=lambda p: p[1], reverse=True)
    return pairs

# Return a subset of the tweet set that contains a certain key word
def keyword_search(tweets, keyword):
    return [tweet for tweet in tweets if keyword in tweet]

# Return sorted word/hashtag frequencies for a set of tweets with a given keyword
def keyword_analysis(tweets, keyword):
    hits = keyword_search(tweets, keyword)
    hashtags, words = freq_dicts(hits)

    top_hashtags, top_words = sort_freq_dict(hashtags), sort_freq_dict(words)

    return top_hashtags, top_words


if __name__ == '__main__':
    tweets = load_tweets('tweet_data.csv')
    tweets_clean = clean(tweets)

    # Get frequency dicts for entire data set and their sorted counts
    hashtags, words = freq_dicts(tweets_clean)
    hashtag_counts = sort_freq_dict(hashtags)
    word_counts = sort_freq_dict(words)

    # get a list of frequency arrays for tweets with a certain keyword. 'hts'
    # is a list of relevant hashtags. Goal was to compare the common words associated
    # with #covid19 and with #chinesevirus, for example
    keyword_results = [keyword_analysis(tweets_clean, ht) for ht in hts]

    coronavirus_words = set([wc[0] for wc in keyword_results[0][1] if wc[1] > 1])
    chinese_virus_words = set([wc[0] for wc in keyword_results[1][1]])
    covid19_words = set([wc[0] for wc in keyword_results[3][1]])

    # venn diagram of words found with #covid19 but not with #chinesevirus and vice versa
    venn = (covid19_words - chinese_virus_words, chinese_virus_words - covid19_words)
