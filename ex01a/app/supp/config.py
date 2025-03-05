
from argparse import ArgumentParser

ASSIGNMENT_ID = 'ex01a'

todo = {}


def _get_arguments():

    parser = ArgumentParser(
        description=ASSIGNMENT_ID
    )
    parser.add_argument(
        '-r', '--review', choices=['0', '1', '2'], default='0',
        help='whose code is being run, default: 0 (your code)'
    ) 
    return vars(parser.parse_args())


def _get_todo_folder(args):
    
    return 'your_code' if not int(args.get('review')) else f'review_{args["review"]}'     


def set_config():

    args = _get_arguments()

    if args['review'] == '1':
         from todos.review_1 import queries

    elif args['review'] == '2':
         from todos.review_2 import queries

    else:
         from todos.your_code import queries

    todo['queries'] = queries  
    todo['folder'] = _get_todo_folder(args)
    todo['prompt'] = f'{ASSIGNMENT_ID} [{todo["folder"]}] > '
