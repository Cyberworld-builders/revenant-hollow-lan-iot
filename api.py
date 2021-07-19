from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

# App
app = Flask(__name__)
api = Api(app)

# Database
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


# Haunt
haunt = {}

class Haunt(Resource):
    def get(self, haunt_id):
        return haunt_id
        # return "test get " + str(haunt_id)
        # return {haunt_id: haunt[haunt_id]}

api.add_resource(Haunt, '/haunt/<int:haunt_id>')

if __name__ == '__main__':
    app.run(debug=True)
