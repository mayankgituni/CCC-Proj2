import sys
import json
import re
from geoCompensate import GeoCompensate

class Filter():
    """This class takes a tweet object, filter out necessary fileds, 
    clean up the tweet text, and try to compensate empty coordinate field"""
    
    def filter(self, tweet):
        filtered_tweet = {}
        geo = GeoCompensate().geoCompensate
        
        tweet = json.loads(tweet)
        
        # append tweet id 
        filtered_tweet["id"] = tweet["id"]

        # text clean up
        # extract mentioned users & hashtags
        text = tweet["full_text"]
        cleaned_text = []
        mention = []
        hashtages = []
        for word in text.split():
            if "http" in word: continue
            elif word.startswith('@'): mention.append(word.strip("@"))
            elif word.startswith('#'): hashtages.append(word.strip("#"))
            else: cleaned_text.append(word.lower())
        
        filtered_tweet["text"] = " ".join(cleaned_text)
        filtered_tweet["mention"] = mention
        filtered_tweet["hashtage"] = hashtages

        # append user id
        filtered_tweet["user"] = tweet["user"]["id"]

        # extract time and year
        time = re.search("\s\d{2}:", tweet["created_at"]).group(0)
        time = int(time.strip(" ").strip(":"))
        filtered_tweet["time"] = time

        year = re.search("\d{4}$", tweet["created_at"]).group(0)
        filtered_tweet["year"] = int(year)
        
        # append coordinates
        try:
            tweet["coordinates"]["coordinates"]
        except:
            try:
                tweet["place"]["bounding_box"]["coordinates"]
            except:
                filtered_tweet["coordinates"] = []
            else:
                # try to use bounding box to indicate the coordinates
                filtered_tweet["coordinates"] = geo(tweet["place"]["bounding_box"]["coordinates"][0])
        else:
            filtered_tweet["coordinates"] = tweet["coordinates"]["coordinates"]

        return filtered_tweet


# if __name__ == "__main__":

#     myfilter = Filter().filter

#     tweet = {"created_at": "Sat May 11 06:44:15 +0000 2019", "id": 1127102098699476992, "id_str": "1127102098699476992", "full_text": "@in_geardagum Not all births are like that", "truncated": false, "display_text_range": [14, 42], "entities": {"hashtags": [], "symbols": [], "user_mentions": [{"screen_name": "in_geardagum", "name": "Anna", "id": 320171714, "id_str": "320171714", "indices": [0, 13]}], "urls": []}, "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>", "in_reply_to_status_id": 1126759258685448198, "in_reply_to_status_id_str": "1126759258685448198", "in_reply_to_user_id": 320171714, "in_reply_to_user_id_str": "320171714", "in_reply_to_screen_name": "in_geardagum", "user": {"id": 3041804096, "id_str": "3041804096", "name": "Diana Jefferies", "screen_name": "diana_jefferies", "location": "Sydney", "description": "", "url": null, "entities": {"description": {"urls": []}}, "protected": false, "followers_count": 59, "friends_count": 104, "listed_count": 1, "created_at": "Wed Feb 25 22:15:39 +0000 2015", "favourites_count": 313, "utc_offset": null, "time_zone": null, "geo_enabled": true, "verified": false, "statuses_count": 272, "lang": "en", "contributors_enabled": false, "is_translator": false, "is_translation_enabled": false, "profile_background_color": "000000", "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "profile_background_tile": false, "profile_image_url": "http://pbs.twimg.com/profile_images/570709552228605952/l3Ig03GZ_normal.jpeg", "profile_image_url_https": "https://pbs.twimg.com/profile_images/570709552228605952/l3Ig03GZ_normal.jpeg", "profile_banner_url": "https://pbs.twimg.com/profile_banners/3041804096/1425035759", "profile_link_color": "9266CC", "profile_sidebar_border_color": "000000", "profile_sidebar_fill_color": "000000", "profile_text_color": "000000", "profile_use_background_image": false, "has_extended_profile": false, "default_profile": false, "default_profile_image": false, "following": false, "follow_request_sent": false, "notifications": false, "translator_type": "none"}, "geo": null, "coordinates": null, "place": {"id": "0073b76548e5984f", "url": "https://api.twitter.com/1.1/geo/id/0073b76548e5984f.json", "place_type": "city", "name": "Sydney", "full_name": "Sydney, New South Wales", "country_code": "AU", "country": "Australia", "contained_within": [], "bounding_box": {"type": "Polygon", "coordinates": [[[150.520928608, -34.1183470085], [151.343020992, -34.1183470085], [151.343020992, -33.578140996], [150.520928608, -33.578140996]]]}, "attributes": {}}, "contributors": null, "is_quote_status": false, "retweet_count": 0, "favorite_count": 0, "favorited": false, "retweeted": false, "lang": "en"}
    
    