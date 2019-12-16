"""
program receives player name -> get images and terms about him -> add data to database.
"""

from DatafromAPI.WikiAPI import WikiAPI
from Database.Database import Database


def get_data_from_api(player_name):
    """ get data from api and insert data to mysql

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
