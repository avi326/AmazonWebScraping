"""
program receives player name -> get images and terms about him -> add data to database.
"""
from mediawiki import mediawiki

from DatafromAPI.WikiAPI import WikiAPI
from Database.Database import Database


def get_player_data(player_name):
    """ get data from api about specific player and put in db.

    Args:
        the player name
    """

    db = Database()
    result = db.read_from_db(columns='player_id', table='Players',
                             where=('name', player_name))
    if not result:
        print("player don't found. ")
    else:
        player_id = result[0][0]  # take the player id

        # read from api
        source_name = "Wikipedia"
        wiki = WikiAPI()
        images, categories = wiki.get_player_data(player_name)

        # add api data to DB
        db.insert_data_from_api(player_id, source_name, images, categories)

    db.close_connect_db()


def get_data_for_all_players():
    """ takes all the players, get more data from api, and put in db. """

    db = Database()
    result = db.read_from_db(columns='player_id, name', table='Players')
    if not result:
        print("players don't found in db. ")
    else:
        for player in result:
            try:
                player_id = player[0]  # take the player id
                player_name = player[1]

                # read from api
                source_name = "Wikipedia"
                wiki = WikiAPI()
                images, categories = wiki.get_player_data(player_name)

                # add api data to DB
                db.insert_data_from_api(player_id, source_name, images, categories)

            except:
                print("there isn't data about the player {} in wikipedia. ".format(player_name))

    db.close_connect_db()
