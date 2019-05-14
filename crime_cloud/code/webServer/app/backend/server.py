import json
import os
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import render_template

# start the web service.
template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'app')
template_dir = os.path.join(template_dir, 'frontend')
template_dir = os.path.join(template_dir, 'build')

print('\n' + template_dir + '\n')
app = Flask(__name__, root_path=template_dir, template_folder=template_dir)
api = Api(app)
# cors = CORS(app, resources={r"/melb*": {"origins": "*"}})
CORS(app)


class Melbourne(Resource):

    def get(self):

        with open ('./melbLga.geojson', 'r') as f:
            melbLga = json.load(f)

        return melbLga


api.add_resource(Melbourne, '/melb')


class USA(Resource):
    
    def get(self):

        with open ('./us-income.geojson', 'r') as f:
            usa = json.load(f)

        return usa


api.add_resource(USA, '/usa')

class Sydney(Resource):
    
    def get(self):

        with open ('./aurin_sydn.geojson', 'r') as f:
            aurin_sydn = json.load(f)

        return aurin_sydn


api.add_resource(Sydney, '/sydn')

# @app.route('/')
# def index():
#     """
#     For test if the service works.
#     :return: NoneType
#     """
#     return "Hello, World!"


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

# # and rearrange them into GeoJson style.
# @app.route("/melb")
# def return_melb():
#     return send_from_directory('.', 'melbLga.geojson')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50000, debug=True)
