Pseudo Mod-Based Model Operations

NOTES:
    _c: model class name, ie, Cmp=Company, Prs=Person, Pl=Place
    When editing a doc, the cloned copy must be inserted in a collection name with the extension _tmp to avoid unique value index problems.
    When creating a new doc, an empty (non-validated) doc must be inserted in a collection name with the extension _tmp to avoid unique value index problems.
TODOs:
    Accommodate ListType.id = unique Id based on _c.docId.nextId 
        collection ids:
            locked   :
            collNam  :
            dId      :
            attribNam:
            nextId   :        


        collection slugs:
            locked   :
            collNam  : cnts
            dId      :
            attribNam: slug
            slugBase   : john_doe
            slugNo   : 2
    Need a controllers.generic.clone
        args:
            _c: <doc model class name>
            doc: <source doc to clone>
            isTmp: <boolean clone to tmp collection?>
QUESTIONS:
    Provision for logging doc changes.
        On add/update/clone/delete, log in a doc with the fields that were changed.
            logaudits
                doc
                    datetime:
                    mBy     : user ObjectID
                    mPl     : modified place 
                    _c      : model class 
                    d_id    : doc ObjectID
                    acts:
                        act     : Action, add, clone, update, delete [a,c,u,d]
                        aNam    : Attribute Name 
                        aVal    : Attribute Val
                        id      : Element Id/elemId
    What/if any validation rules can be delivered to client to relieve client to having to ping API for each/every form element?

New Doc Initialize Form
    CLIENT:
        # Get an empty model doc.
        # Post is used since a tmp doc will be generated.
        HTTP POST: /<_c>
            data: None
    API:
        # Create and initialize an empty model doc
        HTTP POST Triggers: views.generic.post
            querydata:
                _c: <model class name>
                # if no OID exists, this is a new doc
            data: None
            RUN: controllers.generic.post
                args:
                    _c: <model class name>
                    # if no OID exists, this is a new doc. Will need to generate a temporary doc to work with.
                DO THIS:
                    Set collection_name_tmp based on collection name + _tmp.
                    Create an initialized stub doc in cnts_tmp.
                RETURN:
                    status  :
                    doc     : <initialized model doc> # An ObjectID (_id), id (incremented Id) and slug is created.
                    [errors]:
            RETURN:
                status  :
                doc     : <initialized model doc (in temporary collection)>
                [errors]:
    CLIENT:
        Render initialized doc.
Update Doc Initialize Form
    CLIENT:
        # Clone a copy of the doc and insert in collection_name_tmp, ie, cnts_tmp
        # Post is used since a tmp doc will be generated.
        HTTP POST: /<_c>/<OID>
            data: None
    API:
        HTTP POST Triggers: views.generic.post
            querydata:
                _c: <model class name>
                OID: 
            data: None
            RUN: controllers.generic.post
                args:
                    _c: <model class name>
                    OID: 
                    doc: <data>
                    # if doc arg does not exist AND OID exists, this is an EXISTING doc. Generate a clone copy of this doc in the <coll>_tmp collection to work with.
                DO THIS:
                    Is this doc unlocked: controllers.generic.get 
                        data:
                            _c:
                            OID:
                        QUESTION:
                            If doc has been locked longer than mod.doc.lockedDuration, then delete temp doc and unlock?
                        RETURN: 
                            status: #?? for locked
                            msg: "locked, try again"
                    Set collection_name_tmp based on collection name + _tmp.
                    Clone a copy of the doc and insert in collection_name_tmp.
                    Set source doc.locked = to _tmp.doc.OID.
                        # Refuse edits on this doc while locked.
                RETURN:
                    status  :
                    doc     : <cloned copy of source model doc>
                    [errors]: 
            RETURN:
                status  :
                doc     : <cloned copy of model doc (in temporary collection)>
                [errors]:
    CLIENT:
        Render cloned copy of doc.
