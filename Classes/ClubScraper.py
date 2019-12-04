"""
    this program does web scraping from a specific football club, and get
    data for each player.
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


class DataMiningFromClub:
    def __init__(self, url, league_name, country_name):
        self.selenium_driver = get_data_from_url(url)
        self.labels_with_value_dict = {}
        self.league_name = league_name
        self.country_name = country_name

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

            # init list for saving details
            country_list = []
            league_list = []
            club_name_list = []
            jersey_numbers_list = []
            nationals_list = []
            names_list = []
            ages_list = []
            matches_played_list = []
            goals_list = []
            yellow_cards_list = []
            red_cards_list = []

            # iterate over the stats for each player
            for player in players_list:
                country_list.append(self.country_name)
                league_list.append(self.league_name)
                club_name_list.append(club_name)
                jersey_numbers_list.append(player.find_element_by_class_name('jersey-number').text)
                nationals_list.append(
                    player.find_element_by_class_name('player-name').find_element(By.TAG_NAME, 'span').get_attribute(
                        'title'))
                names_list.append(player.find_element_by_class_name('player-name').text)
                ages_list.append(player.find_element_by_class_name('player-age').text)
                matches_played_list.append(player.find_elements_by_tag_name('td')[3].text)
                goals_list.append(player.find_elements_by_tag_name('td')[4].text)
                yellow_cards_list.append(player.find_elements_by_tag_name('td')[5].text)
                red_cards_list.append(player.find_elements_by_tag_name('td')[6].text)

            self.labels_with_value_dict = {"Country": country_list,
                                           "League": league_list,
                                           "Club Name": club_name_list,
                                           "Jersey Number": jersey_numbers_list,
                                           "National": nationals_list,
                                           "Name": names_list,
                                           "Age": ages_list,
                                           "Matched Played": matches_played_list,
                                           "Goals": goals_list,
                                           "Yellow Cards": yellow_cards_list,
                                           "Red Card": red_cards_list,
                                           }
            print(" Done.")
        except ValueError:
            print("No Data for this club. ")

        return self.labels_with_value_dict

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
    options.headless = True
    selenium_driver = webdriver.Chrome(chrome_options=options)
    selenium_driver.get(url)

    return selenium_driver
