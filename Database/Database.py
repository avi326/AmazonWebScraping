"""
Database class:
    handle the database.
    first, can take data after the web scraping and create database with relevant tables.

Author: Avi Barazani & Tal Toledano
"""

# TODO: handle duplicate insert values.

import mysql.connector
import pandas as pd
import os

CSV_File = 'Players Stats.csv'
MYSQL_USERNAME = 'root'

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
                     matched_played, goals, yellow_cards, red_cards) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (None, r['Name'], r['Club Name'], r['National'], r['Jersey Number'], r['Age'], \
                   r['Matched Played'], r['Goals'], r['Yellow Cards'], r['Red Card'])
            self.cur.execute(sql, val)
        self.con.commit()

    def read_from_db(self, columns, table, where=''):
        """ read from Mysql database by statement.
            params:       Columns(str),
                          Table(str),
                optional: Where(column(str),value(str)  """

        if where:
            self.cur.execute("SELECT {} FROM {} WHERE {}='{}'".format(columns, table, where[0], where[1]))
        else:
            self.cur.execute("SELECT {} FROM {} ".format(columns, table))

        result = self.cur.fetchall()
        for x in result:
            print(x)


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
    cur = con.cursor()

    # create if don't exists:
    create_database(cur, con)
    create_tables(cur, con)
    return con, cur


def create_database(cur, con):
    """ create database if don't exists. """

    cur.execute(''' CREATE DATABASE IF NOT EXISTS Players_Stats''')
    cur.execute(''' USE Players_Stats ''')
    con.commit()


def create_tables(cur, con):
    """ create tables if don't exists. """

    sql = ''' 
     CREATE TABLE `Countries` (
      `country_id` int PRIMARY KEY AUTO_INCREMENT,
      `name` varchar(255)
    );

    CREATE TABLE `Leagues` (
      `league_id` int PRIMARY KEY AUTO_INCREMENT,
      `name` varchar(255),
      `country` varchar(255)
    );

    CREATE TABLE `Clubs` (
      `club_id` int PRIMARY KEY AUTO_INCREMENT,
      `name` varchar(255),
      `league_played` varchar(255)
    );

    CREATE TABLE `Players` (
      `player_id` int PRIMARY KEY AUTO_INCREMENT,
      `name` varchar(255),
      `club_played` varchar(255),
      `nationality` varchar(255),
      `jersey_Number` int,
      `age` int,
      `matched_played` int,
      `goals` int,
      `yellow_cards` int,
      `red_cards` int
    );

    ALTER TABLE `Players` ADD FOREIGN KEY (`club_played`) REFERENCES `Clubs` (`name`);

    ALTER TABLE `Countries` ADD FOREIGN KEY (`name`) REFERENCES `Leagues` (`country`);

    ALTER TABLE `Clubs` ADD FOREIGN KEY (`league_played`) REFERENCES `Leagues` (`name`);

    ALTER TABLE `Countries` ADD FOREIGN KEY (`name`) REFERENCES `Players` (`nationality`);
     '''
    cur.execute(sql, multi=True)
    con.commit()


def main():
    return


if __name__ == "__main__":
    main()
