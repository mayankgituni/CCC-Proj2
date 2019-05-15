#!/usr/bin/env python3

import sys
import tweepy
import json
import _thread
from DbOperation import DbOperation


from   tweepy import OAuthHandler
from   tweepy import Stream
from   tweepy.streaming import StreamListener
from   get_time_line import MyTimeLine
from   configuration import Config
import pybloom_live as bf

from sentiment import SentimentAnalysis
from filter import Filter
from locate import Locate



access_token = "1125959900851425285-qiOUb4TaDvlAS9hJ32GCY5luVqgh38"
access_token_secret = "u7PHeleq5eV819ASr6wev3XDob9VNQ6xpYIiNbFGP8tHn"
consumer_key = "oJzRqVWiRxm3fktcWsolfEoMi"
consumer_secret = "FDrh1qlDVO9JwODrnKByLAxw1gmgOFV32pFWtYCphjtoNEtDXc"


with open('melbourne_user.txt', 'r') as f:
    melbourne_user = f.read().splitlines()

with open('sydney_user.txt', 'r') as f:
    sydney_user = f.read().splitlines()

class MyListener(StreamListener):
    city = ''
    coordinates =[]

    sbf = bf.ScalableBloomFilter(mode=bf.ScalableBloomFilter.SMALL_SET_GROWTH)
    timeline = MyTimeLine()
    api_list = Config().api_list
    timeline_num = 200

    print("Class creating....!")
    
    

    def __init__(self, location_json):
        for k, v in location_json.items():
            self.city = k
            self.coordinates = v
    

    def write_file(self, user_id, api, index):

        timeline_tweets = []

        if index == len(self.api_list): return 0
            
        timeline_tweets = self.timeline.process_or_store(user_id, self.timeline_num, api)

        print('User ID: ', format(user_id, '<20'), 'timeline length: ', len(timeline_tweets))

        # if current api token is invalid, switch another one
        if not timeline_tweets:
            index += 1
            return index

        if (self.city == 'melbourne'):

            try:
                with open('twitter_melbourne.json', 'a', encoding='utf8') as f:
                    for tweet in timeline_tweets:
                        f.write(tweet + '\n')

            except BaseException as e:
                print("Error on_data: %s" % str(e))

        elif (self.city == 'sydney'):

            try:
                with open('twitter_sydney.json', 'a', encoding='utf8') as f:
                    for tweet in timeline_tweets:
                        f.write(tweet + '\n')

            except BaseException as e:
                print("Error on_data: %s" % str(e))



    # wirte to json file
    def on_data(self, data):
        try:
            print("On data start....")
            tweet   = json.loads(data)
            user_id = tweet["user"]["id"]
            # text    = tweet["text"]
            index   = 0
            api     = self.api_list[index]


            # create instance 
            my_filter = Filter()
            my_sentiAnalysis = SentimentAnalysis()
            my_locate = Locate()

            print("I am startng the db")
            
            # append user id list based on city
            if (self.city == 'melbourne'):
                lga_file = "melbLga.json" # the LGA code from Aurin
                Locate().getMap(lga_file)
                melb_db = DbOperation('admin','123456','172.26.37.240:50000','melb_tweet')

                if (user_id in melbourne_user):
                    pass
                else:
                    if (user_id in self.sbf):
                        print('user exist')
                        return True
                    else:
                        # add user id into bloom filter
                        self.sbf.add(user_id)

                        # add user id into a file
                        with open('melbourne_user.txt', 'a+') as f:
                            f.write(str(user_id) + '\r\n')

                        # index = self.write_file(user_id, index)

                        # try:
                        #     _thread.start_new_thread( self.write_file, (user_id, api, index) )
                        # except:
                        #     print ("Error: cannot start thread")

                        timeline_tweets = self.timeline.process_or_store(user_id, self.timeline_num, api)
                        print(user_id, timeline_tweets[0], len(timeline_tweets), type(timeline_tweets))


                        for tweet in timeline_tweets:

                            print('hello\n')

                            tweet = my_filter.filter(tweet)

                            print('world\n')
                            tweet = my_sentiAnalysis.sentimentAnalysis(tweet)

                            print('yoyo\n')
                            
                            tweet = my_locate.locate(tweet)
                            # tweet = json.dumps(tweet)
                            
                            print(tweet)

                            melb_db.uploadDoc(tweet)

                        return True

            elif (self.city == 'sydney'):
                lga_file = "sydLga.json" # the LGA code from Aurin
                Locate().getMap(lga_file)
                syd_db = DbOperation('admin','123456','172.26.37.240:50000','syd_tweet')
                if (user_id in sydney_user):
                        pass
                else:
                    # add user id into bloom filter
                    self.sbf.add(user_id)

                    with open('sydney_user.txt', 'a+') as f:
                        f.write(str(user_id) + '\r\n')
                    

                    # try:
                    #     _thread.start_new_thread( self.write_file, (user_id, api, index) )
                    # except:
                    #     print ("Error: cannot start thread")

                    
                    timeline_tweets = self.timeline.process_or_store(user_id, self.timeline_num, api)

                    for tweet in timeline_tweets:

                        tweet = my_filter.filter(tweet)
                        tweet = my_sentiAnalysis.sentiAnalysis(tweet)
                        tweet = my_locate.locate(tweet)
                        tweet = json.dumps(tweet)

                        syd_db.uploadDoc(tweet)

                return True 

                
        except BaseException as e:
            print("on_data wrong: %s" % str(e))
        return True
 

    def on_error(self, status):
        if status == 420:
            #returning False in on_data disconnects the stream
            print('Error 420')
            return False
 

    def start(self, location_json):
        print('hello')
        print(location_json)
        try: 
            print("Starting auth....")
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
        
        except: 
                print("Error: Authentication Failed") 


        print("Start to stream")
        twitter_stream = Stream(auth, self)
        print("Streaming comes with ", self.coordinates)
        # filter streams from Melbourne region
        twitter_stream.filter(locations=self.coordinates, languages = ["en"])
        print("Done filtering")

