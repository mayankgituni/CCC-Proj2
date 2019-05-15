#!/usr/bin/env python3

import tweepy
from   tweepy import OAuthHandler, Stream


screen_name = '@realDonaldTrump'
# user_ID = '791780089620856834'
twitter_no = 200



class Config():


    api_list = []

    def __init__(self): 
        access_token1 = "1114063635733573634-85Olmp5dFd8amqbQ4Hs8K1tkxWlQ8F"
        access_token_secret1 = "jNXnScED9jwsfI18B6Sdnij8T6HPnJ0TCgIdnOyqO3ccO"
        consumer_key1 = "6PEhcfXd251P4DNc3UzX4pyv9"
        consumer_secret1 = "2UcZfFrufMCY07nyYyiutBle6EqOyfOdjZVHVaNwEgFx11vttW"

        access_token2 = "1116125921113595904-DCRygbynO9g5bR5VaHn8xvamc9Hg52"
        access_token_secret2 = "pgF19zNAWbNIW9O7Qjero7eBz5fHU8qBBH9qHziegDmYs"
        consumer_key2 = "sCS8KaVTCXpsB5pFs4Lp5A3J3"
        consumer_secret2 = "plql1gDYTJThzhsOr3BN4ncW6qJPNG2icrsaxxyHbMS2UIFh58"

        access_token3 = "1125948215482667008-paCbl7CJuykk9WKbxc94Tupe9cqdsJ"
        access_token_secret3 = "vcDYdIienDedUOFdQ7FUqqzPXQXyZpO1sVsAX278sBbWw"
        consumer_key3 = "R4WVfADXUlM3CNJEu9bnWA5f2"
        consumer_secret3 = "dKyLBpel7BsiYEPdlV8yCbpJkutWOJ8IbUdZM3TbZFHOj3BS4P"

         # keys and tokens from the Twitter Dev Console 
        access_token4 = "913751919692099584-EdeuOsUbA3vE3BYuqJY99G7PYpV1Mwk"
        access_token_secret4 = "zNbx6nq6O2DBcCataGM9F0d0J1c51HGrL9a5b9S8P3mWj"
        consumer_key4 = "bIEFZFLp5wiuS48Xd6kRjaHAA"
        consumer_secret4 = "lXDW9bkbqqQiTlt8EtLN1KDh8SE9q11m3kUMxxR3a4GYnDxzX0"

        access_token5 = "1125950625957597187-lvRh1OUYslZEJlRgUFbUyJgPMxUUk2"
        access_token_secret5 ="bJbKV6dIhdF3HInrk0ne3xs70509oElL1HoX1YUoByaWm"
        consumer_key5 = "xAV1PYH3xvjOOGrKFEdGGv1pD"
        consumer_secret5 = "BXOfexHaWW2wol8yn5Nci63gzxdBIQCFxiq5k3FXZgd4yH07Wi"

        access_token6 = "1125959900851425285-qiOUb4TaDvlAS9hJ32GCY5luVqgh38"
        access_token_secret6 ="u7PHeleq5eV819ASr6wev3XDob9VNQ6xpYIiNbFGP8tHn"
        consumer_key6 = "oJzRqVWiRxm3fktcWsolfEoMi"
        consumer_secret6 = "FDrh1qlDVO9JwODrnKByLAxw1gmgOFV32pFWtYCphjtoNEtDXc"


        # attempt authentication 
        try: 
            self.auth1 = OAuthHandler(consumer_key1, consumer_secret1)
            self.auth1.set_access_token(access_token1, access_token_secret1) 
            self.api1 = tweepy.API(self.auth1) 

            self.auth2 = OAuthHandler(consumer_key2, consumer_secret2)
            self.auth2.set_access_token(access_token2, access_token_secret2)
            self.api2 = tweepy.API(self.auth2)

            self.auth3 = OAuthHandler(consumer_key3, consumer_secret3)
            self.auth3.set_access_token(access_token3, access_token_secret3)
            self.api3 = tweepy.API(self.auth3)

            self.auth4 = OAuthHandler(consumer_key4, consumer_secret4)
            self.auth4.set_access_token(access_token4, access_token_secret4) 
            self.api4 = tweepy.API(self.auth4) 

            self.auth5 = OAuthHandler(consumer_key5, consumer_secret5)
            self.auth5.set_access_token(access_token5, access_token_secret5) 
            self.api5 = tweepy.API(self.auth5) 

            self.auth6 = OAuthHandler(consumer_key6, consumer_secret6)
            self.auth6.set_access_token(access_token6, access_token_secret6) 
            self.api6 = tweepy.API(self.auth6) 

            try:
                self.api_list = [self.api1, self.api2, self.api3, self.api4, self.api5, self.api6]
            except:
                print('api list error')

        except: 
            print("Error: Authentication Failed") 



