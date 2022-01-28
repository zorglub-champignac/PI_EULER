# Ensure tweepy is installed as Python3 Library
import tweepy
import os
import time
import datetime
import random

# Set up base path - ensures this works in Linux/Windows environments
BASE_PATH = os.sys.path[0]

# Sleep Timer - WARNING: this prevents a RateLimitError, so be careful changing it (unit = seconds)
SLEEP_TIMER = 5*60

# A small amount of sleep after each deletion ...
DELETE_SLEEP = 0.1

PAGE_SLEEP = 0.5

TINY_SLEEP = 0.05

# Age of tweet - default: all tweets older than 7 days
AGE_OF_TWEET = 19

# These are keys for the development API and are static
consumer_key = "9vuTxHqfVJRCqGsDDEH3AylBj"
consumer_secret = "hdcDYqGMz9kJ30McZ3aea1Uim5BUJYKHJ3MoMJ0HWpUBJ9aJY9"
access_token = "2268792535-tRoQGtc8ua72s0xFLztwKBVT69V1CXuTEhZsgO3"
access_token_secret = "AZHiODJOkWc8xJspCUJ70a5LM5CO6B8ftMGmOmTqAVaGr"

user_name = "__Idiotix__"

def get_statuses(api, username, target_username, friend_dump_file):
    # Make a "nice" output for user
    print("\n")
    print("Deleting Tweets for user: " + target_username)
    print("All tweets older than " + str(AGE_OF_TWEET) + " days will be deleted")
    print("---------------------------------------------------------------------------\n")

    idToDelete = [0]
    nbToDelete = 0

    nbSup = 1
    last_id = 1257688772222816260

    try:

        ## use tweepy.cursor to obtain the target user list
        ## for look to circulate through them

        deleted = 0
        skipped = 0
        for get_statuses in tweepy.Cursor(api.user_timeline, screen_name=target_username).pages():
#       for get_statuses in tweepy.Cursor(api.search, q='from:@__Idiotix__  since:2018-03-01 until:2020-05-01').pages():
            for status in get_statuses:
                try:
                    # Get API returned variables ready
                    tweet_id = status.id
                    tweet_text = status.text.replace("\n", "")[:60]
                    tweet_creation_date = status.created_at
                    # Get the age of the tweet in days - e.g. return of "8" indicates it was 8 days ago
                    difference = get_days(tweet_creation_date)
                    # If the age of the tweet is greater than the pre-set variable (set at the top), then delete
#                   if difference > AGE_OF_TWEET:
                    if skipped >= 1000:
                        deleted += 1
                        print ("#" + str(deleted) +  "(" + str(skipped) + ") " +str(tweet_id)  + " " + str(tweet_creation_date) + "  \t TO Delete  --> " + tweet_text )
                        nbToDelete += 1
                        idToDelete.append(tweet_id)
                        # Sleep just a tiny bit...
                    else:
                        skipped += 1
                        if( skipped == 20 * (skipped // 20) ):
                            print("#" + str(skipped) + " " + str(tweet_creation_date) + " " + str(tweet_id) + ": \t Skipping  --> " +   tweet_text )
                except:
                    continue
            time.sleep(PAGE_SLEEP)

        print("---------------------------------------------------------------------------")
        print("Process Finished")
        print("Total Tweets TO delete: " + str(deleted) + " Skipped: " + str(skipped))
        for ind_del in range(nbToDelete,0,-1):
            print(idToDelete[ind_del])
            api.destroy_status(idToDelete[ind_del])
            time.sleep(DELETE_SLEEP)
        print("Total Tweets Deleted: " + str(nbToDelete) + " Skipped: " + str(skipped))
    except tweepy.RateLimitError:
# If you hit a rate limit then sleep for a little bit... recommended is 5 minutes (5x60)
        print("Rate Limit Error: Sleeping for a little while")
        time.sleep(SLEEP_TIMER)


def get_days(created_date):

    # Get the current date and convert to string
    now = str(datetime.date.today())

    # Prepare it for comparison
    now_ready = datetime.datetime.strptime(now, "%Y-%m-%d")

    # Calculate the difference between the two days
    difference = now_ready - created_date

    # Return the single integer value of the days between the two days
    return difference.days

def main():

    ## First ask user what their Twitter username is
 #   username = input("Please Enter your Twitter username: ")
    username = user_name
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

#    target_username = input("Enter target username, to delete statuses older than " + str(AGE_OF_TWEET) + " days: ")
    target_username = user_name
    statuses_file = BASE_PATH + "/" + target_username + "_statuses.txt"

    # Call Function
    get_statuses(api, username, target_username, statuses_file)


if __name__ == "__main__":
    main()


'''   
    nb = 0
    while nbSup:
        try:
            get_statuses = api.home_timeline ()
            nbSup = 0
            for status in get_statuses:
                tweet_id = status.id
                last_id = tweet_id
                nbSup += 1
                nb += 1
                tweet_text = status.text.replace("\n", "")[:60]
                tweet_creation_date = status.created_at
                print("#" + str(nb) + " " + str(tweet_id) + " " + str(tweet_creation_date) + "  \t TO Delete  --> " + tweet_text)
            time.sleep(1+random.random())
            print("--")
        except tweepy.RateLimitError:
        # If you hit a rate limit then sleep for a little bit... recommended is 5 minutes (5x60)
            print("Rate Limit Error: Sleeping for a little while")
            time.sleep(SLEEP_TIMER)
    return
'''

'''
    ## Now create path variable for text file to store tokens
    token_file = BASE_PATH + "/" + username + " - tokens.txt"


    ## Ok, now check if the access Tokens for this user are available
    ## If not user should be asked to visit URN and authorise access via supplied PIN code
    if os.path.isfile(token_file):

        # Yes user is known to us... open the corresponding TOKEN_FILE
        with open(token_file, "r") as file:

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.secure = True
            access_token = file.readline().strip()
            access_token_secret = file.readline().strip()

    else:

        # No user is not known ... ask them to visit URL and read in PIN code supplied by Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth_url = auth.get_authorization_url()
        print("Visit this URL and authorise the app to use your Twitter account: " + auth_url)
        verifier = input('Type in the generated PIN: ').strip()

        # We have the tokens - now save them into respective variables
        auth.get_access_token(verifier)
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret

        # Save them into TOKEN_FILE for future use
        with open(token_file, "w") as f:
            f.write(access_token + "\n")
            f.write(access_token_secret)

        f.close()
'''
