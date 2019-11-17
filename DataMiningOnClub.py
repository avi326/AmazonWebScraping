"""
    this program does web scraping from a specific football club.

"""

# import packages
from bs4 import BeautifulSoup as soup  # HTML data structure
import requests
import pandas as pd


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


def get_player_data(page_soup):
    """
        get page soup object and take the data about each player
    """

    # get club name
    club_name = page_soup.find("div", {"class": "team-name"}).text.strip()

    # finds each player from the club page
    players_table = page_soup.findAll("table", {"class": "base-table squad-table"})[0]
    players_list = players_table.tbody.findAll("tr", {"class": "player"})

    # init list for saving details
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
        club_name_list.append(club_name)
        jersey_numbers_list.append(player.find("td", {"class": "jersey-number"}).text)
        nationals_list.append(player.find("td", {"class": "player-name"}).span.get("title"))
        names_list.append(player.find("td", {"class": "player-name"}).text)
        ages_list.append(player.find("td", {"class": "player-age"}).text)
        matches_played_list.append(player.findAll("td")[3].text)
        goals_list.append(player.findAll("td")[4].text)
        yellow_cards_list.append(player.findAll("td")[5].text)
        red_cards_list.append(player.findAll("td")[6].text)

    labels_with_value_list = {"club name": club_name_list,
                             "Jersey Number": jersey_numbers_list,
                             "National": nationals_list,
                             "Name": names_list,
                             "Age": ages_list,
                             "Matched Played": matches_played_list,
                             "Goals": goals_list,
                             "Yellow Cards": yellow_cards_list,
                             "Red Card": red_cards_list,
                             }

    return labels_with_value_list


def output_to_csv(labels_with_value_list):
    """
        get the players data and output to csv file
    """
    # create CSV file by pandas
    df = pd.DataFrame(labels_with_value_list)
    df.to_csv("players stats.csv")

    return


def test():
    return


def main():
    url = "https://www.scoreboard.com/en/team/liverpool/lId4TMwf/squad/"
    page_soup = get_html_from_url(url)
    labels_with_value_list = get_player_data(page_soup)
    output_to_csv(labels_with_value_list)

    return


if __name__ == "__main__":
    test()
    main()
