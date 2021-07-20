from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_pymongo import PyMongo, MongoClient
from bson.objectid import ObjectId
import ast
import socket
import requests

app = Flask(__name__)
api = Api(app)



# Database
client = MongoClient("mongodb://localhost")
db = client.location

locations = []
ips = []

for location in db.locations.find():
    ips.append({'ip' : location['ip']})
    locations.append({
        'name'  : location['name'],
        'ip'    :   location['ip']
    })

def abort_if_location_doesnt_exist(location_ip):
    if location_ip not in ips:
        abort(404, message="Location {} doesn't exist".format(location_ip))

def abort_if_location_exists(location_ip):
    if location_ip in ips:
        abort(404, message="Location {} already exists".format(location_ip))

parser = reqparse.RequestParser()
parser.add_argument('ip')
parser.add_argument('name')
parser.add_argument('idle')

# Haunt
# shows a single haunt item and lets you delete a haunt item
class Location(Resource):
    def get(self, location_ip):
        query = db.locations.find({'ip': location_ip})
        if query.count() == 0:
            abort(404, message="Location {} doesn't exist".format(location_ip))

        location = {
            'ip'  :   query[0]['ip'],
            'name'  :   query[0]['name'],
            'idle'  :   query[0]['idle']
        }
        return location, 200

    def delete(self, location_ip):
        query = db.locations.find({'ip': location_ip})
        if query.count() == 0:
            abort(404, message="Location {} doesn't exist".format(location_ip))
        location = db.locations.delete_one({'ip': location_ip})
        return location_ip, 204

    def put(self, location_ip):
        query = db.locations.find({'ip': location_ip})
        if query.count() == 0:
            abort(404, message="Location {} doesn't exist".format(location_ip))

        args = parser.parse_args()
        ip = args['ip']
        name = args['name']
        idle = ast.literal_eval(args['idle'])
        filter = {'ip': ip}
        location = {"$set":
            {
                'ip' :  ip,
                'name'  :   name,
                'idle'    :  idle
            }
        }

        query = db.locations.update_one(filter,location)

        local_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

        if ip != local_ip:
            return {'message': "This address is not the local IP of the IOT server. Please forward this request to the IOT node at this address."}, 200
            # r = requests.put('http://' + ip + '/locations/' + ip, data ={'ip': ip, 'name': name, 'idle': idle})
            # return r

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

        query = db.locations.find({'ip': args['ip']})
        if query.count() > 0:
            abort(409, message="Location {} already exists".format(args['ip']))


        # return ips

        # return args['ip']

        location = {
            'ip' : args['ip'],
            'name' : args['name'],
            'idle' : ast.literal_eval(args['idle'])
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
