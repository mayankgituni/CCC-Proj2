#!/usr/bin/env python3

from dbManager import DbOperation
import json


def main(city):
    database = DbOperation('admin','123456','localhost:50000','melbourne_tweet')

    result1 = database.resultConverter('group_tweet', 3)  #keywords
    result2 = database.resultConverter('negative&withoutKeywords', 3)  #I
    result3 = database.resultConverter('negative&withKeywords', 3)    #IE
    result4 = database.resultConverter('positive&withKeywords', 3)    #E
    result5 = database.hashtage_rank()  #hashtage

    if city == 'Melbourne':
        f_path = 'aurin_melb.geojson'
    elif city == 'Sydney':
        f_path = 'aurin_sydn.geojson'

    f = open(f_path, 'r', encoding="utf-8")
    data = json.loads((f.read()))
    f.close()
    features = data['features']
    for feature in features:
        lga_code  = feature['properties']['lga_code']
        if lga_code in result1:
            feature['properties'].update(result1[lga_code])
        else:
            feature['properties'].update({'keywords':0})

        if lga_code in result2:
            feature['properties'].update(result2[lga_code])
        else:
            feature['properties'].update({'I': 0})

        if lga_code in result3:
            feature['properties'].update(result3[lga_code])
        else:
            feature['properties'].update({'IE': 0})
        

        if lga_code in result4:
            feature['properties'].update(result4[lga_code])
        else:
            feature['properties'].update({'E': 0})

        if lga_code in result5:
            feature['properties'].update({'Hashtag':result5[lga_code]})
        else:
            feature['properties'].update({'Hashtag': ''})
        print(feature['properties'])

    
    data['features'] = features

    return data
