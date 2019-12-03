"""
program receives user argument and print the info under query
"""
import configWS
import sys
import argparse
from . import ScoreBoard_WS
import sqlite3
import os
import random
import tqdm
REQUIRED_NUM_OF_ARGS = 3
ARG_OPTION = 1
ARG_FILE_NAME = 2


def ws_summary(query, *args):
    """
    function gets arg from user and returns relevant info
    """
    FILE = 'name of file'
    CLASS = 'name of class'
    args = 'name of country/club/player'

    func_dict = {'player': FILE.get_players_data(),
                 'club': FILE.CLASS.get_club_data(),
                 'country': FILE.CLASS.get_country_data()}

    return func_dict[query].args


# Parse arguments

parser = argparse.ArgumentParser(description="Print Soccer (team|player) stats following CL args")

parser.add_argument("query", help="choose your query you like to check", choices={'country', 'league', 'team', 'player'})
parser.add_argument("-name", help="Print Summary File for specific query", action="store_true")
# parser.add_argument("-name", help="Print Summary File for arg", action="store_true")
# parser.add_argument("-name", help="Print Summary File for arg", action="store_true")
# parser.add_argument("-name", help="Print Summary File for arg", action="store_true")
arg = parser.parse_args()


if arg.query:
    qs = ['player', 'league', 'team', 'country']
    for q in qs:
        print(ws_summary(q))

elif arg.team:
    try:
        result = ws_summary(arg.query)
        print(result)
    except:
        print("usage: ./FILE.py { [query] | -name } ")


if len(sys.argv) != REQUIRED_NUM_OF_ARGS:
    print("usage: ./FILE.py {-query |-name}")
    sys.exit(1)

option = sys.argv[ARG_OPTION]
try:
    filename = sys.argv[ARG_FILE_NAME]
except:
    print("Input file doesn't exist, please check and run again...")

if option == "-player":
    print(...)
elif option == "-club":
    print(...)
elif option == "-league":
    print(...)
elif option == "-country":
    print(...)

else:
    print("unknown option: " + option)
    sys.exit(1)



# DB = 'test.db'
#
# if os.path.exists(DB):
#     os.remove(DB)

# with sqlite3.connect(DB) as con:
#     cur = con.cursor()
#     cur.execute("""CREATE TABLE my_table (
#                         Jersey Number INT PRIMARY KEY
#                         National CHAR
#                         Name CHAR
#                         Age INT
#                         Matched Played INT
#                         Goals INT
#                         Yellow Cards INT
#                         Red Card INT
#                         )""")
#     for i in range(len(DB)):
#         cur.execute("""
#         INSERT INTO my_table
#         (Jersey Number, National, Name, Age, Matched Played, Goals, Yellow Cards, Red Card) VALUES
#         (?, ?, ?, ?, ?, ?, ?, ?)""", [i, random.randint(0, 10)])
#
#         if i % 1000 == 0:
#             con.commit()
#     con.commit()
#     cur.close()
