import time
def nextId(collection):
	"Returns the next unique Id available for a collection via the __nextId collection field."

	max_locked_duration = 5			# In seconds

	response = {}
	response['status'] = 200
	where = {'_id': '__nextId'}
	nextid_doc = collection.find_one({'_id': '__nextId'})
	if not nextid_doc:
		doc = {'_id': '__nextId',
		       'locked': False,
		       'nextId': 2}
		try:
			collection.insert(doc)
		except:
			pass
		response['nextId'] = 1
		return response

	time_start = time.time()
	while True:
		try:
			nextid_doc = collection.find_and_modify(query = where, update = {"$set": {'locked': True}}, new = True)
		except:
			elapsed_time = time.time() - time_start
			if elapsed_time > max_locked_duration:
				response['error']  = 'max_locked_duration reached getting NextID'
				response['status'] = 400
				return response
			pass
		
		nextId = nextid_doc['nextId']
		collection.find_and_modify(where, update = {"$set": {'nextId': nextId + 1, 'locked': False}}, new=True)
		response['nextId'] = nextId
		return response
