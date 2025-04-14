
import yaml # pyright: ignore
from prettytable import PrettyTable # pyright: ignore
from os import path
from supp.config import todo

from os import environ
import json
from cassandra.auth import PlainTextAuthProvider #pyright: ignore


_SELECT_QUERY_1 = 'SELECT * FROM videos'
_SELECT_QUERY_2 = 'SELECT * FROM videos_by_tag'

_FB_QRY = {
    'qa_4': _SELECT_QUERY_1,
    'qa_5': _SELECT_QUERY_1,
    'qa_6': _SELECT_QUERY_1,
    'qa_7': _SELECT_QUERY_1,
    
    'qb_5': _SELECT_QUERY_2,
    'qc_4': _SELECT_QUERY_2,
}

_TODOS_PATH = path.join(
    path.dirname(path.abspath(__file__)), '..', 'todos'
)

_BLUE = '\033[94m'
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
    table.add_rows ([record.values() for record in records ])
    if color: print(color, end='')
    print(table)
    if color: print(_RESET, end='')


def execute_query(session, query_key, queries=None):

    # raises execption if query_key doesn't exist
    query = queries[query_key] if queries else \
            _load_queries()[query_key]

    print(query)

    result = session.execute(query)
    records = result.all()
    if (len(records)): _print_records(records)

    feedback_qry = _FB_QRY.get(query_key)
    if feedback_qry:
        result = session.execute(feedback_qry)
        records = result.all()
        if (len(records)): _print_records(records, _BLUE)


def execute_all(session, command):

    queries = _load_queries()
    param = 0

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
