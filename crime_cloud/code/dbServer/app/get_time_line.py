#!/usr/bin/env python3

import tweepy
import sys
import json 
import re
import time

class MyTimeLine():

    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''


    def process_or_store(self, user_ID, twitter_no, api):
        
        status_list = []
        tweet_list  = []

        try:
            api.user_timeline(user_id = user_ID, count=twitter_no, include_rts = False, tweet_mode = 'extended')
        except Exception:
            return
        else:
            status_list = api.user_timeline(user_id = user_ID, count=twitter_no, include_rts = False, tweet_mode = 'extended')

        

        for status in status_list:
            tweet   = json.dumps(status._json)
            tweet_list.append(tweet)

        # result = {user_ID:tweet_list}
        # print(result.keys)
        # print(len(result.get(user_ID)))
        # print(tweet_list[10], len(tweet_list))

        return tweet_list



