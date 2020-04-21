import tweepy
import json
import csv
import time

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
    tweets = set()
    text_query = 'Chinese Virus'
    count = 200
    try:
        # Pulling individual tweets from query
        for tweet in api.search(q=text_query, count=count, lang='en', until="2020-04-12"):
            #  Adding to list that contains all tweets
             tweets.add(tweet.text.replace('\n', ' '))
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)
        return
    
    filename = "test_tweets.csv"
    output_to_csv(tweets, filename)
    

def output_to_csv(tweets,filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Count', 'Tweet'])
        for i, tweet in enumerate(tweets):
            writer.writerow([i, tweet])

def get_trump_tweets():
    tweets = []
    username = 'realDonaldTrump'
    count = 3200
    last_id = 1241565348765347841 #april 10

    try:
        for tweet in api.user_timeline(id=username, count=count, max_id=last_id):
            tweets.append(tweet)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)
        return
    
    filename = "test_trump.csv"

    for t in tweets[-100:]:
        print(t._json['created_at'], t._t)


if __name__ == "__main__":
    print("Hello Nick!")
    _, api = setup()
    # test_run(api)
    get_trump_tweets()
