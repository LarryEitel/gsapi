import datetime

def logit(usrId, docDict, method='post'):
    now = datetime.datetime.utcnow()

    if method == 'post':
        docDict['oBy'] = usrId
        docDict['oOn'] = now
        docDict['cBy'] = usrId
        docDict['cOn'] = now

    docDict['mBy'] = usrId
    docDict['mOn'] = now

    return docDict

