"""
    this program does web scraping from a specific football club.
    all players data is scrapping.
"""

# import packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
from datetime import datetime
from Constants import *


class ClubScraper:
    def __init__(self, url, league_name, country_name):
        self.selenium_driver = get_data_from_url(url)
        self.labels_with_value_dict = {}
        self.league_name = league_name
        self.country_name = country_name
        # init list for saving details
        self.country_list = []
        self.league_list = []
        self.club_name_list = []
        self.jersey_numbers_list = []
        self.nationals_list = []
        self.names_list = []
        self.ages_list = []
        self.matches_played_list = []
        self.goals_list = []
        self.yellow_cards_list = []
        self.red_cards_list = []
        self.date_list = []

    def get_players_data(self):
        """
            get page soup object and take the data about each player
        """

        # get club name
        club_name = self.selenium_driver.find_elements_by_xpath("//*[@id='fscon']/div[1]/div[2]/div")[0].text.strip()
        print("{} club...".format(club_name), end=" ")
        try:
            # finds each player from the club page
            players_list = self.selenium_driver.find_element_by_class_name('base-table').find_elements(By.CLASS_NAME,
                                                                                                       'player')
            if len(players_list) == 0:
                raise ValueError()

            # iterate over the stats for each player
            for player in players_list:
                self.country_list.append(self.country_name)
                self.league_list.append(self.league_name)
                self.club_name_list.append(club_name)
                self.jersey_numbers_list.append(player.find_element_by_class_name('jersey-number').text)
                self.nationals_list.append(
                    player.find_element_by_class_name('player-name').find_element(By.TAG_NAME, 'span').get_attribute(
                        'title'))
                self.names_list.append(player.find_element_by_class_name('player-name').text)
                self.ages_list.append(player.find_element_by_class_name('player-age').text)
                self.matches_played_list.append(player.find_elements_by_tag_name('td')[3].text)
                self.goals_list.append(player.find_elements_by_tag_name('td')[4].text)
                self.yellow_cards_list.append(player.find_elements_by_tag_name('td')[5].text)
                self.red_cards_list.append(player.find_elements_by_tag_name('td')[6].text)

            self.labels_with_value_dict = self.put_data_in_nested_dict()
            print(" Done.")

        except ValueError:
            print("No Data for this club. ")

        return self.labels_with_value_dict

    def scrap_players_data(self, players_list, club_name):
        # iterate over the stats for each player
        for player in players_list:
            self.country_list.append(self.country_name)
            self.league_list.append(self.league_name)
            self.club_name_list.append(club_name)
            self.jersey_numbers_list.append(player.find_element_by_class_name('jersey-number').text)
            self.nationals_list.append(
                player.find_element_by_class_name('player-name').find_element(By.TAG_NAME, 'span').get_attribute(
                    'title'))
            self.names_list.append(player.find_element_by_class_name('player-name').text)
            self.ages_list.append(player.find_element_by_class_name('player-age').text)
            self.matches_played_list.append(player.find_elements_by_tag_name('td')[3].text)
            self.goals_list.append(player.find_elements_by_tag_name('td')[4].text)
            self.yellow_cards_list.append(player.find_elements_by_tag_name('td')[5].text)
            self.red_cards_list.append(player.find_elements_by_tag_name('td')[6].text)
            self.date_list.append(datetime.now().date())

    def put_data_in_nested_dict(self):
        labels_with_value_dict = {"Country": self.country_list,
                                  "League": self.league_list,
                                  "Club Name": self.club_name_list,
                                  "Jersey Number": self.jersey_numbers_list,
                                  "National": self.nationals_list,
                                  "Name": self.names_list,
                                  "Age": self.ages_list,
                                  "Matched Played": self.matches_played_list,
                                  "Goals": self.goals_list,
                                  "Yellow Cards": self.yellow_cards_list,
                                  "Red Card": self.red_cards_list,
                                  "Date": self.date_list
                                  }
        return labels_with_value_dict

    def output_to_csv(self):
        """
            get the players data and output to csv file
        """
        # create CSV file by pandas
        df = pd.DataFrame(self.labels_with_value_dict)
        if not df.empty:
            # if file does not exist write header
            csv_file_name = 'Players Stats.csv'
            if not os.path.isfile(csv_file_name):
                df.to_csv(csv_file_name)
            else:  # else it exists so append without writing the header
                df.to_csv(csv_file_name, mode='a', header=False)
        return


def get_data_from_url(url):
    """
    function loads url and return object that contain all html data.
    """
    options = Options()
    options.headless = True  # disable open website.
    selenium_driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)
    selenium_driver.get(url)

    return selenium_driver