Update Form Element
    NOTE:
        Each form element will be validated separately in addition to form-level validations where needed.
        Each element can be reverted to previous value. 
    CLIENT:
        # PUT implies that we are UPDATING the resource. Could be a single field or ListType/Array field.
        # OID refers to the doc in the _tmp collection of the corresponding model collection
        # elemId refers to unique key in a ListType field.
        HTTP PUT: /<_c>/<OID>/<attrName>[/<elemId>]
            data:
                attrVal: <new attr value>
    API:
        HTTP PUT Triggers: views.generic.put
            querydata:
                _c      : <model class name>
                OID     : 
                attrName: 
                [elemId]: 
            data: 
                attrVal : <new attr value>

            RUN: controllers.generic.put
                args:
                    _c      : <model class name>
                    OID     : <OID of doc in _tmp collection>
                    attrName: 
                    [elemId]: 
                    attrVal : <new attr value>
                        # if no elemId and attrVal is a single Item, only one item is involved, otherwise, the complete list of all items
                DO THIS:
                    Find and modify attrName of doc at OID in _tmp collection.
                        Log the change
                    Basic fields
                    ModelType fields
                    ListType fields
                    QUESTION:
                        How to determine the type of the attr/field? Hardcode?
                        Schematics has a way to validate ONE field.
                RETURN:
                    status: 
                    attrVal: 
                    [errors]: 
            RETURN:
                status: 
                attrVal:
                [errors]: 
Add to a ListType Form Element
    NOTE:
    CLIENT:
        USER: Click Add Button related to a ListType attr/field.
        Phone Example:
            UI: Insert a Tel (phone) form.
            USER: Click Submit Button

            HTTP POST: /<_c>/<OID>/tels
                data:
                    attrVal: <new attr value>
        New to/parent link to a Company Example:
            Note that user had opportunity to add a new link to any valid Doc/Item, ie, Person, Company, Event, etc. When they clicked, they passed the target_c (model class name), ie, Cmp for a link to a Company AND whether it was targeting a new to/parent or fr/child, ie, targetAs = to/parent OR fr/child.
            Clicking exposes:
                target_c: target model class name 
                targetAs: target doc is a new to/parent OR fr/child
                fr_c    : fr/subject/source model class name
                frOID   : fr/subject/source docOID, what we are linking FROM
            UI: Insert a Lnk form. (Call it Pth?)
                TODOs:
                    Incremental Search:
                        HTTP GET /<target_c>/?<find criteria>
                            search chars 

                    New Parent/Child to what type of item: <dropdown of model classes>
                        TODO: Client has access to static list of all models, ie, Prs:Person, etc.
                          Prompt user to describe the relationship. TODO: UI either access static list of DxRel (relationship titles)? Another AJAX call required?
                            Since the UI knows the typ (type) of document, it can list relevent rel(ationship) titles. If UI is adding a new parent/to relationship, list would include titles such as Son of, Employed by, etc.
                                NOTE: it might be appropriate for UI to prompt for the type/class of parent to create, ie, Person, Company, etc. This would/could enable further filtering of available/appropriate titles from the list.

                    lnkTitle:
                    lnkNote :
                HTTP POST: /<_c>/<OID>/tos
                    data:
                        target_c : target model class name 
                        targetOID: target docOID, what we are linking FROM
                        lnkTypId :
                        lnkTitle :
                        lnkNote  :


        # POST implies that we are ADD an item to a ListType/Array field.
        # attrName must refer to a ListType doc attr
        HTTP POST: /<_c>/<OID>/<attrName>
            data:
                attrVal: <new attr value>
    API:
        HTTP POST Triggers: views.generic.post
            querydata:
                _c           : <model class name>
                OID          : 
                attrName: 
            data: 
                attrVal : <new attr value>

            RUN: controllers.generic.post
                args:
                    _c           : <model class name>
                    OID          : <OID of doc in _tmp collection>
                    attrName: tos <ListType attr name> 
                        # to add new items to a ListType attr, attrName must refer to a ListType field.
                    attrVal : <new attr value>
                        # attrVal must be a single Item
                DO THIS:
                    Validate attrVal for doc model using schematics.
                    Find and append/add attrVal to attrName of doc at OID in _tmp collection.
                    If the attrName is in ['tos', 'frs']:
                        FUNCTION?
                            controllers.pth.mk # mk/generate to/fr pth
                            RETURN:
                                pths:
                                    target:
                                        pth details
                                    source:
                                        pth details
                        Add pths['target'] to tos. Conversely could be frs.
                        Initialize for tmp doc an onSave dict with following:
                            targetOID:
                                attrName: frs 
                                action       : post
                                attrVal : pths['source']
                            NOTE:
                                While submitting/saving changes to a doc:
                                    for OID in targetOID:
                                        Set locked ON
                                    for OID in targetOID:
                                        find OID
                                        do action on attrName field
                                            attrVal
                                    for OID in targetOID:
                                        Set locked OFF
                    If the attrName is ListType like tels, emails, etc:
                        Add email to emails.
                        LOGAUDIT: 
                            OID          :
                            attrName: emails
                            action       : post
                            attrVal : email
                            elemId       : elemId

                        Initialize for tmp doc an onSave dict with following:
                            targetOID:
                                attrName: emails
                                action       : post
                                attrVal : email
                                elemId      : elemId
                            NOTE:
                                While submitting/saving changes to a doc:
                                    for OID in targetOID:
                                        Set locked ON
                                    for OID in targetOID:
                                        find OID
                                        do action on attrName field
                                            attrVal
                                    for OID in targetOID:
                                        Set locked OFF                
                RETURN:
                    status: 
                    attrVal: 
                    [errors]: 
            RETURN:
                status: 
                attrVal:
                [errors]: 

