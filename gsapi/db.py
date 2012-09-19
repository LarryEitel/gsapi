#from flask.ext.pymongo import PyMongo

def get_db(current_app):
    #mongo = PyMongo()
    dbdefaultname = current_app.config['MONGO_DBNAME']
    dbtestname = current_app.config['MONGO_TEST_DBNAME']
    testing = current_app.config['TESTING']
    dbname = dbtestname if testing else dbdefaultname
    db = current_app.extensions['pymongo']['MONGO'][0][dbname]

    return db
