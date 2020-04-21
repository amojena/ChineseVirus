import csv

class CSVManager:
    def __init__(self):
        self.delimeter = " --> "

    def cleanText(self, text):
        return text.replace(',', '').replace('\n', '').replace('\"', '')

    def read(self, filename="tweet_data.csv"):
        tweets = dict()
        try:
            with open(filename, 'r') as f:
                for row in f:
                    tweet = row.split(self.delimeter)
                    if len(tweet) != 2: raise Exception
                    date, text = tweet[0].replace(',', ''), self.cleanText(tweet[1])
                    tweets[text] = date
        except:
            print("Error".format(filename))
        print("{} tweets were saved last session.".format(len(tweets)))
        return tweets

    def write(self, tweets, filename="tweet_data.csv"):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for tweet, date in tweets.items():
                writer.writerow([date, self.delimeter ,tweet])