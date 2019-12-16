"""
program receives player name -> get images and terms about him -> add data to database.
"""

from DatafromAPI.WikiAPI import WikiAPI
from Database.Database import Database
from Constants import *
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="add more data from API about a player")
    parser.add_argument("query", nargs='+', type=str, help="name '*' ")
    args = parser.parse_args()

    where_value = args.query[ARG_NAME]
    where_column = args.query[ARG_OPTION]

    # Parse arguments
    if len(args.query) != REQUIRED_NUM_OF_ARGS:
        print("usage: ./FILE.py {query name}")
        sys.exit(1)

    # checking inputs valid value
    if where_column not in ['name']:
        print("please provide a valid query: name '*' ")

    if not where_value:
        print(f'please provide a valid name for query to look into')

    # call function to print query
    db = Database()
    result = db.read_from_db(columns='player_id', table='Players',
                    where=(where_column, where_value))
    if not result:
        print("player don't found. ")
    else:
        result = result[0][0] # take the player id

    # read from api
    wiki = WikiAPI()
    images, categories = wiki.get_player_data(where_value)
    source_name = "Wikipedia"

    # add api data to DB
    db.insert_data_from_api(result, source_name, images, categories)
    db.close_connect_db()


if __name__ == '__main__':
    main()
