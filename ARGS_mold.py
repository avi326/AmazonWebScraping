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





def ws_summary(query, name):
    """
    function gets arg from user and returns relevant info
    """
    func_dict = {'country': ScoreBoard_WS.main().temp_club.get_players_data()}
    #              'league': league,
    #              'team': team,
    #              'player': player}

    return func_dict[query].name


# Parse arguments

parser = argparse.ArgumentParser(description="Print Soccer (team|player) stats following CL args")

parser.add_argument("query", help="choose your query you like to check", choices={'country', 'league', 'team', 'player'})
parser.add_argument("-name", help="Print Summary File for arg", action="store_true")
args = parser.parse_args()


if args.name:
    qs = ['country']#, 'league', 'team', 'player']
    for q in qs:
        print(ws_summary(args, q))
else:
    try:
        result = ws_summary(args.query)
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
if option == "-all":
    print(...)

elif option == "-player":
    print(...)
elif option == "-team":
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