Add to a ListType Attribute
        Client:
            FUNCTION: POST: /<_c>/<tmpOID>/<attr>
                queryData:
                    _c           : <_c>
                    tmpOID       : <tmpOID>
                    attrName: <attr>
                data:
                    action: post
                    attrVal: <attrVal> # could be a to/fr/emails/tels/etc
                    targetOID   : <targetOID>
                    relTypeOID  : <relTypeOID>
                    retTypeTitle: <retTypeTitle>
                    retTypeNote : <retTypeNote>
        API:
    Update Attribute
        Client:
            FUNCTION: PUT: /<_c>/<tmpOID>/<attr>[/<id>]
                # if id is provided, this refers to an element in ListType attr
                queryData:
                    _c           : <_c>
                    tmpOID       : <tmpOID>
                    attrName: <attr>
                    [id]         : <id>
                data:
                    action      : put
                    [srcOID]    : <srcOID>
                    attrVal: <attrVal>
                    # if no id and attrVal is a single Item, only one item is involved, otherwise, the complete list of items
                    targetOID   : <targetOID>
                    relTypeOID  : <relTypeOID>
                    retTypeTitle: <retTypeTitle>
                    retTypeNote : <retTypeNote>
        API:
    Clone Attribute
        Client:
            # in the case of to/fr relation, cloning allows for easily adding more relationships with different roles/titles, etc.
            FUNCTION: PUT: /<_c>/<tmpOID>/<attr>[/<id>]
                queryData:
                    _c           : <_c>
                    tmpOID       : <tmpOID>
                    attrName: <attr>
                    id           : <id>
                data:
                    action      : clone
                    targetOID   : <targetOID>
                    relTypeOID  : <relTypeOID>
                    retTypeTitle: <retTypeTitle>
                    retTypeNote : <retTypeNote>
        API:
    Delete Form Element
        Client:
            FUNCTION: DELETE: /<_c>/<tmpOID>/<attr>/<id>
                queryData:
                    _c           : <_c>
                    tmpOID       : <tmpOID>
                    attrName: <attr>
                    [id]         : <id>
                data:
                    action      : delete  
        API:      
    Cancel Form
        Client:
            Abandon Edit
                FUNCTION: PUT: /<model>/<OID>/tmp 
                    data:
                        action: cancel
        API:
    Submit Form
        Client:
            FUNCTION: PUT: /<model>/<OID>/tmp
                data:
                    action: submit
                    NOTE: srcDoc will have locked set to tmp_id.
        API:
    API:
        Initialize Form
            Create a snapshot of doc 
                FUNCTION: views.generic.tmp
                    Processes:
                        FUNCTION: controllers.generic.tmp 
                            data:
                                OID: 
                            Processes:
                                If no OID
                                    create an unvalidated empty doc
                                    create an unvalidated empty doc
                                    set tmpDoc.locked to 1
                                set tmpDoc.locked to 1
                                return doc with tmpDoc_id
                            response:
                                data:
                                    tmpOID:
                                    tmpDoc:
        Post Form Element
            FUNCTION: views.generic.post 
                queryData:
                    _c           :
                    tmpOID       :
                    attrName:
                    id           :
                data:
                    action      : post
                    attrVal: <attrVal> # could be a to/fr
                    targetOID   : <targetOID>    # optional
                    relTypeOID  : <relTypeOID>   # optional
                    retTypeTitle: <retTypeTitle> # optional
                    retTypeNote : <retTypeNote>  # optional
                Processes:
                    Find the doc 
                    # If no id, and attrData is an array, assume dealing with complete set.
                    Validate
                    Update doc.attr
                        # may involve relating to another doc IF targetOID and other data is provided.
                    Response            
        Put Form Element
            FUNCTION: views.generic.put 
                queryData:
                    _c           :
                    tmpOID       :
                    attrName:
                    id           :
                data:
                    attrVal  : <attrVal> # could be a to/fr
                    [srcOID]      : <srcOID>
                    [targetOID]   : <targetOID>
                    [relTypeOID]  : <relTypeOID>
                    [retTypeTitle]: <retTypeTitle>
                    [retTypeNote] : <retTypeNote>
                Processes:
                    Find the doc 
                    # If no id, and attrData is an array, assume dealing with complete set.
                    Validate
                    Update doc.attr
                        if the attr is tos/frs
                            create to toBeUpdtd{}
                            srcAttributeName    = tos
                            # this means target.attr would be frs
                            targetOID           = Get the element based on id
                            targetAttributeName = frs
                            # generate a dRel docs to be embedded
                                srcDRel    = dRel
                                targetDRel = targetDRel
                            # set toBeUpdtd
                            toBeUpdtd['tos'][id]['targetCollection'] = 'cnts'
                            toBeUpdtd['tos'][id]['targetOID']
                            toBeUpdtd['tos'][id]['targetAttributeName'] = 'frs'
                            toBeUpdtd['tos'][id]['targetDRel'] = targetDRel

                        # may involve relating to another doc IF targetOID and other data is provided.
                    Response
        Delete Form Element
            # Existing form/doc attr can be deleted/removed 
            # Existing form/doc ListType/array can an element deleted/removed 
            FUNCTION: views.generic.delete 
                queryData:
                    _c           :
                    tmpOID       :
                    attrName:
                    id           :
                data:
                    attrVal: <attrVal> # could be a to/fr
                Processes:
                    Find the doc 
                    # If no id, and attrData is an array, assume dealing with complete set.
                    Validate
                    Delete doc.attr
                        if attr is a to/fr 
                            # need to delete element from related doc tos/frs
                    Response                        
        Cancel Form
            FUNCTION: views.generic.put
                queryData:
                    tmpOID: <tmpOID>
                data:
                    action: cancel
                Processes:
                    Delete tmpDoc
        Submit Form
            FUNCTION: views.generic.put
                queryData:
                    tmpOID: <tmpOID>
                data:
                    action: submit
                Processes:
                    Validate
                    Handle toBeUpdtd Actions
                        Updating related docs
                    Unlock tmpDoc.locked
        Response:
            status: 200
            _id   : <OID>
            If error:
                Response with details.

