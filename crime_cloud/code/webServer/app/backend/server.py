import json
import os
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import render_template
from dbManager import DbOperation
from generate_geofile import GenerateGeo

# start the web service.
template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# template_dir = os.path.join(template_dir, 'CCC-Project')
template_dir = os.path.join(template_dir, 'app')
template_dir = os.path.join(template_dir, 'frontend')
template_dir = os.path.join(template_dir, 'build')

# display current directory
print('\n' + template_dir + '\n')

app = Flask(__name__, root_path=template_dir, template_folder=template_dir)
api = Api(app)

# allow cross site request
CORS(app)

db_operator = DbOperation('admin', '123456', '172.26.37.240:50000', 'aurin')
gn_operator_melb = GenerateGeo('172.26.37.240', 'melb_tweet')
gn_operator_sydn = GenerateGeo('172.26.38.161', 'melb_tweet')

class Melbourne(Resource):
    """
    Melbourne class: handle all request relate with melbourne
    method:get(year), return data in geojson format
    """

    # return aurin data based on year
    def get(self, year):
        if year == '2015':
            return   db_operator.query_aurin('2015_melb.geojson')
        elif year == '2016':
            return db_operator.query_aurin('2016_melb.geojson')
        elif year == '2017':
            return db_operator.query_aurin('2017_melb.geojson')
        elif year == 'aurinmelb':
            return db_operator.query_aurin('aurin_melb.geojson')


api.add_resource(Melbourne, '/melb/<string:year>')


class Twitter(Resource):
    """
    Twitter class: handle all request relate with our twitter data
    method:get(city), return data in geojson format
    """

    # return live mapreduce result by city
    def get(self, city):
        if city == 'melb':
            result = gn_operator_melb.get_twitter_data('melbourne')
        elif city == 'sydn':
            result = gn_operator_sydn.get_twitter_data('sydney')

        return result


api.add_resource(Twitter, '/tweet/<string:city>')

class Sydney(Resource):
    """
    Sydney class: handle all request relate with sydney
    method:get(), return data in geojson format
    """
    # return sydney crime data
    def get(self):

        aurin_sydn =  db_operator.query_aurin('aurin_sydn_crime_2017.geojson')
        return aurin_sydn


api.add_resource(Sydney, '/sydn')


# a route where we will display a welcome message via an HTML template
@app.route("/")
def index():  
    with open ('../frontend/build/index.html', 'r') as f:
        print(f)
    return render_template('index.html')


@app.route("/app")
def index2():  
    with open ('../frontend/build/index.html', 'r') as f:
        print(f)
    return render_template('index.html')


@app.route("/app/dashboard")
def index3():  
    with open ('../frontend/build/index.html', 'r') as f:
        print(f)
    return render_template('index.html')


@app.route("/app/maps")
def index4():  
    with open ('../frontend/build/index.html', 'r') as f:
        print(f)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50000, debug=True)
