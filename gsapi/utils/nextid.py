class NextId():
	def __init__(self):
		pass
	
	def nextId(self, collection):
		# insure sparse index on __nextId
		# collection.find('__nextId')
		return 1234