Validate Element
    Client:
        Processes:
            Validate Element
                HTTP: GET: /<model>/<attr>/validate
                    data:
                        Element data
    API:
        Processes:
            Validate Embedded Doc
                FUNCTION: views.generic.validate
        Response:
            status: 200
            If error:
                Response with details.
Validate Embedded Element
    Client:
        Processes:
            Validate Embedded Element
                HTTP: GET: /validate/Phone
                    data:
                        Element data
    API:
        Processes:
            Validate Embedded Doc
                FUNCTION: views.generic.validate
        Response:
            status: 200
            If error:
                Response with details.
Validate Embedded List 
    Client:
        Processes:
            Validate Embedded List
                HTTP: GET: /validate/Phones
                    data:
                        [Element data]
    API:
        Processes:
            Validate Embedded Doc
                FUNCTION: views.generic.validate
        Response:
            status: 200
            If error:
                Response with details.
Doc Edit
    Client:
        Processes:
            Initialize Form
                FUNCTION: GET: /<model>/<OID>/tmp
                    Response:
                        data:
                            tmpOID: <OID>
                            tmpDoc: <doc>

            Update Form Elements
                FUNCTION: PUT: /<_c>/<OID>/<attr>/<id>
                    queryData:
                        _c           : <_c>
                        OID          : <OID>
                        attrName: <attr>
                        id          : <id>
                    data:
                        attrVal: <attrVal>
            Cancel Form
                Abandon Edit
                    FUNCTION: PUT: /<model>/<OID>/tmp 
                        data:
                            action: cancel
            Submit Form
                FUNCTION: PUT: /<model>/<OID>/tmp
                    data:
                        action: submit
                        NOTE: srcDoc will have locked set to tmp_id.
    API:
        Processes:
            Initialize Form
                Create a snapshot of doc 
                    FUNCTION: views.generic.tmp
                        Processes:
                            FUNCTION: controllers.generic.tmp 
                                data:
                                    OID: 
                                Processes:
                                    find OID 
                                    clone a copy of doc
                                    set srcDoc.locked to tmpDoc_id
                                    set tmpDoc.locked to 1
                                    return doc with tmpDoc_id
                                response:
                                    data:
                                        srcOID:
                                        tmpOID:
                                        tmpDoc:
            Put Form Elements
                FUNCTION: views.generic.put 
                    queryData:
                        _c           :
                        OID          :
                        attrName:
                        id           :
                    data:
                        attrData: <data>
                    Processes:
                        Find the doc 
                        # If no id, and attrData is an array, assume dealing with complete set.
                        Validate
                        Update doc.attr
                        Response
            Cancel Form
                FUNCTION: views.generic.put
                    queryData:
                        OID: <srcOID>
                        tmp:
                    data:
                        action: cancel
                        NOTE: srcDoc will have locked set to tmp_id.
                    Processes:
                        Delete tmpDoc 
                        Unlock srcDoc.locked
            Submit Form
                FUNCTION: views.generic.put
                    queryData:
                        OID: <srcOID>
                    data:
                        action: submit
                        NOTE: srcDoc will have locked set to tmp_id.
                    Processes:
                        Loop through all fields and where srcDoc.Attribute is different than tmpDoc.Attribute, update attr.
                        Delete tmpDoc 
                        Unlock srcDoc.locked
        Response:
            status: 200
            _id   : <newId>
            If error:
                Response with details.
