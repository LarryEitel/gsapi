import datetime

def logit(usr, docDict, method=''):
    now = datetime.datetime.utcnow()


    if method == 'post':
        docDict['oBy'] = usr['OID']
        docDict['oOn'] = now
        if usr['at']:
        	docDict['oAt'] = usr['at'] # lattitude, longitude (x,y)
        docDict['cBy'] = usr['OID']
        docDict['cOn'] = now
        if usr['at']:
        	docDict['cAt'] = usr['at']

    docDict['mBy'] = usr['OID']
    docDict['mOn'] = now
    if usr['at']:
    	docDict['mAt'] = usr['at']

    return docDict

