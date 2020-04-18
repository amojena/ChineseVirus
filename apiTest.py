import tweepy
import json
import csv
from time import time

def load_keys(pathname):
    with open(pathname, "r") as f:
        return json.load(f)
    
def setup():
    keys = load_keys("twitter-creds.json")
    auth = tweepy.OAuthHandler(keys["api_key"], keys["api_secret_key"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return auth, api

def test_run(api):
    tweets = []
    text_query = 'Chinese Virus'
    count = 3
    try:
        # Pulling individual tweets from query
        for tweet in api.search(q=text_query, count=count):
            #  Adding to list that contains all tweets
            tweets.append((tweet.text))
            # print(tweet.text)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)
        return
    
    output_to_csv(tweets)
    

def output_to_csv(tweets):
    with open("test_tweets.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Count', 'Tweet'])
        # writer.writerows(tweets)
        for i, tweet in enumerate(tweets):
            writer.writerow([i, tweet])

if __name__ == "__main__":
    print("Hello Nick!")
    _, api = setup()
    test_run(api)
