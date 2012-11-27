def slugify(text, collection):
	# insure sparse index on __nextId
	# collection.find('__nextId')
	return text.lower().replace(' ', '_')