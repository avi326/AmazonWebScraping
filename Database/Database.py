import mysql.connector
import pandas as pd

CSV_File = 'Players Stats example.csv'
MYSQL_USERNAME = 'root'

class Database:
    def __init__(self):
        self.con, self.cur = connect_mysql()
        self.df = read_csv(CSV_File)

    def create_database(self):
        self.cur.execute(''' CREATE DATABASE IF NOT EXISTS Players_Stats''')
        self.cur.execute(''' USE Players_Stats ''')

    def create_tables(self):
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

        self.cur.execute(sql, multi=True)
        self.con.commit()

    def insert_values(self):
        self.insert_countries_table()
        self.insert_leagues_table()
        self.insert_clubs_table()
        self.insert_players_table()

    def insert_countries_table(self):
        df = self.df
        for i, r in df.iterrows():
            sql = "INSERT IGNORE INTO Countries (Country_id,name) VALUES (%s, %s)"
            val = (None, r['Country'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_clubs_table(self):
        df = self.df
        for i, r in df.iterrows():
            sql = "INSERT IGNORE INTO Clubs (club_id, name, league_played) VALUES (%s, %s, %s)"
            val = (None, r['Club Name'], r['League'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_leagues_table(self):
        df = self.df
        for i, r in df.iterrows():
            sql = "INSERT IGNORE INTO Leagues (league_id, name, country) VALUES (%s, %s, %s)"
            val = (None, r['League'], r['Country'])
            self.cur.execute(sql, val)
        self.con.commit()

    def insert_players_table(self):
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


def read_csv(file):
    df = pd.read_csv(file)
    df = df.fillna("empty")
    return df


def connect_mysql():
    con = mysql.connector.connect(
        host='localhost', user=MYSQL_USERNAME, use_pure=True, auth_plugin='mysql_native_password')
    cur = con.cursor()
    return con, cur


def main():
    db = Database()
    db.create_database()
    db.create_tables()
    db.insert_values()
    db.con.close()


if __name__ == "__main__":
    main()
