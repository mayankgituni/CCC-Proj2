import os
import json
import copy


with open('./2015_melb.json', 'r') as f:
    melb_2015 = json.load(f)

with open('./2016_melb.json', 'r') as f:
    melb_2016 = json.load(f)

with open('./2017_melb.json', 'r') as f:
    melb_2017 = json.load(f)


class Processor():


    def trim_data(self, file, fname):

        properties={}
        new_features=[]
        features_array = file['features']

        for district in features_array: 
            a_crime = district['properties']['total_division_a_offences']
            b_crime = district['properties']['total_division_b_offences']
            c_crime = district['properties']['total_division_c_offences']
            d_crime = district['properties']['total_division_d_offences']
            e_crime = district['properties']['total_division_e_offences']
            f_crime = district['properties']['total_division_f_offences']
            lga_name11 = district['properties']['lga_name11']
            lga_code = district['properties']['lga_code']
            grand_total_offence_count = district['properties']['grand_total_offence_count']
            lga_erp = district['properties']['lga_erp']

            properties.update({
                'a_crime': a_crime,
                'b_crime': b_crime,
                'c_crime': c_crime,
                'd_crime': d_crime,
                'e_crime': e_crime,
                'f_crime': f_crime,
                'lga_name11': lga_name11,
                'lga_code': lga_code,
                'totoal_offence': grand_total_offence_count,
                'lga_erp': lga_erp,
            })

            district['properties'] = properties
            tmp = copy.deepcopy(district)
            new_features.append(tmp)
            


        if (fname == '2015_melb'):
            with open('2015_melb.geojson', 'a+') as f:
                f.write(json.dumps({
                    'type': file['type'],
                    'crs':  file['crs'],
                    'features': new_features
                }))

        elif (fname == '2016_melb'):
            with open('2016_melb.geojson', 'a+') as f:
                f.write(json.dumps({
                    'type': file['type'],
                    'crs':  file['crs'],
                    'features': new_features
                }))
        elif (fname == '2017_melb'):
            with open('2017_melb.geojson', 'a+') as f:
                f.write(json.dumps({
                    'type': file['type'],
                    'crs':  file['crs'],
                    'features': new_features
                }))



if __name__ == "__main__":
    processor = Processor()
    processor.trim_data(melb_2015, '2015_melb')
    processor.trim_data(melb_2016, '2016_melb')
    processor.trim_data(melb_2017, '2017_melb')