Doc Clone
    Client:
        Processes:
            Present Option: Shallow | Deep
    API:
        Processes:
            Shallow
            Deep
        Response:
            status: 200
            _id   : <newId>
            If error:
                Response with details.
Doc Delete
    Shallow
    Deep
Doc Move (Up/Down)
    UpDown
    NewTo
Doc Relate
Doc Relate Edit
Doc Relate Delete
Doc Relate Clone
Doc Relate Move

Create Relation
    Client:
        Processes:
            Present a form to gather details related to the relation to be made between two docs.
            Subject (currently focused doc) of the form, ie, a Prs (person) is given option to create a relation/link to a parent/to or child/fr.
                The new dx doc will associate the currently focussed subject doc with dx.fr_c, dx.fr_id, At this point UI knows the fr_c (subject/currently focused doc/item), frOID, frNam, frNamS.
                UI needs to provide a lookup form to gather the following details:
                    Prompt user to describe the relationship. TODO: UI either access static list of DxRel (relationship titles)? Another AJAX call required?
                    Since the UI knows the typ (type) of document, it can list relevent rel(ationship) titles. If UI is adding a new parent/to relationship, list would include titles such as Son of, Employed by, etc.
                        NOTE: it might be appropriate for UI to prompt for the type/class of parent to create, ie, Person, Company, etc. This would/could enable further filtering of available/appropriate titles from the list.
                Client ultimately needs to provide the target parent/to or child/fr: OID, _c, and dxRelOID.
            HTTP POST: /Dx

    API:
        Processes:
            Validate OAuth acces_token validity. If valid check login session. If valid proceed.
            If login is not valid redirect to login page. If OAuth is not valid send the response status code indicating OAuth access token needds to be renewed. 
            Client calls view function
                FUNCTION: views.dx.create
            Call controller function for creating Dx and DxRel and also pass data.
                FUNCTION: controllers.dx.Create
                    Check OIDs for presence in database. 
                    Pull docs. 
                    If Docs do not exist respond with a status code. With a possible message of session hijacking.
                    Create Dx and DxRel objects and generate OID and other ids.
                    Updating tos and frs of objects.
                        While updating any of these objects if document is found to be locked retry after half seconds.
                        If maximum no. of retries are over send status code to retry in some time.
                    If everything is good send status code to caller.
  
