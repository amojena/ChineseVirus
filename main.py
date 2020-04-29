from TweetManager import TweetManager
import sys

if __name__ == "__main__":
    qTerm = sys.argv[1]
    tweetMan = TweetManager()
    tweetMan.query(qTerm, 3200)
    tweetMan.write()
