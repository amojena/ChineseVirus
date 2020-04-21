import tweepy
import json
import time
from CSVManager import CSVManager

class TweetManager:
    def __init__(self):
        self.setup()
        self.csvMan = CSVManager()
        self.tweets = self.csvMan.read() # {tweet: date}
        self.getHistory()

    def setup(self):
        with open("twitter-creds.json", "r") as f:
            keys = json.load(f)
        auth = tweepy.OAuthHandler(keys["api_key"], keys["api_secret_key"])
        auth.set_access_token(keys["access_token"], keys["access_token_secret"])
        self.api = tweepy.API(auth,wait_on_rate_limit=True)
    
    def getHistory(self):
        self.queries = set()
        try:
            with open("past_queries.txt", 'r') as f:
                self.queries = set(f.readlines())

            if len(self.tweets) < 1 or len(self.queries) == 0: raise Exception
            print("There are a total of {} tweets from the queries: {}".format(len(self.tweets), ''.join(self.queries)))
        
        except:
            print("No queries have been made.")


    def write(self):
        self.csvMan.write(self.tweets)
        with open("past_queries.txt", 'w') as f:
            f.writelines(self.queries)
    
    # Tries to find the recent count tweets when textQuery is searched
    # TODO: Automate so it searches until it is actually able to get count tweets (using pages or unique id)
    # TODO: Either filter out RTs or find universal json attribute for date of either original tweet or RT
    def query(self, textQuery, count):
        try:
            # Pulling individual tweets from query
            for tweet in self.api.search(q=textQuery, count=count, lang='en'):
                t = tweet.text.replace('\n', ' ')
                date = tweet._json['created_at']
                if self.tweets.get(t) is None:
                    self.tweets[t] = date
            self.queries.add(textQuery)

        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
            return

    def getTrumpTweets(self):
        tweets = []
        username = 'realDonaldTrump'
        count = 3200
        last_id = 1241565348765347841 # Unique ID of a tweet from April 10

        try:
            for tweet in self.api.user_timeline(id=username, count=count, max_id=last_id):
                tweets.append(tweet)
        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
            return