Create Dx Relation
    Client:
        Processes:
            Present a form to gather details related to the relation to be made between two docs.
            Subject (currently focused doc) of the form, ie, a Prs (person) is given option to create a relation/link to a parent/to or child/fr.
                The new dx doc will associate the currently focussed subject doc with dx.fr_c, dx.fr_id, At this point UI knows the fr_c (subject/currently focused doc/item), frOID, frNam, frNamS.
                UI needs to provide a lookup form to gather the following details:
                    Prompt user to describe the relationship. TODO: UI either access static list of DxRel (relationship titles)? Another AJAX call required?
                    Since the UI knows the typ (type) of document, it can list relevent rel(ationship) titles. If UI is adding a new parent/to relationship, list would include titles such as Son of, Employed by, etc.
                        NOTE: it might be appropriate for UI to prompt for the type/class of parent to create, ie, Person, Company, etc. This would/could enable further filtering of available/appropriate titles from the list.
                Client ultimately needs to provide the target parent/to or child/fr: OID, _c, and dxRelOID.
            HTTP POST: /Dx

    API:
        Processes:
            Validate OAuth acces_token validity. If valid check login session. If valid proceed.
            If login is not valid redirect to login page. If OAuth is not valid send the response status code indicating OAuth access token needds to be renewed. 
            Client calls view function
                FUNCTION: views.dx.create
            Call controller function for creating Dx and DxRel and also pass data.
                FUNCTION: controllers.dx.Create
                    Check OIDs for presence in database. 
                    Pull docs. 
                    If Docs do not exist respond with a status code. With a possible message of session hijacking.
                    Create Dx and DxRel objects and generate OID and other ids.
                    Updating tos and frs of objects.
                        While updating any of these objects if document is found to be locked retry after half seconds.
                        If maximum no. of retries are over send status code to retry in some time.
                    If everything is good send status code to caller.
                    
