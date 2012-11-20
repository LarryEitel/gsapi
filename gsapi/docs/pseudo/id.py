Pyseudo Generic Features/Functions

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