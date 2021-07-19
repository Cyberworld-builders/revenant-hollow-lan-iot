from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo, MongoClient

app = Flask(__name__)
api = Api(app)

# Database
client = MongoClient("mongodb://localhost")
db = client.location

def abort_if_haunt_doesnt_exist(haunt_id):
    if haunt_id not in haunts:
        abort(404, message="Haunt {} doesn't exist".format(haunt_id))

parser = reqparse.RequestParser()
parser.add_argument('name')


# Haunt
# shows a single haunt item and lets you delete a haunt item
class Haunt(Resource):
    def get(self, haunt_id):
        abort_if_haunt_doesnt_exist(haunt_id)
        return haunts[haunt_id]

    def delete(self, haunt_id):
        abort_if_haunt_doesnt_exist(haunt_id)
        del haunts[haunt_id]
        return '', 204

    def put(self, haunt_id):
        args = parser.parse_args()
        name = {'name': args['name']}
        haunts[haunt_id] = name
        return name, 201


# HauntList
# shows a list of all haunts, and lets you POST to add new names
class HauntList(Resource):
    def get(self):

        haunts = []

        for haunt in db.haunts.find():
            haunts.append({
                'name'  : haunt['name']
            })
            
        return haunts

    def post(self):
        args = parser.parse_args()

        haunt = {'name' : args['name']}
        db.haunts.insert_one(haunt)
        return {"message" : "Haunt created successfully."},201

##
## Actually setup the Api resource routing here
##
api.add_resource(HauntList, '/haunts')
api.add_resource(Haunt, '/haunts/<haunt_id>')


if __name__ == '__main__':
    app.run(debug=True)
