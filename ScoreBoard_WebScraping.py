"""
    this program call all relevant classes to scrap main url and print stat to file
"""

from Classes import LeagueScraper, ClubScraper, CountriesScraper
from Database import Database
from DatafromAPI import AddDataFromAPI
from tqdm import tqdm

def main():
    # extract all urls of each premier league from each state listed on the ScoreBoard.com.
    print("Starting Scrapping leagues from each country... ")
    urls = CountriesScraper.CountryScraper().extract_urls()
    print("Done! ")

    # get club list for each state
    for url in tqdm(urls):
        try:
            league_to_scraping = LeagueScraper.LeagueScraper(url)
            league_name = league_to_scraping.get_league_name()
            country_name = league_to_scraping.get_country_name()
            print("### Scrapping {} from {} ###".format(league_name, country_name))

            premier_league_clubs = league_to_scraping.get_club_urls_list()
        except Exception as err:
            print("problem to scarp leage... :( \n", err)

        # get data for each player in this club
        for club in premier_league_clubs:
            try:
                temp_club = ClubScraper.ClubScraper(club, league_name, country_name)
                temp_club.get_players_data()
                temp_club.output_to_csv()
            except Exception as err:
                print("problem to scarp club... :( \n", err)


        print("### Done! ###".format(league_name, country_name))

    # convert the csv file to tables in database
    print("Convert CSV to MySQL Database. ")
    db = Database.Database()
    db.insert_all_to_mysql()
    db.close_connect_db()
    print("Done. ")

    # add more data to db from api
    AddDataFromAPI.get_data_for_all_players()

    return


if __name__ == "__main__":
    main()
