
from os import environ
from pprint import pprint 

from pymongo import MongoClient # pyright: ignore
from pymongo.results import DeleteResult, InsertOneResult, InsertManyResult, UpdateResult # pyright: ignore
from pymongo.cursor import Cursor # pyright: ignore
from pymongo.command_cursor import CommandCursor # pyright: ignore

from supp.config import todo, set_prompt


class SomeError(Exception):
    def __init__(self, message="Some error occurred"):
        self.message = message
        super().__init__(self.message)


def connect(host):

    if not host in [
        'mongo',
        'mongo0', 'mongo1', 'mongo2',
        'rs'
    ]:
        raise SomeError('Unknown service')

    if host == 'mongo':
        mongodb_uri = environ['MONGODB_URI']
        client = MongoClient(mongodb_uri)
    
    elif host == 'rs':
        client = MongoClient(
            ['mongo0', 'mongo1', 'mongo2'],
            replicaset='rs',
        )
    
    else:
        client = MongoClient(host, directConnection=True)

    set_prompt(host)
    return client

#
# Course Queries
#

def list_courses(db):
    return db.courses.find()

def delete_courses(db):
    return db.courses.delete_many({})

def insert_courses(db):
    return db.courses.insert_many([
        {
          '_id': 'ARK.ME.032',
          'name': '3D Modeling II',
          'ects': 3,
          'category': 'B'
        },
        {
          '_id': 'DPHS.230',
          'name': 'Academic Writing',
          'ects': 2,
          'category': 'B'
        },
        {
          '_id': 'KONE.411',
          'name': 'Additive Mfg.',
          'ects': 5,
          'category': 'A',
        }
    ])

#
# Category Queries
#

def list_categories(db):
    return db.categories.find()

def delete_categories(db):
    return db.categories.delete_many({})


def print_result(result):

    if isinstance(result, Cursor) or isinstance(result, CommandCursor):
        for doc in result: pprint(doc)

    elif isinstance(result, DeleteResult):
        print('- ok?:', result.acknowledged)
        print('- deleted_count:', result.deleted_count)

    elif isinstance(result, InsertOneResult):
        print('- ok?:', result.acknowledged)
    
    elif isinstance(result, InsertManyResult):
        print('- ok?:', result.acknowledged)
        print('- inserted_count:', len(result.inserted_ids))

    elif isinstance(result, UpdateResult):
        print('- ok?:', result.acknowledged)
        print('- matched_count:', result.matched_count)
        print('- modified_count:', result.modified_count)
        print('- upserted?:', result.upserted_id != None)

    else:
        pprint(result)


def run_query(db, command):

    query_function = getattr(todo['queries'], command)
    result = query_function(db)
    print_result(result)

