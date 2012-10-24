# cnt, cntX, cntXRel
'''
create usr Bill
create cmp ACME


create some cntXrel docs, ie, Admin, manager, supervisor

cntX
    from_id = Bill
    to_id = Sue
    dNam = cntXRel.name + ' ' + to.dNam


cntXRel
    subject_gender = m 
    target_gender = f
    toName = Father of
    fromReverse = Daughter of
    maternal = 



Bill is Admin of ACME
ACME is Employer of Bill

Bill is Father of Sue
Sue is Daughter of Bill

if you're setting on Bill
    Add cntX 
        Pick Sue
            Show list of available cntXRel 
                list cntXRel where subject_gender = m and
                    target_gender = f 

            pick from cntXRel 


get cntXRel doc for Admin

create cntX between usr.Bill & cmp.ACME as cntX.Admin of ACME

Question:

Consider following scenario:

create user Sam
create user Jen
create user Paul

create cntXRel father, son, mother, daughter and grandfather

sitting on Sam
    set relationship between Sam and Jen as father and daughter

sitting on Jen
    set relationship between Jen and Paul as mother and son

Question is how we would establish relationship between Sam and Paul?

The above scenario depicts relationship between three entities.
How will we manage more entities related togeher?

Possible solution:

    Users need to explicitly set relationship.

One complex situation is persented here:

create user Sam
create user Paul
create user Jen
create user Lisa

Sam and Jen are brother and sister.
Paul and Lisa are brother and sister.

Sam is married to Lisa and Paul is married to Jen. Cyclic relationship.

Possible solution:

    Establish two relationships.
    Jen is sister of Sam.
    Jen is sister-in-law of Sam.
    Sam is husband of Lisa.
    Sam is brother-in-law of Lisa.


Question:

ni
    kirmse
        104
            1031
                Bill

acme 
    abc
        1031
            Bill


Question:

create company A
create company B

    B is a child company A

create user Sam

    Sam is an employee of B

Does this mean Sam is also an employee of A?

Trivial question:

Sam and Paul are friends. Jen is sister of Paul but not a friend of Sam.
Will there exist a relationship between Sam and Jen?

There should not exist a relationship unless stated. We cannot have a
relationship like friend's sister.

Will there be relations like ex-eployee and ex-employer? I think there
should be such relationships.

https://developers.google.com/gdata/docs/2.0/elements#gdGeoPt
Deprecated. This element is deprecated. For geotagging data, use GeoRSS instead.

Questions:

1. Which model is the containing entity of a place?
2. What are all possible types of place relationships?
3. We need followers count in Widgets?
4. Website field of place?
5. International phone no of place?
6. Can have a field category in event models?
7. Author URL in review class?
8. Who of message?

Testing strategy:

1. We use Selenium/automated scripts to generate users/companies/
   Contacts/ContactRelations/Places/Widgets/Shares/Events/Notes/Reviews/
   Ratings.
2. We also try to send invalid input.
3. We try to modify data of db generated this way using valid/invalid
   requests.
4. We try to delete data of db with valid/invalid requests.
5. We search our datanase ensuring both Elastic and Mongo are tested.
6. We run the a subset of above tests manually.
'''