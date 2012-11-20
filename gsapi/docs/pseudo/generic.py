Pyseudo Generic Features/Functions

Create/Post new document.
    Client:
        Processes:
            Init Edit Form
                Initial form from static data, ie, 
                    static.models.<Model>.newForm
                HTTP POST: /<Model>
                    data: 
    API:
        Processes:
            Validate 
                App OAuth exists and valid?
                If passed _id, complain. Should use PUT instead.
                QUESTION: How to handle doc ListType fields that are embedded docs?
                    For example, client returns doc with list of embedded email docs. These need to be validated.
                    TODO: Pseudo code this process. Handle invalid embedded docs.
            Generate a new _id
                PROBLEM: Getting a new _id by creating a stub doc will be problematic in view of the fact that in some models there may be fields that have required values.
                    Solution? Maintain a set of _id's in a mongo.collection. Create a blank doc and grab the new OID. Use it to persist a new doc.
                FUNCTION: controllers.app.next_id
                NOTE: Use of _id. variableOID variable_id, variableId
                    _id is the name of the primary key field used by mongo. It represents the mongo document ObjectID.
                    If a field references an _id in another model, use field_id/attribute_id since it refers to an ObjectID value in another collection.
                    If a field contains the String value of an ObjectID, use fieldOID/attributeOID.
                    Python variables that are set to the value of an ObjectID are suggested to be named variableNameOID.
            Generate a unique numeric Id if implemented.
                Whenever Id or fieldId/attributeId is referenced, it refers to a unique numeric value similar to a RDBMS incremented primary key.
                See code examples:
                    http://www.lovemikeg.com/2010/08/11/auto-increment-with-mongodb/
                        CODE: http://shiflett.org/blog/2010/jul/auto-increment-with-mongodb
                    http://stackoverflow.com/questions/11990254/how-to-create-a-worldwide-unique-guid-uuid-system-for-mongo-with-python
                TODO: Create function to generate a unique numeric Id for a collection.
                    FUNCTION: controller.generic.nextId 
                        data:
                            _c    : <model class> # ie, Cmp (Company)
                            _limit: 1 # ie, last Max value
                        Processes:
                            Find next MAX Id value for provided _c(lass).
                                nextId = MAX_Id_value + 1
                                Loop until successful
                                    Try to create a new key doc with Id = nextId
                                        If fails, another process (race condition) bet us to it. Increment and try again.
                                            nextId += 1
            Generate a unique slug.
                Create a slug using dNam. Must be unique for in model (_c) class. If proposed slug exists, increment from the trailing numeric portion occuring in proposed slug.
                Examples:
                    dNam: John Adams = slug: john_adams
                        if john_adams exists, slug = john_adams1
                        if john_adams1 exists, slug = john_adams2

                See sample slugify code examples:
                    http://flask.pocoo.org/snippets/5/
                    https://gist.github.com/1428479
                    http://pypi.python.org/pypi/django-autoslug

                FUNCTION: controllers.generic.slugify
                    data:
                        _c  : Prs # model class # ie (Person)
                        dNam: John Adams # ie, last Max value
                    Processes:
                        Generate slug based on dNam
                            TODO: Existing slug generator?
                        slug = slugify(dNam)
                        incr = ''
                        Loop until successful
                            # slug not already used?
                            if not mongo.<collection>.find slug + incr:
                                # try adding slug to db.slugs
                                Loop until successful
                                    # add to slugs
                                    response = controller.generic.post
                                        data:
                                            _c     : Slug # model class # ie (Person)
                                            model_c: # model class # ie (Person)
                                        Return:
                                            Success:
                                                status: True
                                                _id:  
                                            Failed:
                                                status: False
                                    if response == False:
                                        failed, someone beat us to it (race condition)
                                        # increment slug suffix value.
                                        incr = str(val(incr) + 1)
                                        continue
                                    slug = slug + str(val(incr)) if incr else ''
                                    break
                            Try to create a new key doc with _key = next_key
                                If fails, another process (race condition) bet us to it. Increment and try again.
                                    next_key += 1
                        incr = numeric portion of slug
                        TODO: Function to increment slug if exists.
                data:
                    _c: Prs
                    dNam: John Adams
            Insert new doc 
                FUNCTION: controller.generic.post
                    data:
                        _id : <new_id>
                        slug : <slug>
                mongo using new _id, slug and _key (if used) along with data.
                TODO: Logging event in Mod Class and Logger
            Add to Index.
            TESTS
        Response:
            status: 200
            _id   : <newId>
            If error:
                Response with details.
    Client:
        Processes:
            Request newly added doc using returned _id.
                HTTP GET: /<model>/<id>
Update/Put document.
    # Changes can be made only to non List Fields (ListType).
    Client:
        Processes:
            Edit User Profile
                HTTP GET: /Usr/<id>
                HTTP GET: /Usr/<slug>
    API:
        Processes:
            # Find and return document
            FUNCTION: views.generic.get
                data:
                    _id : abcd
                Processes:
                    mongo find on _id or slug
                Response:
                    status: 200
                        doc:
                    If error:
                        Response with details.
    Client:
        Processes:
            Submit changes
                HTTP PATCH: /<model>/<id>    
                    ie: Usr                   
                        data:
                            uNam: jkutz
                            fNam: Josh
                            lNam: Kutz
                            gen : m
                            pw  : m
    API:
        Processes:
            FUNCTION: views.generic.put
                Validate supplied data.
                    # reject any keys that represent ListType fields.
                Update mongo.
                    TODO: Logging event in Mod Class and Logger
                Update index.

                Returns:
                    status: 200
                    If error:
                        Response with details.
Edit/Update a ListField (ListType).
    Client:
        # Any element in ListField that is altered must submit changes to API. For example, if an item is marked as prim(ary), Client must submit change related to UNselected item.
        Processes:
            Edit an item in a List Field.
                HTTP PUT: /<model>/<id>
                    ie: emails
                        data:
                            - _field : emails
                              _offset: 0
                              address: jkutz@gmail.com
                              # typ comes from static.typs.Email
                              typ    : work # Email.work
                              # Client is responsible to submit change to previously selected prim(ary) item.
                              prim   : 1
                              # Client is responsible to submit change to previous item w(eight) values.
                              w      : 100
                              note   : "misc comment"
                              # delete this line
    API:
        Processes:
            FUNCTION: views.generic.put
                Processes:
                    find model doc, ie, Usr 
                    find ListType field element via _offset
                    Validate Model 
                    Update element in List field
                        TODO: Logging event in Mod Class and Logger
                response:
                    status: 200
                    If error:
                        Response with details.
Delete/Del document
Add an element to a ListField (ListType)
Delete/Del an element in a ListField