Delete Dx relation
    Client:
        Processes:
            HTTP POST: /Dx/Delete
                data:
                    OID:
    API:
        Processes:
            Validate OAuth acces_token validity. If valid check login session. If valid proceed.
            If login is not valid redirect to login page. If OAuth is not valid send the response status code indicating OAuth access token needds to be renewed. 

            FUNCTION: views.dx.delete
                data:
                    OID:
                
                Call controller function to delete Dx and DxRel record.
                
            FUNCTION: controllers.dx.delete
                data:
                    OID:
                    
                    Check OID for presence in database. If Doc doe not exist respond with a status code. With a possible message of session hijacking.
                    Call function deleteChild with frOID.
                    
            FUNCTION: contoller.dx.delete
                    This function checks for children recursively. If they have multiple tos then the tos of this node and
                    its childre is updated and child and its chilredn are not deleted.
                    If any child has only one tos path leading to parent in consideration then that child and its Dx and DxRel objects are deleted.
                        While deleting any of these objects if document is found to be locked retry after half seonds.
                        If maximum no. of retries are over send status code to retry in some time.
                    After deleting all Dx and DxRel record update parents' froms. 
                    If everything is good send status code to caller.

Delete Dx relation
    Client:
        Processes:
            HTTP POST: /Dx/Update
                data:
                    OID:

    API:
        Processes:
            Validate OAuth acces_token validity. If valid check login session. If valid proceed.
            If login is not valid redirect to login page. If OAuth is not valid send the response status code indicating OAuth access token needds to be renewed. 

            FUNCTION: views.dx.udpate
                data:
                    OID:
            
            
            FUNCTION: controllers.dx.update
                data:
                    OID:
                    
                    Check OID for presence in database. If Doc doe not exist respond with a status code. With a possible message of session hijacking.
                    Client will send request with type and value because any of the attrs can be updated. Any of the following can trigger a
                    change in Dx and DxRel.
                    fr_c, frNam, frNamS, frGen, to_c, toNam, toNamS, toGen, fam, mask, w.
                    Changes in dNam and dNamS of objects will also trigger these changes. Gender change will also effect and class changes too.
                    Check if these attrs have changed. If yes immediate parent's tos will be updated.
                    And like deleteChild call update child with OID.
                
            FUNCTION: controllers.dx.updateChild
                data:
                    OID:
                    
                    Update childrens to path recursively.
                        While updating any of these objects if document is found to be locked retry after half seonds.
                        If maximum no. of retries are over send status code to retry in some time.
                    Update all children and their tos and froms. 
                    If everything is good send status code to caller.
                    
Move an object for new relation
    Client:
        Processes:
            HTTP POST: /Dx/Move
                data:
                    old_toOID  :
                    old_to_c   :
                    old_toNam  :
                    old_toNams :
                    old_frOID  :
                    old_fr_c   :
                    old_frNam  :
                    old_frNamS :
                    new_toOID  :
                    new_to_c   :
                    new_toNam  :
                    new_toNams :
                    new_frOID  :
                    new_fr_c   :
                    new_frNam  :
                    new_frNamS :
                    
        Comment: A move is basically a delete and create.

                    
    dRelTitle 
    dRelDesc
views.dx.Create
views.dx.Create
controllers.dx.Create
controllers.dx.Delete
controllers.dx.Update
controllers.dx.Move


Mary Bell associates herself with Program Group
    # Id = 23
    controllers.dx.Relate(toOID = pggrp, frOID = "13445")
    controllers.Cnt.Associate(to_oid = pggrp, from_oid = MaryBell)
        UI must select the two oids and a set of pre-existing relations will be populated in a drop down list.
        One of the values from this drop down must be picked.
        
        controllers.Dx.CreateDx(to_oid = pggrp, from_oid = MaryBell)
            This function will create a Dx object between these two oid.
        controllers.Dx.CreateDxRel(to_oid = pggrp, from_oid = MaryBell)
            This function will create a new Dx object between these two depending on the relation.
        
        Now Associate will populate tos and froms of both the objects.
        Now update tos of children of Mary Bell. In this case there are none.

