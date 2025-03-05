
from os import environ
from pprint import pprint 

from pymongo import MongoClient # pyright: ignore
from pymongo.results import DeleteResult, InsertOneResult, InsertManyResult, UpdateResult # pyright: ignore
from pymongo.cursor import Cursor # pyright: ignore

from supp.config import todo


def connect_db():    
    mongodb_uri = environ['MONGODB_URI']
    return MongoClient(mongodb_uri)


def list_courses(db):
    return db.courses.find()


def delete_courses(db):
    return db.courses.delete_many({})


def print_result(result):

    if isinstance(result, Cursor):
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
        print(result)


def run_query(db, command):

    query_function = getattr(todo['queries'], command)
    result = query_function(db)
    print_result(result)


def run_all(db):

    print()
    print('.... RESET')
    print_result(delete_courses(db))
    print()

    for i in range(1,16):
        command = f'q{i}'
        print(f'.... QUERY {i} ({command})')
        run_query(db, command)
        if i in [1, 2, 9, 10, 11, 12]:
            print('.... LIST')
            print_result(list_courses(db))
        print()
