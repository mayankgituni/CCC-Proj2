#!/usr/bin/env python3

import json
import sys
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import time

class Locate():

    suburbs = [] # contains all polygons obtained from LGA code

    def getMap(self, filename):
        """read LGA file and stores polygons"""

        with open (filename, "r") as f:
            lga = json.load(f)

        for feature in lga["features"]:
            suburb = {}

            suburb["code"] = feature["properties"]["feature_code"]
            suburb["name"] = feature["properties"]["feature_name"]

            multiPolygons = feature["geometry"]["coordinates"]

            for multiPolygon in multiPolygons:
                for i in range(len(multiPolygon)):
                    polygon = multiPolygon[i]
                    for j in range(len(polygon)):
                        polygon[j] = tuple(polygon[j])
                    multiPolygon[i] = Polygon(polygon)
    

            suburb["coordinates"] = multiPolygons
            self.suburbs.append(suburb)


    def locatePoint(self,point):
        """locate a point in given polygons
            return [] if the point is out of range"""
            
        point = Point(tuple(point))
        found = False

        for suburb in self.suburbs:
            for multiPolygon in suburb["coordinates"]:
                outer = multiPolygon[0]
                if outer.contains(point):
                    found = True
                for index in range(1, len(multiPolygon)):
                    hole = multiPolygon[index]
                    if hole.contains(point):
                        found = False
                        break
                
                if found == True: 
                    return ([suburb["name"], suburb["code"]])
        return []

    def locate(self, tweet):
        tweet["location"] = {}
        if tweet["coordinates"] != []:
            out = self.locatePoint(tweet["coordinates"])

            # the point is outside the range
            if out == []:
                tweet["location"]["name"] = []
                tweet["location"]["code"] = []
            else:
                tweet["location"]["name"] = out[0]
                tweet["location"]["code"] = out[1]
        else:
            tweet["location"]["name"] = []
            tweet["location"]["code"] = []

        return tweet

            




    