Create company GSNI
    controllers.Cnt.CreateCmp(ni)

Mary Bell associates Program Group with GSNI
    controllers.Cnt.Associate(to_oid = ni, from_oid = pggrp)
        UI must select the two oids and a set of pre-existing relations will be populated in a drop down list.
        One of the values from this drop down must be picked.
        
        controllers.Dx.CreateDx(to_oid = ni, from_oid = pggrp)
            This function will create a Dx object between these two oid.
        controllers.Dx.CreateDxRel(to_oid = ni, from_oid = pggrp)
            This function will create a new Dx object between these two depending on the relation.
        
        Now Associate will populate tos and froms of both the objects.
        Now update tos of children of Program Group. In this case there is one child Mary Bell so its tos must be updated.

Create user Sally
    controllers.Cnt.CreateUsr(Sally)

Create company Kirmse
    controllers.Cnt.CreateCmp(Krmse)

Sally associates Kirmse with GSNI
    controllers.Cnt.Associate(to_oid = ni, from_oid = kirmse)
        UI must select the two oids and a set of pre-existing relations will be populated in a drop down list.
        One of the values from this drop down must be picked.
        
        controllers.Dx.CreateDx(to_oid = ni, from_oid = kirmse)
            This function will create a Dx object between these two oid.
        controllers.Dx.CreateDxRel(to_oid = ni, from_oid = kirmse)
            This function will create a new Dx object between these two depending on the relation.
        
        Now Associate will populate tos and froms of both the objects.
        Now update tos of children of Kirmse. However, Kirmse do not have any children.

Sally creates area 104
    controllers.Cnt.CreateCmp(104)
    
Sally associates 104 with Kirmse 
    controllers.Cnt.Associate(to_oid = ni, from_oid = kirmse)
        UI must select the two oids and a set of pre-existing relations will be populated in a drop down list.
        One of the values from this drop down must be picked.
        
        controllers.Dx.CreateDx(to_oid = ni, from_oid = kirmse)
            This function will create a Dx object between these two oid.
        controllers.Dx.CreateDxRel(to_oid = ni, from_oid = kirmse)
            This function will create a new Dx object between these two depending on the relation.
        
        Now Associate will populate tos and froms of both the objects.
        Now update tos of children of Kirmse. However, Kirmse do not have any children.

Now let us say the entire lucid chard diagram is created this way.

Delete troop 1031
    controllers.Cnt.DeleteCmp(1031)
        UI must select the oid of the object to be deleted.
        Delete all children recursively and their Dx and DxRel objects.
        
        controllers.Dx.DeleteDx(oid = 1031)
            controllers.Dx.DeleteChild(1031)
            Update tos.
        
        controllers.Dx.DeleteChild(oid)
            If it has no child delete its Dx and DxRel and then the object.
            












Create company kirmse
    controllers.Cnt.CreateCmpKirmse

Relate kirmse to ni via Dx doc
    Create a relation between parent ni and child kirmse using a Dx doc.
        UI needs to provide selected OID for ni and kirmse.
        Assuming UI is focused on doc kirmse, user can choose to relate this doc to another doc OR add a child relationship.
            UI needs to provide the type relationship this is using a DxRel doc.
            Since kirmse is a Cmp class doc, UI presents a list of available DxRel titles/roles/association.
                For example: 
                    CompanyOf
                    DepartmentOf
                    BranchOf

    controllers.Dx.RelateKirmseToNi
        Pass in:
            toId: OID for ni
            frId: OID for kirmse
            dxRelId: OID for areaOf

        Process:
            Create dx
            Update kirmse
                Add ni as a parent/to of kirmse
                    Add a dRel to kirmse.tos
            Update ni
                Add kirmse a child/fr of ni
                    Add a dRel to ni.frs