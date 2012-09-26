#from flask.ext.pymongo import PyMongo
from flask import current_app

db = current_app.extensions['pymongo']['MONGO'][1]

# def get_db(current_app):
#     #mongo = PyMongo()
#     #dbdefaultname = current_app.config['MONGO_DBNAME']
#     #dbtestname = current_app.config['MONGO_TEST_DBNAME']
#     #testing = current_app.config['TESTING']
#     #dbname = dbtestname if testing else dbdefaultname
#     #db = current_app.extensions['pymongo']['MONGO'][0][dbname]
#     db = current_app.extensions['pymongo']['MONGO'][1]

#     return db
