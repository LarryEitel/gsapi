
TestGeneric.test_get
LOAD SAMPLE DOCS:

6 docs loaded from: C:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\tests/data/contacts.json!


Verify GET all docs:
RAW REQUEST:
http://localhost:5000/test/Prs

Successfully returned 4 sample docs.

Verify VIRTUAL FIELDS:
RAW REQUEST:
http://localhost:5000/test/Prs?vflds=["dNam"]


Verify GET one doc by id:
RAW REQUEST:
http://localhost:5000/test/Prs/50536c4c2558792c205a299d

Success

Verify WHERE:
RAW REQUEST:
http://localhost:5000/test/Prs?where={"fNam":"sue"}

Success. Expected 1 docs and found 1 docs

Verify WHERE:
RAW REQUEST:
http://localhost:5000/test/Prs?where={"dOn":"$isodate:2012-09-14T23:00Z"}

Success. Expected 1 docs and found 1 docs

Verify WHERE:
RAW REQUEST:
http://localhost:5000/test/Prs?where={"mBy":"$oid:50468de92558713d84b03ed7"}

Success. Expected 1 docs and found 1 docs

Verify SORT:
RAW REQUEST:
http://localhost:5000/test/Prs?sort=[{"fNam": "1"}]

Success

Verify FIELDS LIST ["fNam", "title"]:
RAW REQUEST:
http://localhost:5000/test/Prs?fields=["fNam", "title"]

Success

Verify SKIP & LIMIT:
RAW REQUEST:
http://localhost:5000/test/Prs?skip=1&limit=1

Success. Expected 1 docs and found 1 docs
TestPersons.test_post_one
INSERT NEW PERSON:

RAW REQUEST:
POST http://localhost:5000/test/Prs HTTP/1.1
content-type: application/json
Host: localhost:5000/test
Content-Length: 644

[{"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "larry@stooge.com"}], "lNam": "stooge", "fNam": "larry", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}, {"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "moe@stooge.com"}], "lNam": "stooge", "fNam": "moe", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}, {"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "curly@stooge.com"}], "lNam": "stooge", "fNam": "curly", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}]

## TestPersons.test_post_one
### INSERT NEW PERSON:

#### RAW REQUEST:
POST http://localhost:5000/test/Prs HTTP/1.1
content-type: application/json
Host: localhost:5000/test
Content-Length: 221

{"dOn": "$isodate:2012-09-14T17:41:32.471Z", "rBy": {"$oid": "50468de92558713d84b03fd7"}, "emails": [{"email": "john@doe.com"}], "lNam": "doe", "fNam": "johnathan", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "gen": "m"}

TestGeneric.test_patch
LOAD SAMPLE DOCS:

6 docs loaded from: C:\Users\Larry\__prjs\_ex\_prjs\gsapi\gsapi\tests/data/contacts.json!

Sample data to submit for patch:

RAW REQUEST:
PUT http://localhost:5000/test/Prs HTTP/1.1
content-type: application/json
Host: localhost:5000/test
Content-Length: 266

{"where": {"_id": {"$oid": "50536c4c2558712e205a299b"}}, "patch": {"lvOn": {"$date": 1347893866298}, "rBy": {"$oid": "50468de92558713d84b03fd7"}, "fNam": "longname", "oBy": {"$oid": "50468de92558713d84b03fd0"}, "_c": "Prs", "emails": [{"email": "larry@eitel.com"}]}}

