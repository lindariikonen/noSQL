
def q1(db):
    '''
    Insert a Single Document
    '''

    return db.courses.insert_one({'_id': 'ARK.ME.032', 'ects': 3, 'name': '3D Modeling II'})


def q2(db):
    '''
    Insert Multiple Documents
    '''

    return db.courses.insert_many([{'_id': 'DPHS.230', 'ects': 2, 'name': 'Academic Writing'}, 
{'_id': 'KONE.411', 'ects': 5, 'name': 'Additive Manufacturing'}])


def q3(db):
    '''
    Find a Document with Equality
    '''

    return db.courses.find_one({'_id': 'KONE.411'})
    

def q4(db):
    '''
    Find a Document by Using the $in Operator
    '''

    return db.courses.find({'_id': {"$in":['DPHS.230', 'KONE.411']}})
  

def q5(db):
    '''
    Find Documents by Using Comparison Operators
    '''

    return db.courses.find({'ects': {"$lt": 5}})
  

def q6(db):
    '''
    Count Documents
    '''

    return db.courses.count_documents({'ects': {"$lt": 5}})


def q7(db):
    '''
    Include and Exclude a Field
    '''

    return db.courses.find({},{'_id':0, 'name':1})


def q8(db):
    '''
    Sort and Limit Result
    '''

    return db.courses.find({},{'_id':0}).sort('ects', -1).limit(1)
  

def q9(db):
    '''
    Update a Document by Using updateOne and $set
    '''

    return db.courses.update_one({'_id':'KONE.411'}, {"$set":{'categories':['A', 'B'], 'prerequisites': [{'course_id': 'MEI.52000'}]}}, upsert=False)


def q10(db):
    '''
    Update a Document by Using updateOne and $push
    '''

    return db.courses.update_one({'_id':'KONE.411'}, {"$push":{'categories':'C'}})


def q11(db):
    '''
    Update Documents by Using updateMany
    '''

    return db.courses.update_many({'_id':{"$ne":'KONE.411'}},{"$set":{'categories':['B']}})


def q12(db):
    '''
    Insert a Document by Using updateOne (upsert)
    '''

    return db.courses.update_one({'_id': 'KONE.412'}, {"$set":{'categories': ['C'], 'name': 'Manufacturing Methods 1'}}, upsert=True)


def q13(db):
    '''
    Find Documents with an Array That Contains a Specified Value
    '''

    return db.courses.find({'categories':'A'})


def q14(db):
    '''
    Find Documents by Using the $or Operator
    '''

    return db.courses.find({"$or":[{'categories':'C'},{'ects': {"$lte": 2}}]})


def q15(db):
    '''
    Find a Document by Using the $elemMatch Operator
    '''

    return db.courses.find({'prerequisites':{"$elemMatch":{'course_id': 'MEI.52000'}}},{'_id':0, 'name':1, 'prerequisites':1})
