
TestGeneric.test_get
LOAD SAMPLE DOCS:

6 docs loaded from: C:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\tests/data/contacts.json!

GET ALL docs:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args = {
    "class_name": "Prs"
}

Successfully returned 4 sample docs.

VIRTUAL FIELDS:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args = {
    "class_name": "Prs", 
    "vflds": [
        "dNam"
    ]
}

Verify virtual field was returned with result. 
Success

ONE BY ID:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args = {
    "class_name": "Prs", 
    "id": "50536c4c2558712e205a269a"
}

Success

WHERE by fNam:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args = {
    "class_name": "Prs", 
    "where": {
        "fNam": "sue"
    }
}

Success. Expected 1 docs and found 1 docs
Success

WHERE by datetime:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args {'class_name': 'Prs', 'where': {'dOn': datetime.datetime(2012, 9, 14, 23, 0, tzinfo=<isodate.tzinfo.Utc object at 0x0360D110>)}}

Success. Expected 1 docs and found 1 docs
Success

WHERE by ObjectId:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args {'class_name': 'Prs', 'where': {'mBy': ObjectId('50468de92558713d84b03ed7')}}

Success. Expected 1 docs and found 1 docs
Success

SORT:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args {'class_name': 'Prs', 'sort': [{'fNam': '1'}]}

Success

FIELDS LIST:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args = {
    "class_name": "Prs", 
    "fields": [
        "fNam", 
        "title"
    ]
}

Success

SKIP & LIMIT:
CALL:
generic  = controllers.Generic(db)
generic.get(**args)
WITH:
args = {
    "class_name": "Prs", 
    "limit": "1", 
    "skip": "1"
}

Success. Expected 1 docs and found 1 docs
## nTestGeneric.test_post_list
### INSERT NEW PERSONS:

POST ONE doc:
CALL:
controllers.generic.get(db, **args)
WITH:
args = {'class_name': 'Prs', 'docs': [{'rBy': ObjectId('50468de92558713d84b03fd7'), 'emails': [{'email': 'larry@stooge.com'}], 'lNam': 'stooge', 'mOn': datetime.datetime(2012, 9, 27, 21, 43, 33, 927000, tzinfo=<isodate.tzinfo.Utc object at 0x0360D110>), 'fNam': 'larry', 'oBy': ObjectId('50468de92558713d84b03fd0'), 'gen': 'm'}, {'rBy': ObjectId('50468de92558713d84b03fd7'), 'emails': [{'email': 'moe@stooge.com'}], 'lNam': 'stooge', 'mOn': datetime.datetime(2012, 9, 27, 21, 43, 33, 927000, tzinfo=<isodate.tzinfo.Utc object at 0x0360D110>), 'fNam': 'moe', 'oBy': ObjectId('50468de92558713d84b03fd0'), 'gen': 'm'}, {'rBy': ObjectId('50468de92558713d84b03fd7'), 'emails': [{'email': 'curly@stooge.com'}], 'lNam': 'stooge', 'mOn': datetime.datetime(2012, 9, 27, 21, 43, 33, 927000, tzinfo=<isodate.tzinfo.Utc object at 0x0360D110>), 'fNam': 'curly', 'oBy': ObjectId('50468de92558713d84b03fd0'), 'gen': 'm'}]}

## nTestGeneric.test_post_one
### INSERT NEW PERSON:

POST ONE doc:
CALL:
controllers.generic.get(db, **args)
WITH:
args = {'class_name': 'Prs', 'docs': [{'rBy': ObjectId('50468de92558713d84b03fd7'), 'emails': [{'email': 'john@doe.com'}], 'lNam': 'doe', 'mOn': datetime.datetime(2012, 9, 27, 21, 43, 33, 927000, tzinfo=<isodate.tzinfo.Utc object at 0x0360D110>), 'fNam': 'johnathan', 'oBy': ObjectId('50468de92558713d84b03fd0'), 'gen': 'm'}]}

INSERTED OBJECT_ID: 506c58ce2558712cbc82f11d
TestGeneric.test_put
LOAD SAMPLE DOCS:

6 docs loaded from: C:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\tests/data/contacts.json!
Sample data to submit for patch:

PUT ONE doc:
CALL:
controllers.generic.put(db, **args)
WITH:
args = {'class_name': 'Prs', 'usrid': ObjectId('50468de92558713d84b03fd0'), 'data': {'where': {'_id': ObjectId('50536c4c2558792c206a299d')}, 'patch': {'rBy': ObjectId('50468de92558713d84b03fd7'), 'oOn': datetime.datetime(2012, 9, 27, 21, 43, 33, 927000, tzinfo=<isodate.tzinfo.Utc object at 0x0360D110>), 'fNam': 'longname', 'oBy': ObjectId('50468de92558713d84b03fd0'), '_c': 'Prs', 'emails': [{'email': 'larry@eitel.com'}]}}}


TestGeneric.test_get
LOAD SAMPLE DOCS:

6 docs loaded from: C:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\tests/data/contacts.json!

Verify GET all docs:
RAW REQUEST:
http://localhost:5000/Prs

Successfully returned 4 sample docs.

Verify VIRTUAL FIELDS:
RAW REQUEST:
http://localhost:5000/Prs?vflds=["dNam"]


Verify GET one doc by id:
RAW REQUEST:
http://localhost:5000/Prs/50536c4c2558712f205a299c

Success

Verify WHERE:
RAW REQUEST:
http://localhost:5000/Prs?where={"fNam":"sue"}

