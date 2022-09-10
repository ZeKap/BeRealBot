import tweepy

from tokens import apiKey, apiSecret, accessToken, accessSecret

from random import randrange
import time

# vars for prog
debug = False
maxTweets = 5
minTweets = 1
moments = []

# try to connect with tweepy api
def connect_api():
    auth = tweepy.OAuthHandler(apiKey, apiSecret)
    auth.set_access_token(accessToken, accessSecret)

    global api  # declare global var api to send tweet in others func
    api = tweepy.API(auth)

    try:    # try to connect and exit in case of error
        api.verify_credentials()
        if(debug): print("Tweepy credentials are ok")
    except:
        print("Error in tweepy")
        exit(2)

# generate a random moment in day
def random_moment() -> str:
    hour = randrange(0, 23)     # random hour
    minute = randrange(0, 59)   # random minute
    if(hour) < 10: hour = '0' + str(hour)       # store in str and add '0' if < 10
    else: hour = str(hour)
    if(minute) < 10: minute = '0' + str(minute) # store in str and add '0' if < 10
    else: minute = str(minute)
    return hour + ":" + minute  # return in format '00:00'

# generate random number of tweets in the day
def nb_tweets() -> int:
    return randrange(minTweets, maxTweets)

# tweet a tweet
def make_a_tweet():
    from tweets import tweetsList                   # get list of tweets possible
    tweet = tweetsList[randrange(len(tweetsList))]  # get random tweet from tweet list
    if('lastTweet' in globals()):                   # if there is a last tweet available
        while(tweet == lastTweet):                  # while the new tweet is the same as the old one
            tweet = tweetsList[randrange(len(tweetsList))]  # take a tweet
    lastTweet = tweet                               # store new tweet in lastTweet
    if(debug): print("Tweet: " + tweet)
    api.update_status(tweet)                        # tweet a tweet

# generate a random number of jobs
def create_moments():
    if(debug): print("clearing jobs")
    moments.clear()                             # remove every entry in the list
    for _ in range(nb_tweets()):
        moments.append(random_moment())         # add a random moment to the list
    if(debug): print(moments)

if(__name__ == "__main__"):
    connect_api()                               # connect to tweepy API
    create_moments()                            # create jobs
    while True:
        currentTime = time.strftime("%H:%M")    # get current time
        if(currentTime in moments):             # if it's time to do a tweet
            make_a_tweet()                      # do a tweet
        if(currentTime == "00:00"):             # if it's midnight
            create_moments()                    # delete and recreate random schedule jobs
        time.sleep(50)                          # sleep for 50 seconds before retrying