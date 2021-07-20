from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)



# Database
client = MongoClient("mongodb://localhost")
db = client.location

locations = []
ips = []

for location in db.locations.find():
    ips.append({'ip': location['ip']})
    locations.append({
        'name'  : location['name'],
        'ip'    :   location['ip'],
        'idle'  :   location['idle']
    })

def abort_if_location_doesnt_exist(location_ip):
    if location_ip not in ips:
        abort(404, message="Location {} doesn't exist".format(location_ip))

parser = reqparse.RequestParser()
parser.add_argument('ip')
parser.add_argument('name')
parser.add_argument('idle')



# Haunt
# shows a single haunt item and lets you delete a haunt item
class Location(Resource):
    def get(self, location_ip):
        abort_if_location_doesnt_exist(location_ip)
        query = db.locations.find({'ip': "10.0.0.6"})[0]
        location = {
            'ip'  :   query['ip'],
            'name'  :   query['name'],
            'idle'  :   query['idle']
        }
        return location, 200

    def delete(self, location_ip):
        abort_if_location_doesnt_exist(location_ip)
        location = db.locations.remove({'ip': location_ip})
        return location_ip, 204

    def put(self, location_ip):
        args = parser.parse_args()
        ip = args['ip']
        name = args['name']
        idle = args['idle']
        filter = {'ip': ip}
        location = {"$set":
            {
                'ip' :  ip,
                'name'  :   name,
                'idle'    :   idle
            }
        }

        query = db.locations.update_one(filter,location)
        return location, 201

# LocationList
# shows a list of all haunts, and lets you POST to add new names
class LocationList(Resource):
    def get(self):
        locations = []
        for location in db.locations.find():
            ips.append(location['ip'])
            locations.append({
                'ip'    :   location['ip'],
                'name'  : location['name'],
                'idle'  :   location['idle']
            })
        return locations, 200
    def post(self):
        args = parser.parse_args()

        location = {
            'ip' : args['ip'],
            'name' : args['name'],
            'idle' : args['idle']
        }
        db.locations.insert_one(location)
        return {"message" : "Location stored successfully."},201

##
## Routing
##
api.add_resource(LocationList, '/locations')
api.add_resource(Location, '/locations/<location_ip>')

if __name__ == '__main__':
    app.run(debug=True)