Success. Expected 1 docs and found 1 docs

Verify WHERE:
RAW REQUEST:
http://localhost:5000/Prs?where={"dOn":"$isodate:2012-09-14T23:00Z"}

Success. Expected 1 docs and found 1 docs

Verify WHERE:
RAW REQUEST:
http://localhost:5000/Prs?where={"mBy":"$oid:50468de92558713d84b03ed7"}

Success. Expected 1 docs and found 1 docs

Verify SORT:
RAW REQUEST:
http://localhost:5000/Prs?sort=[{"fNam": "1"}]

Success

Verify FIELDS LIST ["fNam", "title"]:
RAW REQUEST:
http://localhost:5000/Prs?fields=["fNam", "title"]

Success

Verify SKIP & LIMIT:
RAW REQUEST:
http://localhost:5000/Prs?skip=1&limit=1

Success. Expected 1 docs and found 1 docs
TestPersons.test_post_one
INSERT NEW PERSON:

RAW REQUEST:
POST http://localhost:5000/Prs HTTP/1.1
content-type: application/json
Host: localhost:5000
Content-Length: 644

[{"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "larry@stooge.com"}], "lNam": "stooge", "fNam": "larry", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}, {"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "moe@stooge.com"}], "lNam": "stooge", "fNam": "moe", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}, {"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "curly@stooge.com"}], "lNam": "stooge", "fNam": "curly", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}]

Success. RESPONSE:
{u'docs': [{u'doc': {u'cBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'rBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'oOn': {u'$date': 1349277949759L}, u'cOn': {u'$date': 1349277949759L}, u'shares': [], u'emails': [{u'email': u'larry@stooge.com'}], u'lNam': u'stooge', u'mOn': {u'$date': 1349277949759L}, u'fNam': u'larry', u'oBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'_id': {u'$oid': u'506c58fd2558710444b16b13'}, u'_c': u'Prs', u'gen': u'm', u'mBy': {u'$oid': u'50468de92558713d84b03fd7'}}, u'id': u'506c58fd2558710444b16b13'}, {u'doc': {u'cBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'rBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'oOn': {u'$date': 1349277949759L}, u'cOn': {u'$date': 1349277949759L}, u'shares': [], u'emails': [{u'email': u'moe@stooge.com'}], u'lNam': u'stooge', u'mOn': {u'$date': 1349277949759L}, u'fNam': u'moe', u'oBy': {u'$oid': u'50468de92558713d84b03fd0'}, u'_id': {u'$oid': u'506c58fe2558710444b16b14'}, u'_c': u'Prs', u'gen': u'm', u'mBy': {u'$oid': u'50468de92558713d84b03fd7'}}, u'id': u'506c58fe2558710444b16b14'}, {u'doc': {u'cBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'rBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'oOn': {u'$date': 1349277950389L}, u'cOn': {u'$date': 1349277950389L}, u'shares': [], u'emails': [{u'email': u'curly@stooge.com'}], u'lNam': u'stooge', u'mOn': {u'$date': 1349277950389L}, u'fNam': u'curly', u'oBy': {u'$oid': u'50468de92558713d84b03fd0'}, u'_id': {u'$oid': u'506c58fe2558710444b16b15'}, u'_c': u'Prs', u'gen': u'm', u'mBy': {u'$oid': u'50468de92558713d84b03fd7'}}, u'id': u'506c58fe2558710444b16b15'}], u'total_inserted': 3, u'total_invalid': 0}
INSERTED OBJECT_ID: 506c58fd2558710444b16b13
## TestPersons.test_post_one
### INSERT NEW PERSON:

#### RAW REQUEST:
POST http://localhost:5000/Prs HTTP/1.1
content-type: application/json
Host: localhost:5000
Content-Length: 221

{"dOn": "$isodate:2012-09-14T17:41:32.471Z", "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "john@doe.com"}], "lNam": "doe", "fNam": "johnathan", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}

Success.
#### RESPONSE:
{u'docs': [{u'doc': {u'cBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'dOn': {u'$date': 1347644492000L}, u'rBy': {u'$oid': u'50468de92558713d84b03fd7'}, u'oOn': {u'$date': 1349277950397L}, u'cOn': {u'$date': 1349277950397L}, u'shares': [], u'emails': [{u'email': u'john@doe.com'}], u'lNam': u'doe', u'mOn': {u'$date': 1349277950397L}, u'fNam': u'johnathan', u'oBy': {u'$oid': u'50468de92558713d84b03fd0'}, u'_id': {u'$oid': u'506c58ff2558710444b16b16'}, u'_c': u'Prs', u'gen': u'm', u'mBy': {u'$oid': u'50468de92558713d84b03fd7'}}, u'id': u'506c58ff2558710444b16b16'}], u'total_inserted': 1, u'total_invalid': 0}
INSERTED OBJECT_ID: 506c58ff2558710444b16b16
TestGeneric.test_patch
LOAD SAMPLE DOCS:

6 docs loaded from: C:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\tests/data/contacts.json!
Sample data to submit for patch:

RAW REQUEST:
PUT http://localhost:5000/Prs HTTP/1.1
content-type: application/json
Host: localhost:5000
Content-Length: 266

{"where": {"_id": {"$oid": "50536c4c2558712e205a299b"}}, "patch": {"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "fNam": "longname", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "_c": "Prs", "emails": [{"email": "larry@eitel.com"}]}}

Verify submitted patch was successful.
Success
