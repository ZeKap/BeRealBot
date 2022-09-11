import tweepy

from tokens import apiKey, apiSecret, accessToken, accessSecret

from random import randrange
import time

# vars for prog
debug = False
minDays = 2
maxDays = 4
lastTweet = ""

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

# tweet a tweet
def make_a_tweet():
    if(debug): print("Tweeting")
    from tweets import tweetsList                   # get list of tweets possible
    tweet = tweetsList[randrange(len(tweetsList))]  # get random tweet from tweet list
    global lastTweet
    while(tweet == lastTweet):                      # while the new tweet is the same as the old one
        tweet = tweetsList[randrange(len(tweetsList))]  # take an other tweet
    lastTweet = tweet                               # store new tweet in lastTweet
    if(debug): print("Tweet: " + tweet)
    api.update_status(tweet)                        # tweet a tweet

# generate random number of days in the week
def nb_days() -> int:
    if(debug): print("Generating random number of days")
    return randrange(minDays, maxDays)

# generate a random day without being in the list
def random_day(addedList) -> int:
    if(debug): print("Picking a random day")
    nb = randrange(1, 8)
    while(nb in addedList):
        nb = randrange(1, 8)
    return nb

# generate a random moment in day
def random_hour() -> str:
    if(debug): print("Generating random moment")
    hour = randrange(0, 24)                     # random hour
    minute = randrange(0, 60)                   # random minute
    if(hour) < 10: hour = '0' + str(hour)       # store hour in str and add '0' if < 10
    else: hour = str(hour)
    if(minute) < 10: minute = '0' + str(minute) # store minute in str and add '0' if < 10
    else: minute = str(minute)
    return hour + ":" + minute                  # return in format 'HH:MM'

# generate a list of days to tweet
def create_days():
    if(debug): print("Creating a list of random days")
    days = []                               # list of days to tweet
    if(debug): print("clearing days")
    days.clear()                            # clear the list
    for _ in range(nb_days()):              # add a random number of day
        days.append(random_day(days))       # add a random day to the list without double
    if(debug): print(days)
    return days

if(__name__ == "__main__"):
    connect_api()                                       # connect to tweepy API
    days = create_days()                                # create list of days to tweet
    tweeted = False
    while True:
        if(debug): print("Starting loop")
        currentDay = int(time.strftime("%u"))           # get current day
        if(currentDay in days):                         # if it's a day to tweet
            hour = random_hour()                        # take a random moment in day
            if(debug): print(hour)
            while(not tweeted):                         # while there was no tweet
                if(debug): print("current day is in days: "+time.strftime("%u"))
                #use while instead
                while(time.strftime("%H:%M") != hour):  # check if it's time to do a tweet
                    if(debug): print("not time to do a tweet")
                    time.sleep(50)                      # sleep for 50 seconds before retrying
                if(debug): print("time to tweet")
                make_a_tweet()                          # do a tweet
                tweeted = True
                # sleep until end of day
                if(debug): print("sleep until end of day")
                time.sleep(((23-int(time.strftime("%H")))*60*60)+((59-int(time.strftime("%M")))*60)+(58-int(time.strftime("%S"))))
                while(time.strftime("%H:%M") != "00:00"):# while it's not the end of the day
                    if(debug): print("sleep until end of day but precise")
                    time.sleep(1)                       # sleep for 1 second before checking hour
                currentDay = int(time.strftime("%u"))   # get current day
            tweeted = False
            if(currentDay == 0):                        # if it's the end of week (it dont block making a tweet because this test is after)
                if(debug): print("end of week, create a new list")
                days = create_days()                    # regenerate list of days to tweet
        else:
            if(debug): print("sleep until end of day at the end of prog")
            time.sleep(((23-int(time.strftime("%H")))*60*60)+((59-int(time.strftime("%M")))*60)+(58-int(time.strftime("%S"))))
            while(time.strftime("%H:%M") != "00:00"):   
                if(debug): print("sleep until end of day")
                time.sleep(1)                           # sleep for 1 second before checking hour