
import traceback
from pymongo.errors import ConnectionFailure, OperationFailure # pyright: ignore

try:
    import readline
except:
    pass 

from supp.config import todo, set_config
from supp.helpers import SomeError, print_result 
from supp import helpers

DATABASE = 'nosql_2024_ex01b'

def repl():
    
    db_client = None
    db = None

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


            if len(input_strings) == 2:

                if command == 'connect':

                    if db_client: db_client.close()
                    host = input_strings[1]
                    db_client = helpers.connect(host)
                    db = db_client[DATABASE]

                    continue

            if len(input_strings) != 1: raise AssertionError

            # --

            if command in ('exit', 'quit'):
                if db_client: db_client.close()
                break

            if db == None: raise SomeError('Not connected')

            if command == 'reset':                
                print_result(helpers.delete_categories(db))
                print_result(helpers.delete_courses(db))
                print_result(helpers.insert_courses(db))
                continue

            if command == 'list':
                result = helpers.list_courses(db) 
                print_result(result)
                continue

            if command == 'cats':
                print_result(helpers.list_categories(db))
                continue

            # --

            if command == 'init':
                result = todo['queries'].rs_init(db_client)
                print_result(result)
                continue

            if command == 'status':
                result = todo['queries'].rs_status(db_client)
                print_result(result)
                continue

            if command == 'stepdown':
                result = todo['queries'].rs_stepdown(db_client)
                print_result(result)
                continue

            # --

            if command == 'tx':
                with db_client.start_session() as session:
                    with session.start_transaction():
                        print_result(todo['queries'].tx_q1(db, session))
                        print_result(todo['queries'].tx_q2(db, session))
                continue

            if command == 'txfail':
                with db_client.start_session() as session:
                    with session.start_transaction():
                        print_result(todo['queries'].tx_q1(db, session))
                        raise SomeError('Failure in transaction')
                        print(todo['queries'].tx_q2(db, session))
                continue

            # --
                
            if command.startswith('q'):
                helpers.run_query(db, command)
                continue

            raise AssertionError

        except AttributeError:
            print('Unkwown query:', command)

        except AssertionError:
            print('Usage: {{reset|list|cats} | {qa|qi}{1|2|3|4} | {init|status|stepdown} | tx[fail] | {exit|quit}}')

        except (ConnectionFailure, OperationFailure, TypeError, SomeError) as err:
            print(err)

        except Exception as err:
            print(err)
            traceback.print_exc()

if __name__ == '__main__':

    set_config()
    repl()
