Pseudo api Operations

NOTES:
TODOs:
QUESTIONS:

# See /run.py
# Example: @app.route( '/<regex("[\w]*[Ss]"):class_name>/<regex("[a-f0-9]{24}"):id>', methods=['GET'])

POST: /<_c>[/<OID>[/<attrName>]]
	views.generic.post
GET:  /<_c>[/<OID>[/<attrName>[/<elemId>]]]
PUT:  /<_c>/<OID>[/<attrName>[/<elemId>]]
	views.generic.put
