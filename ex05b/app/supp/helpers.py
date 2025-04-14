
import yaml # pyright: ignore
from prettytable import PrettyTable # pyright: ignore
from os import path
from supp.config import todo

from os import environ
import json
from cassandra.auth import PlainTextAuthProvider #pyright: ignore

import subprocess

_CREATE_KEYSPACE = \
'''CREATE KEYSPACE IF NOT EXISTS datadb300 
WITH replication = {
  'class':'SimpleStrategy',
  'replication_factor': 1
}'''
_USE_KEYSPACE = 'USE datadb300'

_RESET_QRY = {
    'qa': [
        _CREATE_KEYSPACE, _USE_KEYSPACE, 
        'DROP TABLE IF EXISTS videos_by_title_year'
    ],
    'qb': [
        _CREATE_KEYSPACE, _USE_KEYSPACE, 
        'DROP TABLE IF EXISTS bad_videos_by_tag_year',
        'DROP TABLE IF EXISTS videos_by_tag_year'
    ],
    'qc': [
        _CREATE_KEYSPACE, _USE_KEYSPACE, 
        'DROP TABLE IF EXISTS videos_by_actor',
        'DROP TABLE IF EXISTS videos_by_genre',
        'DROP TYPE IF EXISTS video_encoding'
    ],
    'qd': [
        _CREATE_KEYSPACE, _USE_KEYSPACE, 
        'DROP TABLE IF EXISTS videos'
    ]
}

_FB_QRY = {
    'qa_2': 'SELECT COUNT(*) FROM videos_by_title_year',

    'qb_2': 'SELECT COUNT(*) FROM bad_videos_by_tag_year',
    'qb_4': 'SELECT COUNT(*) FROM videos_by_tag_year',

    'qc_3': 'SELECT COUNT(*) FROM videos_by_actor',
    'qc_6': 'SELECT COUNT(*) FROM videos_by_genre',
    
    'qd_3': 'SELECT COUNT(*) FROM datadb300.videos',
    'qd_6': 'SELECT COUNT(*) FROM datadb300.videos',
    'qd_9': 'SELECT COUNT(*) FROM datadb300.videos',
}

_TODOS_PATH = path.join(
    path.dirname(path.abspath(__file__)), '..', 'todos'
)

_BLUE = '\033[94m'
_GRAY = '\033[90m'
_BOLD = '\033[1m'
_RESET = '\033[0m'

def _load_queries():
    '''
    Load queries from file to dict
    '''    
    qry_path = path.join(_TODOS_PATH, todo['folder'], 'queries.yml')
    with open(qry_path, 'r') as file:
        queries_dict = yaml.safe_load(file)
    return queries_dict

def _bold_print(text):
    print(f'\n{_BOLD}{text.upper()}{_RESET}')

def _print_records(records, color=None):
    '''
    '''
    table = PrettyTable()
    table.align = 'l'
    table.field_names = records[0].keys()

    table.add_rows ([[ 
        value if not isinstance(value, str) or len(value) < 50 else value[:50] + ' ...' for value in record.values()
    ] for record in records ])

    if color: print(color, end='')
    print(table)
    if color: print(_RESET, end='')


def execute_query(session, query_key, queries=None):

    # raises execption if query_key doesn't exist
    query = queries[query_key] if queries else \
            _load_queries()[query_key]

    if not len(query): return

    print(f'{_GRAY}{query}{_RESET}')

    query_command, query_rest = query.split(maxsplit=1)

    if query_command.upper() == 'COPY':

        command_file = path.join(
            _TODOS_PATH, 
            todo['folder'], 
            f'{query_rest.strip()}.cql'
        )
        with open(command_file, 'r') as file:
            print(f'{_GRAY}{file.read()}{_RESET}')

        subprocess.Popen(
            f'cqlsh cassandra -f {command_file}', 
            shell=True
        ).wait()

    else:  

        result = session.execute(query)
        records = result.all()
        if (len(records)): _print_records(records)

    feedback_qry = _FB_QRY.get(query_key)
    if feedback_qry:
        result = session.execute(feedback_qry)
        records = result.all()
        if (len(records)): _print_records(records, _BLUE)


def execute_reset(session, command):

    for reset_query in _RESET_QRY[command]:
        print(f'{_GRAY}{reset_query}{_RESET}')
        try: 
            session.execute(reset_query)
        except Exception as err: 
            print(err)


def execute_all(session, command):

    execute_reset(session, command)

    queries = _load_queries()
    param = 1

    while True:
        query_key = f'{command}_{param}'
        if not queries.get(query_key): break
        _bold_print(f'{command} ({param})') 
        try:           
            execute_query(session, query_key, queries)
        except Exception as err:
            print(err)
        param += 1

    print()


def get_credentials(folder):
   
    secure_connect_bundle=environ.get('SECURE_CONNECT_BUNDLE', None)
    application_token=environ.get('APPLICATION_TOKEN', None)

    if not (secure_connect_bundle and application_token):
       return None, None

    cloud_config = {
        'secure_connect_bundle': path.join(folder, secure_connect_bundle)
    }

    with open(path.join(folder, application_token)) as f:
        secrets = json.load(f)

    auth_provider = PlainTextAuthProvider(secrets["clientId"], secrets["secret"])

    return cloud_config, auth_provider
