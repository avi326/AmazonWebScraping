"""
program receives user argument and print the info under query
"""
# import new.configWS
import sys
import argparse
# from . import ScoreBoard_WS
import os
import random
import tqdm
import pandas as pd

REQUIRED_NUM_OF_ARGS = 3
ARG_OPTION = 0
ARG_NAME = 1
# ARG_FILE_NAME = -1
# print(PRINT)
path = '/Users/tal/Dropbox/ITC/Git/WS_Proj/ScoreBoardWebScraping/Database/stats.csv'

DATA = pd.read_csv(path)


def main():
    parser = argparse.ArgumentParser(description="Print Soccer (country|club|player) stats following CL args")
    parser.add_argument("query", nargs='+', type=str, help="Choose your query you like to check")
    args = parser.parse_args()

    NAME = args.query[ARG_NAME]
    QUERY = args.query[ARG_OPTION]

    # Parse arguments
    if len(sys.argv) != REQUIRED_NUM_OF_ARGS:
        print("usage: ./FILE.py {query name}")
        sys.exit(1)

    # checking inputs valid value
    if QUERY not in ['Country', 'Club Name', 'Name']:
        print('please provide a valid query to look into, as stats for [countries|clubs|players].')

    if not NAME:
        print(f'please provide a valid name for query to look into')

    # call function to print query
    print(f'Stats for the {QUERY}-{NAME}/n{DATA[DATA[QUERY].str.contains(NAME.title())]}\n')


if __name__ == '__main__':
    main()

# in need to write to DB
"""for kind, options in DATA.items():
        if kind == 'Country':
            parser.add_argument('-c', '--country', nargs='+', help=f'Choose name of country.\
                             syntax: "name surname". options: {DATA[DATA["Country"].str.contains(options)]}')
        elif kind == 'Club Name':
            parser.add_argument('-l', '--leagues', nargs='+', help=f'Choose name of leagues.\
                             syntax: "name". options: {DATA[DATA["Club Name"].str.contains(options)]}')
        elif kind == 'Name':
            parser.add_argument('-p', '--players', nargs='+', help=f'Choose name of players.\
                     syntax: "name surname". options: {DATA[DATA["Name"].str.contains(options)]}')"""

# parser.add_argument('-c', '--mysqlcreds', nargs='+', help='username and password for mySQL server: username password')
# parser.add_argument('-i', '--information', nargs='+', help=GV.information_to_show_help)
