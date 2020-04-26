import tweepy
import json
import time
from math import inf
from CSVManager import CSVManager

class TweetManager:
    def __init__(self):
        self.queryID = dict() # {textQuery : id of most recent tweet}
        self.setup()
        self.csvMan = CSVManager()
        self.tweets = self.csvMan.read() # {tweet: date}
        self.getPastQueries()
        

    def setup(self):
        with open("twitter-creds.json", "r") as f:
            keys = json.load(f)
        auth = tweepy.OAuthHandler(keys["api_key"], keys["api_secret_key"])
        auth.set_access_token(keys["access_token"], keys["access_token_secret"])
        self.api = tweepy.API(auth,wait_on_rate_limit=True)
        print("Authorization succesful...")
    
    def getPastQueries(self):
        print("Getting past queries...")
        try:
            with open("past_queries.txt", 'r') as f:
                for line in f:
                    query, mostRecentId = line.strip().split('\n')
                    self.queryID[query] = int(mostRecentId)
                    self.queries.add(query)

            if len(self.tweets) < 1 or len(self.queries) == 0: raise Exception
            print(" There are a total of {} tweets from the queries: {}".format(len(self.tweets), ', '.join(self.queries)))
        
        except:
            print(" No queries have been made.")

    def bookmark(self):
        print("Bookmarking {} tweets and {} queries...".format(len(self.tweets), len(self.queryID)))
        self.csvMan.write(self.tweets)
        with open("past_queries.txt", 'w') as f:
            for query, t_id in self.queryID.items():
                f.writelines([query, ',', str(t_id)])
    
    # Will get called to update previous queries results, not expected to find count tweets
    def query(self, textQuery, count):
        if self.queryID.get(textQuery) is None: self.queryBulk(textQuery, count)
        else: self.queryUpdate(textQuery, count)

    def queryUpdate(self, textQuery, count):
        print("Update querying: {}".format(textQuery))
        try:
            lastBatch = 0
            while lastBatch < count:
            # Pulling individual tweets from query
                query = self.api.search(q=textQuery, count=count, lang='en', since_id=self.queryID[textQuery], tweet_mode='extended')
                for tweet in query:
                    t = tweet.full_text.replace('\n', ' ')
                    date = tweet._json['created_at']

                    if self.tweets.get(t) is None:
                        self.queryID[textQuery] = max(self.queryID[textQuery], tweet.id)
                        self.tweets[t] = date
                        lastBatch += 1


        except BaseException as e:
            print(' failed on_status,',str(e))
            time.sleep(3)
            return

    # Will get called whenever a completely new query is made
    def queryBulk(self, textQuery, count):
        print("Bulk querying: {}".format(textQuery))
        try:
            lastId = -1
            retweet = False
            while len(self.tweets) < count:
                if lastId != -1:
                    newTweets = self.api.search(q=textQuery, count=count, max_id=str(lastId - 1), tweet_mode='extended')
                else:
                    newTweets = self.api.search(q=textQuery, count=count, tweet_mode='extended')
                    
                if not newTweets:
                    break
                
                lastId = newTweets[0].id

                # Start keeping track of the most recent tweet in the query
                if self.queryID.get(textQuery) is None:
                    self.queryID[textQuery] = lastId
                
                for tweet in newTweets:
                    t = tweet.full_text.replace('\n', ' ')
                    date = tweet._json['created_at']

                    if "RT" == t[:2]:
                        t = "RT: " + tweet._json["retweeted_status"]["full_text"]

                    if self.tweets.get(t) is None:
                        # Tweets are not sorted by ID/date, check ID to find largest one (most recent tweet)
                        self.queryID[textQuery] = max(self.queryID[textQuery], tweet.id)

                        # Tweets are not sorted by ID/date, check ID to find smallest one (earliest tweet)
                        lastId = min(lastId, tweet.id)

                        self.tweets[t] = date
                print(" {} tweets left.".format(count - len(self.tweets)))

        except BaseException as e:
            print(" Failed on status: ",str(e))
            time.sleep(3)
            return