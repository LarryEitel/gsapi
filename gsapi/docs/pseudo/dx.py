Pseudo Dx Features/Functions

Create user Mary Bell
    controllers.cnt.CreateUsr(MaryBell)
    
Create company Program Group
    controllers.Cnt.CreateCmp(pgrp)
    
Create Relationship between two docs
    NOTES:
        Is it required to capture dxRefOID? Only parent/child
    Example subject doc: 
        doc._c   : Prs
        doc.dNamS: john_adams
        doc.gen  : m
    User can relate/link/associate most docs with most other docs. To do so, user must:
        Choose to relate to a parent or child.
            Radio button:
                targetAs = 
                    to/parent
                    fr/child
            # based on selection will determine which doc is parent and which is child
            Example: targetAs: parent
        Choose a target doc to be related.
            Incremental search form to select a target doc to relate to.
            FUNCTION: views.generic.get
            Example selected:
                targetDoc:
                    OID   :
                    _c    : Cmp
                    _dNamS: acme
        UI Example
            Form:
                dNamS: john_adams
                Places:
                    Home at 123 Maple, San Diego, California, 92117
                    Office at 123 Maple, San Diego, California, 92117
                    Service Group at 123 Maple, San Diego, California, 92117
                Contacts:
                    Son of Timothy
                    Father of Mary
                    Employed by acme/Subsidiary of ABC/Branch of HIPO
                    Service Overseer of Hilltop Congregation
                Events:
                    Born on date
                    Married on date
                Notes: Add New Appears on mouse over
                    date subject asdfasdfasdf..... 
                    date subject asdfasdfasdf..... 
                    date subject asdfasdfasdf..... 
                    date subject asdfasdfasdf..... 

                Add New (List Model Class types that have no items yet)
                    Comment 
                    Project

                Parent Relations/Associations: 
                    Button: Add New
                Child Relations/Associations:
                    Father of Mary
                    Button: Add New
            Form Actions:
                Clicked on Button Add New (parent/child)
                    Hide: Button: Add New
                    JS unhide form:
                        targetAs: to/fm
                        Select target Parent: ______. (Incremental)
                            QUESTION: Option to Add new doc to be created and then selected?
                            Show list.
                                Pick from list.
                                On select, show Submit Button.
                                returns:
                                    OID   :
                                    _c    : Cmp
                                    _dNamS: acme
                            Hide this form.
                        Show item with dxRels from which to select:
                            Describe john_adams as: dropdown[v] acme  [Submit after selection]
                                QUESTION:
                                    What if desired relationship title is not provided? Can one be added dynamically.

                                DropDown: 
                                    TODO: FUNCTION: views.dx.get
                                        data:
                                            targetAs: to
                                            gen     : m 
                                            sub_c   : Prs 
                                        Process:
                                            query mongo like:
                                                find:
                                                    filter:
                                                        Prs in fr_c 
                                                        gen in frGens
                                                    fields:
                                                        OID 
                                                        to_c 
                                                        toNam 
                                                        toNamS
                                                    sort:
                                                        w
                                    return:
                                        dxRelOID:
                                        to_c    : Cmp 
                                        toNam   : Employed by
                                        toNamS  : employed_by

                                Show:
                                    Revise line
                                        from:
                                            Describe john_adams as: dropdown acme
                                        to:
                                            Employed by acme [Optional Title: _____] [Optional Note: ____] Submit Button appears if optional fields are changed.

                                Show:
                                    Revise line
                                        from:
                                            Employed by acme [Optional Title: Manager] [Optional Note: IT Dept] Submit Button appears if optional fields are changed.
                                        to:
                                            Employed by acme. Title: Manager. Note: IT Dept


                                Submit:
                                    HTTP: POST: /Dx
                                        data:
                                            toOID    : acme (placeholder)
                                            frOID    : john_adams (placeholder)
                                            dRelTitle: Manager
                                            dRelNote : IT Dept
                                            dxRelOID : employed_by (placeholder)

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
                    Client will send request with type and value because any of the attributes can be updated. Any of the following can trigger a
                    change in Dx and DxRel.
                    fr_c, frNam, frNamS, frGen, to_c, toNam, toNamS, toGen, fam, mask, w.
                    Changes in dNam and dNamS of objects will also trigger these changes. Gender change will also effect and class changes too.
                    Check if these attributes have changed. If yes immediate parent's tos will be updated.
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