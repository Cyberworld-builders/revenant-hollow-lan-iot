# Revenant Hollow LAN IOT API

This codebase enables a central server on a Revenant Hollow location LAN to control all of the IOT nodes and interface with the Cloud API. This is also the same codebase installed on all of the nodes to program the effects that the node controls.

Update: this codebase is just for the IOT nodes. You can install most of it on a machine running Ubuntu
for development and testing. Some of the packages and code require Raspberry Pi hardware, so at times
you will have to deploy to a Pi for testing. The idea is that Flask is a great light-weight framework
with a simple API package to expose the nodes on the network. This should help the performance of the
props and effects that are controlled by the Pi. The servers, however will need more robust authentication
and CRUD capabilities since they are exposed to the internet and interface closely with the main database.

Each node will therefore run the most light-weight API possible and store only the data relevant to the active
experiences that are proximal to it geographically. We will use a small, simple Mongodb that lives on the Pi itself
and primarily persist the location haunt object, any effect and phenomena objects relational to it, and possibly
the data of users within its radius of influence and their respective personal haunt data (ie: a user poltergeist
or posession)

## Required Hardware
- A router with port forwarding controlling your LAN.
- A computer that can run Ubuntu.
- At least one Raspberry Pi to control an IOT node.


## Setup

### Ubuntu (for development)

#### Python
- Configure the server machine to use a local static ip
- Ideally, you want a static external ip, too.
- Forward all traffic on the server port to the server ip
- install python
- install pip
- install flask restful `pip install flask-restful`
- install mongo`pip install Flask-PyMongo`

#### Mongo
mongo on ubuntu 20 is kind of a pain. i'll run through the process again later and clean up these docs, but getting it to work was a mess. the main idea is that ubuntu 20 ships with a version of
mongo that you don't want. you have to completely remove that one, then become root with `sudo su` and
more or less follow the below instructions.
- `wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -`
- `echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list`
- `sudo apt-get install -y mongodb-org`


## Raspberry Pi (for production)
