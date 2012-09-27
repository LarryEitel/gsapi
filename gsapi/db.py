#from flask.ext.pymongo import PyMongo
from flask import Flask, current_app
from settings import Config

from flask.ext.pymongo import PyMongo
from pymongo import Connection

#app = Flask(__name__)

#app.config.from_object(Config)

#mongo = PyMongo()
#mongo.init_app(app)

#try:
    #with app.app_context():
        ## within this block, current_app points to app.
        #if not 'pymongo' in current_app.extensions:
            #current_app.mongo.init_app(current_app)

    #db = current_app.extensions['pymongo']['MONGO'][1]
#except:
    #db = None

def get_db2(dbname):
    c = Connection()
    return c[dbname]

def get_db3():


    app = Flask(__name__)

    app.config.from_object(Config)

    mongo = PyMongo()
    mongo.init_app(app)


    return app.extensions['pymongo']['MONGO'][1]


def get_db(current_app):
    #mongo = PyMongo()
    #dbdefaultname = current_app.config['MONGO_DBNAME']
    #dbtestname = current_app.config['MONGO_TEST_DBNAME']
    #testing = current_app.config['TESTING']
    #dbname = dbtestname if testing else dbdefaultname
    # db = current_app.extensions['pymongo']['MONGO'][0][dbname]

    if not 'pymongo' in current_app.extensions:
        current_app.mongo.init_app(current_app)

    db = current_app.extensions['pymongo']['MONGO'][1]

    return db
