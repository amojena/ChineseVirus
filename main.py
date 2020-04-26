from TweetManager import TweetManager

if __name__ == "__main__":
    tweetMan = TweetManager()
    tweetMan.query("Chinese Virus", 2000)
    tweetMan.bookmark()