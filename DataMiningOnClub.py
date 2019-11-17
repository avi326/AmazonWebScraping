from bs4 import BeautifulSoup as soup  # HTML data structure
import requests
import pandas as pd

# headers setup
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'referrer': 'https://google.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache',
}

# TODO timeout int list

# URl to web scrap from.
# scrap from scoreboard.com (football statistics website)
page_url = "https://www.scoreboard.com/en/team/liverpool/lId4TMwf/squad/"

# opens the connection and downloads html page from url
uClient = requests.get(page_url, headers=headers, timeout=5)

# parses html into a soup data structure to traverse html
page_soup = soup(uClient.text, "html.parser")
uClient.close()

# get club name
club_name = page_soup.find("div", {"class": "team-name"}).text.strip()

# finds each player from the club page
players_table = page_soup.findAll("table", {"class": "base-table squad-table"})[0]
players_list = players_table.tbody.findAll("tr", {"class": "player"})

# init list for saving details
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
    jersey_number = player.find("td", {"class": "jersey-number"}).text
    national = player.find("td", {"class": "player-name"}).span.get("title")
    name = player.find("td", {"class": "player-name"}).text
    age = player.find("td", {"class": "player-age"}).text
    matches_played = player.findAll("td")[3].text
    goals = player.findAll("td")[4].text
    yellow_cards = player.findAll("td")[5].text
    red_cards = player.findAll("td")[6].text

    jersey_numbers_list.append(jersey_number)
    nationals_list.append(national)
    names_list.append(name)
    ages_list.append(age)
    matches_played_list.append(matches_played)
    goals_list.append(goals)
    yellow_cards_list.append(yellow_cards)
    red_cards_list.append(red_cards)

# create CSV file by pandas
column_with_data_dict = {"Jersey Number": jersey_numbers_list,
                         "National": nationals_list,
                         "Name": names_list,
                         "Age": ages_list,
                         "Matched Played": matches_played_list,
                         "Goals": goals_list,
                         "Yellow Cards": yellow_cards_list,
                         "Red Card": red_cards_list,
                         }

df = pd.DataFrame(column_with_data_dict)
df.to_csv(club_name + " - players stats.csv")
