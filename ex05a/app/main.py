
import traceback
try: import readline
except: pass 
from dotenv import load_dotenv # pyright: ignore
from os import environ
from os import path

from cassandra.cluster import Cluster  # pyright: ignore
from cassandra.query import dict_factory # pyright: ignore

from supp import helpers, config

def repl():
    
    try: 

        cloud_config, auth_provider = helpers.get_credentials(
           path.dirname(path.abspath(__file__))
        )

        if cloud_config:
            cluster = Cluster(
               cloud=cloud_config, 
               auth_provider=auth_provider
            )
        else:
            cassandra_host = environ.get('CASSANDRA_HOST')
            cluster =  Cluster([
                cassandra_host if cassandra_host else 'cassandra'
            ])

        session = cluster.connect()
        session.row_factory = dict_factory

        print(f'Using Cassandra at {cluster.get_control_connection_host()}')

    except Exception as err:
        print(err)
        return

    while True:

        try:
            user_input = input(config.todo['prompt'])

        except EOFError:
            if cluster: cluster.shutdown()
            print('')
            break        

        if not user_input.strip(): continue
        
        input_strings = user_input.lower().split()
        command = input_strings[0]

        try:

            if len(input_strings) == 1:

                if command in ('exit', 'quit'):
                    if cluster: cluster.shutdown()
                    break
                raise AssertionError    

            if len(input_strings) != 2: raise AssertionError 
            assert command in ['qa','qb','qc']                

            param = input_strings[1]

            if param == 'all': 
                helpers.execute_all(session, command)
                continue

            helpers.execute_query(session, f'{command}_{param}')
            continue

        except KeyError:
            print('Unkwown query:', f'{command}_{param}')

        except AssertionError:
            print('Usage:{ q{a|b|c} {<int>|all} | exit | quit }')

        except Exception as err:
            print(err)
            # traceback.print_exc()

if __name__ == '__main__':

    load_dotenv()
    config.set_config()
    repl()
