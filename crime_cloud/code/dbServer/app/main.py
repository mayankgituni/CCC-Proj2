#!/usr/bin/env python3

import json
from twitter_streaming import MyListener

if __name__ == '__main__':
    f = open("/app/setup.json", "r")
    # line = f.readline().strip()
    city = json.load(f)
    print (city, type(city), city['melbourne'])
    listener  = MyListener(city)
    # print("Listening...")
    listener.start(city)
    print("End!")