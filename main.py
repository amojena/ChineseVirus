from TweetManager import TweetManager
import sys

if __name__ == "__main__":
    qTerm = sys.argv[1]
    tweetMan = TweetManager()

    while True:
        query = input("Enter keyword search to query: ")
        if query == "kill": exit(0)
        if query == "exit": break
        tweetMan.query(query, 2000)

    tweetMan.bookmark()
