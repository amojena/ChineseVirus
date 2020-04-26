import csv

class CSVManager:
    def __init__(self):
        self.delimeter = " --> "

    def cleanText(self, text):
        return text.replace(',', '').replace('\n', ' ').replace('\"', '')
    
    def parseTweet(self, tweet):
        return tweet[0].replace(',', ''), self.cleanText(tweet[2]), tweet[1][4:].replace(' ', '')

    def read(self, filename="tweet_data.csv"):
        print("Getting all queried tweets...")
        tweets = dict()
        try:
            with open(filename, 'r') as f:
                for row in f:
                    tweet = row.split(self.delimeter)
                    date, text, rts = self.parseTweet(tweet)
                    tweets[text] = [date, rts]
        except:
            print(" Error {} does not exist".format(filename))
        print(" {} tweets were saved last session.".format(len(tweets)))
        return tweets

    def write(self, tweets, filename="tweet_data.csv"):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for tweet, info in tweets.items():
                date, rts = info[0], info[1]
                writer.writerow([date, self.delimeter, "RTs: {}".format(rts), self.delimeter, self.cleanText(tweet)])