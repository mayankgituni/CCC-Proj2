from dbManager import DbOperation
import json

def main(city):
    database = DbOperation('admin','123456','10.12.107.7:5984','melb_tweet')

    result1 = database.resultConverter('group_tweet', 3)  #keywords
    result2 = database.resultConverter('negative&withoutKeywords', 3)  #I
    result3 = database.resultConverter('negative&withKeywords', 3)    #IE
    result4 = database.resultConverter('positive&withKeywords', 3)    #E

    if city == 'Melbourne':
        f_path = 'aurin_melb.geojson'
    elif city == 'Sydney':
        f_path = 'aurin_sydn.geojson'
    elif city == 'Brisbane':
        f_path = 'aurin_bris.geojson'

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
            feature['properties'].update(result2[lga_code])
        else:
            feature['properties'].update({'IE': 0})
        if lga_code in result4:
            feature['properties'].update(result4[lga_code])
        else:
            feature['properties'].update({'E': 0})


    data['features'] = features
    features = data['features']
    for feature in features:
        print(feature['properties'])
    return features

if __name__ == "__main__":
    f = open("data.json", "w")
    f.write(main())