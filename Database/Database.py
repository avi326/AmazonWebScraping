"""
Database class:
    handle the database.
    first, can take data after the web scraping and create database with relevant tables.

Author: Avi Barazani & Tal Toledano
"""

# TODO: handle duplicate insert values.

import mysql.connector
import pandas as pd
from Constants import *


class Database:
    def __init__(self):
        """ connect to database. if don't exists - create database and tables. """

        self.con, self.cur = setup_mysql_db()
        self.df = read_csv(CSV_File)

    def close_connect_db(self):
        """ close connection to Mysql database. """
        self.con.close()

    def insert_all_to_mysql(self):
        """from CSV file, insert all tables: Countries, Clubs, Leagues, Players to Mysql database."""

        self.insert_countries_table()
        self.insert_leagues_table()
        self.insert_clubs_table()
        self.insert_players_table()

    def insert_countries_table(self):
        """ from CSV file, insert Countries table to mysql """

        df = self.df
        for i, r in df.iterrows():
            sql = "INSERT IGNORE INTO Countries (Country_id,name) VALUES (%s, %s)"
            val = (None, r['Country'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_clubs_table(self):
        """ from CSV file, insert Clubs table to mysql """

        df = self.df
        for i, r in df.iterrows():
            sql = "INSERT IGNORE INTO Clubs (club_id, name, league_played) VALUES (%s, %s, %s)"
            val = (None, r['Club Name'], r['League'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_leagues_table(self):
        """ from CSV file, insert Leagues table to mysql """

        df = self.df
        for i, r in df.iterrows():
            sql = "INSERT IGNORE INTO Leagues (league_id, name, country) VALUES (%s, %s, %s)"
            val = (None, r['League'], r['Country'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_players_table(self):
        """ from CSV file, insert Players table to mysql """

        df = self.df
        for i, r in df.iterrows():
            sql = """INSERT IGNORE INTO Players
                    (player_id, name, club_played, nationality, jersey_Number, age,
                     matched_played, goals, yellow_cards, red_cards, date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (None, r['Name'], r['Club Name'], r['National'], r['Jersey Number'], r['Age'], \
                   r['Matched Played'], r['Goals'], r['Yellow Cards'], r['Red Card'], r['Date'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_data_from_api(self, player_id, source_name, images, categories):
        """ from api, insert data to mysql

        Args:
            1) player id from 'players' table from DB
            2) the api website
            3) image urls of the player
            4) some terms that connect to the player
        """

        # add data to Image table
        for img in images:
            sql = """INSERT IGNORE INTO Images
                    (image_id, player_id, source, image_url)
                    VALUES (%s, %s, %s, %s)"""
            val = (None, player_id, source_name, img)
            self.cur.execute(sql, val)

        # add data to Categories table
        for cat in categories:
            sql = """INSERT IGNORE INTO Categories
                    (cat_id, player_id, source, category)
                    VALUES (%s, %s, %s, %s)"""
            val = (None, player_id, source_name, cat)
            self.cur.execute(sql, val)
        self.con.commit()

    def read_from_db(self, columns, table, where=''):
        """ read and print from Mysql database by statement.
            params:       Columns(str),
                          Table(str),
                optional: Where(column(str),value(str)  """

        if where:
            self.cur.execute("SELECT {} FROM {} WHERE {}='{}'".format(columns, table, where[0], where[1]))
        else:
            self.cur.execute("SELECT {} FROM {} ".format(columns, table))

        result = self.cur.fetchall()

        return result


########### static functions ############

def read_csv(file):
    """ read csv file to DataFrame of pandas package. """

    df = pd.read_csv(file)
    df = df.fillna("empty")  # fillna beacause the python can't pass null to mysql db. #TODO better solution code.
    return df


def setup_mysql_db():
    """ connect to mysql server. and create database and tables if don't exists."""

    con = mysql.connector.connect(
        host='localhost', user=MYSQL_USERNAME, use_pure=True, auth_plugin='mysql_native_password')

    # create if don't exists:
    create_database(con)
    create_tables(con)

    return con, con.cursor()


def create_database(con):
    """ create database if don't exists. """
    cur = con.cursor()
    cur.execute(''' CREATE DATABASE IF NOT EXISTS Players_Stats''')
    cur.execute(''' USE Players_Stats ''')
    con.commit()


def create_tables(con):
    """ create tables if don't exists. """

    cur = con.cursor()

    create_Countries = '''
         CREATE TABLE IF NOT EXISTS `Countries` (
         `country_id` int PRIMARY KEY AUTO_INCREMENT,
        `name` varchar(255)
        );
    '''
    cur.execute(create_Countries)
    #############################
    create_Leagues = '''
            CREATE TABLE IF NOT EXISTS `Leagues` (
          `league_id` int PRIMARY KEY AUTO_INCREMENT,
          `name` varchar(255),
          `country` varchar(255)
        );
        '''
    cur.execute(create_Leagues)
    #############################
    create_Clubs = '''
        CREATE TABLE IF NOT EXISTS `Clubs` (
          `club_id` int PRIMARY KEY AUTO_INCREMENT,
          `name` varchar(255),
          `league_played` varchar(255)
        );

        '''
    cur.execute(create_Clubs)
    #############################
    create_Players = '''
      CREATE TABLE IF NOT EXISTS `Players` (
          `player_id` int PRIMARY KEY AUTO_INCREMENT,
          `name` varchar(255),
          `club_played` varchar(255),
          `nationality` varchar(255),
          `jersey_Number` int,
          `age` int,
          `matched_played` int,
          `goals` int,
          `yellow_cards` int,
          `red_cards` int,
          `date` int
        );

    '''
    cur.execute(create_Players)
    #############################
    create_Images = '''
            CREATE TABLE IF NOT EXISTS `Images` (
          `image_id` int PRIMARY KEY AUTO_INCREMENT,
          `player_id` int,
          `source` varchar(255),
          `image_url` varchar(255)
            );
    '''
    cur.execute(create_Images)
    #############################
    create_Categories = '''
            CREATE TABLE IF NOT EXISTS `Categories` (
              `cat_id` int PRIMARY KEY AUTO_INCREMENT,
              `player_id` int,
              `source` varchar(255),
              `category` varchar(255)
            );
    '''
    cur.execute(create_Categories)
    #############################
    keys = ''' 
    ALTER TABLE `Players` ADD FOREIGN KEY (`club_played`) REFERENCES `Clubs` (`name`);

    ALTER TABLE `Countries` ADD FOREIGN KEY (`name`) REFERENCES `Leagues` (`country`);

    ALTER TABLE `Clubs` ADD FOREIGN KEY (`league_played`) REFERENCES `Leagues` (`name`);

    ALTER TABLE `Countries` ADD FOREIGN KEY (`name`) REFERENCES `Players` (`nationality`);

    ALTER TABLE `Images` ADD FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`);

    ALTER TABLE `Categories` ADD FOREIGN KEY (`player_id`) REFERENCES `Players` (`player_id`);
     '''
    cur.execute(keys, multi=True)
    con.commit()


def main():
    db = Database()
    return


if __name__ == "__main__":
    main()
