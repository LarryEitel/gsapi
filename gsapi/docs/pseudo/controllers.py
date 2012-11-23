Pseudo controllers Operations

NOTES:
TODOs:
QUESTIONS:


# controllers.py
class Generic
    def __init__(self, db, es = None):
        #: Doc comment for instance attribute db
        self.db = db
        self.es = es
    def post(self, **kwargs):
        session    = kwargs['session'] if 'session' in kwargs else {}
        db         = self.db
        _c         = kwargs['_c']
        model      = getattr(models, _c)
        collNam    = model.meta['collection']
        collNamTmp = model.meta['collNam'] + '_tmp'
        coll       = db[collNam]
        collTmp    = db[collNamTmp]

        # QUESTION: How to init an empty schematic model with defaults, etc.
        # if no OID exists, this is a new doc. Will need to generate a temporary doc to work with.
        if not 'OID' in kwargs:
            # create tmpDoc
            # init model for this doc
            m      = model({})
            m.id   = barak.nextId()
            m.slug = barak.slugify()
            tmpOID = str(collTmp.insert(m.to_python(), safe = True))
            # save tmpOID in session
            pass

        # does tmpDoc already exist
        elif 'tmpOID' in session:
            tmpOID = session['tmpOID']

        # if OID exists, need tmpOID
        elif not 'OID' in kwargs:
            pass

controllers.generic.get 
controllers.generic.put
controllers.generic.nextId
