"""
program receives user argument and print the info under query
"""

import sys
import argparse
from . import ScoreBoard_WS
import sqlite3
import os
import random
import tqdm

REQUIRED_NUM_OF_ARGS = 2 or 3
ARG_OPTION = 1
ARG_NAME = 2
ARG_FILE_NAME = -1
# print(PRINT)


def get_stats(query, *args):
    """
    function gets arg from user and returns relevant info
    """
    FILE = 'name of file'
    CLASS = 'name of class'
    args = 'name of country/club/player'

    func_dict = {'players': FILE.get_players_data(),
                 'clubs': FILE.CLASS.get_club_data(),
                 'countries': FILE.CLASS.get_country_data()}

    return func_dict[query].args


# Parse arguments
parser = argparse.ArgumentParser(description="Print Soccer (country|club|player) stats following CL args")

parser.add_argument("query", help="choose your query you like to check", choices={'countries', 'clubs', 'players'})
parser.add_argument("-name", help="Print Summary File for specific query", type=str, action="store_true", choices='FUNC.CALL.QUERRY')
arg = parser.parse_args()
# .py players messi
# create the top-level parser
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-name', action='store_true', help='specify a name for the query')
subparsers = parser.add_subparsers(help='write down the name of the player you would like ')

# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('bar', type=int, help='bar help')

# create the parser for the "b" command
parser_b = subparsers.add_parser('b', help='b help')
parser_b.add_argument('--baz', choices='XYZ', help='baz help')

# parse some argument lists
parser.parse_args(['a', '12'])

parser.parse_args(['--foo', 'b', '--baz', 'Z'])


if len(arg.NAMESPACE()) != REQUIRED_NUM_OF_ARGS:
    print("usage: ./FILE.py {query |-name}")
    sys.exit(1)

# checking inputs valid value
if arg.query not in ['countries', 'clubs', 'players']:
    exp = 'please provide a valid query to look into, as stats for country, club, player.'
    raise Exception(exp)

if arg.query:
    qs = ['clubs', 'countries']
    for q in qs:
        print(get_stats(q))

if arg.name:
    result = get_stats(arg.name, 'name')
    print(result)
    exp = "usage: ./FILE.py { [query] | -name } "
    raise Exception(exp)

option = sys.argv[ARG_OPTION]

try:
    filename = sys.argv[ARG_FILE_NAME]
except:
    print("Input file doesn't exist, please check and run again...")


else:
    print("unknown option: " + option)
    sys.exit(1)


