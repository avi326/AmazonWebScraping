"""
    this program does web scraping from a specific football club.

"""

# import packages
from bs4 import BeautifulSoup as soup  # HTML data structure
import requests
import pandas as pd
import os


class DataMiningFromClub:
    def __init__(self, url, league_name, country_name):
        self.page_soup = get_html_from_url(url)
        self.labels_with_value_dict = {}
        self.league_name = league_name
        self.country_name = country_name

    def get_players_data(self):
        """
            get page soup object and take the data about each player
        """

        # get club name
        self.club_name = self.page_soup.find("div", {"class": "team-name"}).text.strip()

        print("Scraping from {}, {}, {}...".format(self.club_name, self.league_name, self.country_name))

        try:
            # finds each player from the club page
            get_table_elm = self.page_soup.findAll("table", {"class": "base-table squad-table"})

            players_table = get_table_elm[0]
            players_list = players_table.tbody.findAll("tr", {"class": "player"})

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
                club_name_list.append(self.club_name)
                jersey_numbers_list.append(player.find("td", {"class": "jersey-number"}).text)
                nationals_list.append(player.find("td", {"class": "player-name"}).span.get("title"))
                names_list.append(player.find("td", {"class": "player-name"}).text)
                ages_list.append(player.find("td", {"class": "player-age"}).text)
                matches_played_list.append(player.findAll("td")[3].text)
                goals_list.append(player.findAll("td")[4].text)
                yellow_cards_list.append(player.findAll("td")[5].text)
                red_cards_list.append(player.findAll("td")[6].text)

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

        except IndexError as meg:  # selenium.common.exceptions.NoSuchElementException, IndexError:
            print("problem on get players stats. ")
            # print(meg)

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


def get_html_from_url(url):
    """
        get bs4 object that contain html data
    """
    # TODO timeout int list

    # headers setup
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

    # URl to web scrap from.
    # scrap from scoreboard.com (football statistics website)
    page_url = url

    # opens the connection and downloads html page from url
    u_client = requests.get(page_url, headers=headers, timeout=5)

    # parses html into a soup data structure to traverse html
    page_soup = soup(u_client.text, "html.parser")
    u_client.close()

    return page_soup
