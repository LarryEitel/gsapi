from flask import Flask, request, session

import json
import sys, os

sys.path.insert(0, os.getcwd())

from views import generic
from views.contacts import contacts
from bson.json_util import dumps
from extensions import RegexConverter
from settings import Config

from flask.ext.pymongo import PyMongo

app = Flask(__name__)

app.config.from_object(Config)

mongo = PyMongo()
app.mongo = mongo
mongo.init_app(app)

# add regex for routing
app.url_map.converters['regex'] = RegexConverter

##################### PUT
@app.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['PUT','PATCH'])
def put(class_name):
    if not class_name in Config.DOMAIN.keys():
        abort(404)
    response = generic.put(class_name)
    return response

##################### POST
@app.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['POST'])
def post(class_name):
    if not class_name in Config.DOMAIN.keys():
        abort(404)
    response = generic.post(class_name)
    return response

##################### GET
@app.route( '/<regex("[\w]*[Ss]"):class_name>/<regex("[a-f0-9]{24}"):id>', methods=['GET'])
@app.route( '/<regex("[\w]*[Ss]"):class_name>?', methods=['GET'])
@app.route( '/<regex("[\w]*[Ss]"):class_name>', methods=['GET'])
def get(class_name, id=None):
    if not class_name in Config.DOMAIN.keys():
        abort(404)
    response = generic.get(class_name, id)
    return response

def main():
    app.host = sys.argv['-h'] if '-h' in sys.argv else '127.0.0.1'
    if '-t' in sys.argv:
        app.config['TESTING'] = True
        print 'Running in test mode.'
    app.debug = '-d' in sys.argv
    app.use_reloader = '-r' in sys.argv
    app.run()

if __name__ == '__main__':
    main()
