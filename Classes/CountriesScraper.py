"""
this program extract urls for each country and premier leagues.
"""

# import configWS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

URL = 'https://www.scoreboard.com/en/soccer/'
COUNTRY_IDX = 1
URL_IDX = 0

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")


class SBScraper(object):
    """
    class will get from CL (or elsewhere) name of country team or league and will get the stats of game or player '''
    """

    def __init__(self, country='', league='', team=''):
        self.country = country
        self.league = league
        self.team = team
        self.url = URL
        self.driver = webdriver.Chrome(executable_path='/Applications/chromedriver 2', options=chrome_options)
        self.delay = 5
        self.sub_url = f"{self.url}{country}/{league}/{team}"
        self.driver.get(self.url)
        self.source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.source, 'html.parser')

    def load_url(self):
        """
        function call extract_url to loads url list and wait certain amount of time to load bottom page stats.
        and debug url string that varies between countries.
        """

        links = self.extract_urls()[URL_IDX]
        for i in range(len(links)):
            try:
                self.driver.get(links[i])
                wait = WebDriverWait(self.driver, self.delay)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tournament-header")))
                print("Page is ready")

            except:
                links[i] = links[i][:37] + links[i][37:].split('/')[1]
                self.driver.get(links[i])
                wait = WebDriverWait(self.driver, self.delay)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tournament-header")))
                print("Page is ready")

    def extract_urls(self):
        """
        loop through html and extract countries and links for primer league
        :param url, country (list)
        :returns list of urls for further scrapping
        """

        country_list = []
        el = self.driver.find_elements_by_xpath('//a[contains(@href,"/en/soccer/")]')
        for i in el:
            country_list.append('-'.join(i.text.split()).lower())
        country_list = country_list[7:-8]

        lmenu = []
        for i in self.soup.find_all('ul', class_='menu-left')[2:]:
            for j in i.find_all('li'):
                lmenu.append(j['id'])

        url_list = []
        links = []
        for l in lmenu:
            self.driver.find_element_by_xpath(f"//li[@id='{l}']").click()
            time.sleep(5)
            links.append(
                self.driver.find_element_by_class_name('last').find_element_by_xpath(f'//*[@id="{l}"]/ul/li/a'))
        for link in links:
            url_list.append(link.get_attribute('href'))

        # leagues_america = ['Premier-League', 'Canadian-Premier-League', 'Primera-Division', 'LDF', 'Primera-Division',
        #                    'Liga-Nacional', 'Championnat-National', 'liga-nacional', 'Premier-League', 'Liga-MX',
        #                    'Liga-Primera', 'LPF', 'Pro-League', 'MLS', 'Superliga', 'Division-di-Honor',
        #                    'Division-Profesional', 'Serie-A', 'Primera-Division', 'Liga-Aguila', 'Liga-Pro',
        #                    'Primera-Division', 'Liga-1', 'Primera-Division', 'Primera-Division']
        # for i in range(len(links)):
        #     url_list.append(self.url + country_list[i] + '/' + leagues_america[i].lower())

        return url_list[:-8], country_list

    def drive_exit(self):
        """
        closing Chrome driver
        """
        self.driver.close()


def main():
    scraper = SBScraper()
    urls = scraper.extract_urls()[URL_IDX]
    # countries = scraper.extract_urls()[COUNTRY_IDX]

    print(urls)


if __name__ == '__main__':
    main()
