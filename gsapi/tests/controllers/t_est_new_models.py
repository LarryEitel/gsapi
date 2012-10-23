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


'''