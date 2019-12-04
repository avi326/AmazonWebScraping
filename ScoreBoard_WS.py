"""
    this program call all relevant classes to scrap main url and print stat to file
"""

from Classes import LeagueScraper, ClubScraper, CountriesScraper
from Database import Database
from tqdm import tqdm
import time


def main():
    # extract all urls of each premier league from each state listed on the ScoreBoard.com.
    print("Starting Scrapping leagues from each country... ")
    urls = CountriesScraper.SBScraper().extract_urls()
    print("Done! ")

    # get club list for each state
    for url in tqdm(urls):
        league_to_scraping = LeagueScraper.GetLeagueUrls(url)
        league_name = league_to_scraping.get_league_name()
        country_name = league_to_scraping.get_country_name()
        print("### Scrapping {} from {} ###".format(league_name, country_name))

        premier_league_clubs = league_to_scraping.get_club_urls_list()
        # get data for each player in this club
        for club in premier_league_clubs:
            temp_club = ClubScraper.DataMiningFromClub(club, league_name, country_name)
            temp_club.get_players_data()
            temp_club.output_to_csv()

        print("### Done! ###".format(league_name, country_name))

    # convert the csv file to tables in database
    print("Convert CSV to MySQL Database. ")
    db = Database.Database()
    # db.insert_values() #TODO insert to database by user command line (if did web scraping )
    db.read_from_db(columns='name', table='Players',
                    where=('name', 'Barboza Facundo'))  # TODO read by user command line.
    db.close_connect_db()
    print("Done. ")

    return


if __name__ == "__main__":
    main()
