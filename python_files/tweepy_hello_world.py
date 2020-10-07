#!/usr/bin/env python
# coding: utf-8

#Step one: import tweepy and use the token and keys to authorize and access the API
import tweepy
import csv #Import csv
import json
from datetime import date
from datetime import datetime
import time
import numpy as np
import pandas as pd

from config import consumer_key, consumer_secret, access_token, access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Helper function to handle twitter API rate limit
def limit_handled(cursor, list_name):
  while True:
    try:
      yield cursor.next()
    # Catch Twitter API rate limit exception and wait for 15 minutes
    except tweepy.RateLimitError:
      print("\nData points in list = {}".format(len(list_name)))
      print('Hit Twitter API rate limit.')
      for i in range(3, 0, -1):
        print("Wait for {} mins.".format(i * 5))
        time.sleep(5 * 60)
    # Catch any other Twitter API exceptions
    except tweepy.error.TweepError:
      print('\nCaught TweepError exception' )


# def get_all_tweets(screen_name):
#     #Twitter only allows access to a users most recent 3240 tweets with this method
#
#     #initialize a list to hold all the tweepy Tweets
#     alltweets = []
#
#     #make initial request for most recent tweets (200 is the maximum allowed count)
#     new_tweets = api.user_timeline(screen_name = screen_name,count=200)
#
#     #save most recent tweets
#     alltweets.extend(new_tweets)
#
#     #save the id of the oldest tweet less one
#     oldest = alltweets[-1].id - 1
#
#     #keep grabbing tweets until there are no tweets left to grab
#     while len(new_tweets) > 0:
#         print(f"getting tweets before {oldest}")
#
#         #all subsiquent requests use the max_id param to prevent duplicates
#         new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
#
#         #save most recent tweets
#         alltweets.extend(new_tweets)
#
#         #update the id of the oldest tweet less one
#         oldest = alltweets[-1].id - 1
#
#         print(f"...{len(alltweets)} tweets downloaded so far")
#
#     #transform the tweepy tweets into a 2D array that will populate the csv
#     outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
#
#     #write the csv
#     with open(f'new_{screen_name}_tweets.csv', 'w') as f:
#         writer = csv.writer(f)
#         writer.writerow(["id","created_at","text"])
#         writer.writerows(outtweets)

#get_all_tweets('CLau24fiddy')

# # This part is for the people RECIEVING death threats

def search_on_twitter(cursor, unique_search):
    #documentation
    #cursor: pass in cursor object with your search api call
    #unique_search: pass in string that it searched with the cursor object
    #returns an numpy array with the 10 attributes for each tweet that It finds searching the unique_search keyword
    tweet_arr=[['search_word','user','screen_name','text', 'follow_count', 'friends', 'bio', 'is_verified',
           'is_default_profile', 'is_default_profile_img', 'is_geo_enabled']]
    maxCount = 1
    count = 0
    alltweets = []

    for tweet in cursor.items():
        print("Text:", tweet.text)
        search_word=unique_search
        text = tweet.text

        user = tweet.user.id
        #Camisani-Calzolari Rule set
        user = api.get_user(user)
        screen_name = user.screen_name
        print(screen_name)

        follow_count = user.followers_count
        print(follow_count)

        friends = user.friends_count
        print(friends)

        is_verified = user.verified
        print(is_verified)

        is_default_profile = user.default_profile
        print(is_default_profile)

        is_default_profile_img = user.default_profile_image
        print(is_default_profile_img)
        #we can figure out the gender through self-identifying information in bios.
        bio = user.description
        print(bio)


        is_geo_enabled = user.geo_enabled
        print(is_geo_enabled)
        print("User ID:", tweet.user.id)

        #adding the temp variable into an array of values
        arr=[[search_word, user, screen_name, text, follow_count, friends, bio, is_verified, is_default_profile, is_default_profile_img, is_geo_enabled]]
        tweet_arr = np.concatenate((tweet_arr,arr))

        count = count+1
        if count==100:
            time.sleep(60)
        if count == maxCount:
            return tweet_arr
            break;

def export_csv(var, key_word):
# with open(f'new_{screen_name}_tweets.csv', 'w') as f:
    export_name= key_word
    with open(export_name+'.csv', 'w') as f:
        writer = csv.writer(f)
                #writer.writerow(["id","created_at","text"])
        writer.writerows(var)

key_word_one = 'I received death threat'
key_word_two = 'sent death threat'
key_word_three = 'got death threat'

cursor_one= tweepy.Cursor(api.search, q=key_word_one, lang="en", count= 50)
cursor_two= tweepy.Cursor(api.search, q=key_word_two, lang="en", count=50)
cursor_three=tweepy.Cursor(api.search, q=key_word_three, lang="en", count=50)

#I_received_death_threat_arr= search_on_twitter(cursor_one, key_word_one)
#print(I_received_death_threat_arr)
#export_csv(I_received_death_threat_arr, key_word_one)


#sent_death_threat_arr= search_on_twitter(cursor_two, key_word_two)
#export_csv(sent_death_threat_arr, key_word_two)


#send_me_death_threat_arr= search_on_twitter(cursor_three, key_word_three)
#print(send_me_death_threat_arr)
#export_csv(send_me_death_threat_arr, key_word_three)


# # This part is for people who SENT death threats

key_word_four = 'please go kill yourself'
key_word_five = 'i hope you die'
key_word_six = 'please commit suicide'

cursor_four= tweepy.Cursor(api.search, q=key_word_four, lang="en", count= 50)
cursor_five= tweepy.Cursor(api.search, q=key_word_two, lang="en", count=50)
cursor_six= tweepy.Cursor(api.search, q=key_word_three, lang="en", count=50)

#please_go_kill_yourself_arr= search_on_twitter(cursor_four, key_word_four)
#export_csv(please_go_kill_yourself_arr, key_word_four)


#i_hope_you_die_arr= search_on_twitter(cursor_five, key_word_five)
#print(i_hope_you_die_arr)
#export_csv(i_hope_you_die_arr, key_word_five)

#i_hope_you_die_arr= search_on_twitter(cursor_five, key_word_five)

#please_commit_suicide_arr= search_on_twitter(cursor_six, key_word_six)
#print(please_commit_suicide_arr)
#export_csv(please_commit_suicide_arr, key_word_six)
key_word_seven = 'hi there'
cursor_seven=tweepy.Cursor(api.search, q=key_word_seven, lang="en", count=50)

hi_ther_arr= search_on_twitter(cursor_seven, key_word_seven)
export_csv(hi_ther_arr, key_word_seven)
