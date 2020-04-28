from TweetManager import TweetManager

if __name__ == "__main__":
    tweetMan = TweetManager()

    while True:
        query = input("Enter keyword search to query: ")
        if query == "kill": exit(0)
        if query == "exit": break  
        tweetMan.query(query, 2000)

    tweetMan.bookmark()