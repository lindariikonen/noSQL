
import traceback
from pymongo.errors import ConnectionFailure, OperationFailure # pyright: ignore

try:
    import readline
except:
    pass 

from supp.config import todo, set_config
from supp.helpers import connect_db, list_courses, delete_courses, print_result, run_query, run_all 

DATABASE = 'nosql_2024_ex1a'

def repl():
    
    db_client = None

    while True:

        try:
            user_input = input(todo['prompt'])

        except EOFError:
            if db_client: db_client.close()
            print('')
            break        

        if not user_input.strip(): continue
        input_strings = user_input.lower().split()
        command = input_strings[0]

        try:

            if len(input_strings) != 1: raise AssertionError

            if command in ('exit', 'quit'):
                if db_client: db_client.close()
                break

            if not db_client: 
                db_client = connect_db()
                db = db_client[DATABASE]

            if command == 'dbs':
                for name in db_client.list_database_names(): print(name)
                continue

            if command == 'reset':
                result = delete_courses(db)
                print_result(result)
                continue

            if command == 'list':
                result = list_courses(db) 
                print_result(result)
                continue

            if command == 'all':
                run_all(db) 
                continue

            if command.startswith('q'):
                run_query(db, command)
                continue

            raise AssertionError

        except AttributeError:
            print('Unkwown query:', command)

        except AssertionError:
            print('Usage: { q<int> | list | reset | all | dbs | exit | quit }')

        except (ConnectionFailure, OperationFailure, TypeError) as err:
            print(err)

        except Exception as err:
            print(err)
            traceback.print_exc()


if __name__ == '__main__':

    set_config()
    repl()
