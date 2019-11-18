import GetLeagueUrls
import DataMiningFromClub
from tqdm import tqdm


def test():
    # TODO some tests
    return


def main():
    urls = ['https://www.scoreboard.com/en/soccer/bermuda/Premier-League',
            'https://www.scoreboard.com/en/soccer/canada/Canadian-Premier-League',
            'https://www.scoreboard.com/en/soccer/costa-rica/Primera-Division',
            'https://www.scoreboard.com/en/soccer/dominican-republic/LDF',
            'https://www.scoreboard.com/en/soccer/el-salvador/Primera-Division',
            'https://www.scoreboard.com/en/soccer/guatemala/Liga-Nacional',
            'https://www.scoreboard.com/en/soccer/haiti/Championnat-National',
            'https://www.scoreboard.com/en/soccer/honduras/Liga-Nacional',
            'https://www.scoreboard.com/en/soccer/jamaica/Premier-League',
            'https://www.scoreboard.com/en/soccer/nicaragua/Liga-Primera',
            'https://www.scoreboard.com/en/soccer/panama/LPF']

    for url in tqdm(urls):
        league_to_scraping = GetLeagueUrls.GetLeagueUrls(url)
        premier_league_clubs = league_to_scraping.get_club_urls_list()
        league_name = league_to_scraping.get_league_name()
        country_name = league_to_scraping.get_country_name()

        for club in tqdm(premier_league_clubs):
            temp_club = DataMiningFromClub.DataMiningFromClub(club, league_name, country_name)
            temp_club.get_players_data()
            temp_club.output_to_csv()

    return


if __name__ == "__main__":
    test()
    main()
