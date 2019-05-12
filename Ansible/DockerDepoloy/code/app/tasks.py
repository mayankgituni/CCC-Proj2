#!/usr/bin/env python3

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Melb(Resource):
    def get(self):
        f= open("writeTest.txt","w+")
        f.write("I am wirint to test the volume.")
        f.close()
        return {
            "Name" : "Mayank Tomar",
            "Age" : 27,
            "Height" : 445.2
        }

api.add_resource(Melb,'/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50001, debug=True)
