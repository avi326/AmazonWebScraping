"""
program receives user argument and print the info under query
for example:
    -name "Lionel Messi" -> print messi stats.
    -nationality "Israel" -> print all israeli players.
    -club_played "Real Madrid" -> print all Real Madrid players.
"""

import sys
import argparse
from Database import Database
from Constants import *


def main():
    parser = argparse.ArgumentParser(description="Print Soccer (country|club|player) stats following CL args")
    parser.add_argument("query", nargs='+', type=str, help="Choose your query you like to check")
    args = parser.parse_args()

    where_value = args.query[ARG_NAME]
    where_column = args.query[ARG_OPTION]

    # Parse arguments
    if len(args.query) != REQUIRED_NUM_OF_ARGS:
        print("usage: ./FILE.py {query name}")
        sys.exit(1)

    # checking inputs valid value
    if where_column not in ['nationality', 'club_played', 'name']:
        print('please provide a valid query to look into, as stats for [countries|clubs|players].')

    if not where_value:
        print(f'please provide a valid name for query to look into')

    # call function to print query
    db = Database.Database()
    result = db.read_from_db(columns='*', table='Players',
                    where=(where_column, where_value))  # TODO read by user command line.
    print(result)
    db.close_connect_db()


if __name__ == '__main__':
    main()
