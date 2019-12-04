"""
    this program call all relevant classes to scrap main url and print stat to file
"""

from .Classes import LeagueScraper, ClubScraper, CountriesScraper
from tqdm import tqdm

def main():

    # extract all urls of each premier league from each state listed on the ScoreBoard.com.
    urls = CountriesScraper.SBScraper().extract_urls()

    # get club list for each state
    for url in tqdm(urls):
        league_to_scraping = LeagueScraper.GetLeagueUrls(url)
        premier_league_clubs = league_to_scraping.get_club_urls_list()
        league_name = league_to_scraping.get_league_name()
        country_name = league_to_scraping.get_country_name()

        # get data for each player in this club
        for club in premier_league_clubs:
            temp_club = ClubScraper.DataMiningFromClub(club, league_name, country_name)
            temp_club.get_players_data()
            temp_club.output_to_csv()

    return temp_club.get_players_data(), temp_club.output_to_csv()


if __name__ == "__main__":
    main()