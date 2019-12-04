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

REQUIRED_NUM_OF_ARGS = 2 or 3
ARG_OPTION = 0
ARG_NAME = 1
# ARG_FILE_NAME = -1
# print(PRINT)


def get_stats(option, name):
    """
    function gets arg from user and returns relevant info
    """
    # option = queries[ARG_OPTION]
    # name = queries[ARG_NAME]

    FILE = 'name of file'
    CLASS = 'name of class'
    args = 'name of country/club/player'

    func_dict = {'players': 1,#FILE.CLASS.get_players_data(),
                 'clubs': 1,#FILE.CLASS.get_club_data(),
                 'countries': name}#.FILE.CLASS.get_country_data()}

    return func_dict[option]


def checker():
    return lambda x: str(x)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Print Soccer (country|club|player) stats following CL args")

    parser.add_argument("query", nargs='+', help="Choose your query you like to check", choices={'countries', 'clubs', 'players'})
    parser.add_argument("name", help="Choose specific name for your summary stats you like to check",
                        action="store_true")
    args = parser.parse_args()

    if len(sys.argv) != REQUIRED_NUM_OF_ARGS:
        print("usage: ./FILE.py {query name}")
        sys.exit(1)
    print(args.query)
    # checking inputs valid value
    if ''.join(args.query) not in ['countries', 'clubs', 'players']:
        err = 'please provide a valid query to look into, as stats for [countries|clubs|players].'
        raise Exception(err)

    if not args.name:
        err = f'please provide a valid name from {args.query} to look into'
        raise Exception(err)

    # call function to print query
    if args.query:
        try:
            print(get_stats(args.query, args.name))
        except:
            err = "usage: ./FILE.py { [query] | -name } "
            raise Exception(err)
    # if args.name:
    #     result = get_stats(args.name)
    #     print(result)


if __name__ == '__main__':
    main()
