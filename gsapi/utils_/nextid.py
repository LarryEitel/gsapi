class NextId():
	def __init__(self, collection):
		self.collection = collection
		# insure sparse index on __nextId
		
	def nextId(self):
		collection.find('__nextId')
		return 1234