from typing import DefaultDict
import pandas as pd
import requests
from bs4 import BeautifulSoup


class UFCWebsiteScraper():
    def __init__(self):
        self.BASE_URL = "https://www.ufc.com/athlete/"

    def export_to_excel(self, athlete_statistics):
        """
            Exports the compiled data into an Excel file.

            :param athlete_statisitcs: Compiled statistics of athlete data.
            :type athlete_statisitcs: dict
            :returns: None

        """
        data = pd.DataFrame(athlete_statistics)
        data.to_excel('stats.xlsx', engine='xlsxwriter')


    def scrape_athlete_nickname(self, soup):
        """
            Scrapes the athlete's nickname.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: str of the athlete's nickname

        """
        nickname = soup.find(class_='field field-name-nickname').get_text()
        nickname = nickname.replace("\"", "")
        return nickname

    def scrape_athlete_record(self, soup):
        """
            Scrapes the athlete's record.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: str of the athlete's record
        
        """
        record = soup.find(class_='c-hero__headline-suffix tz-change-inner').get_text()
        record = record.strip().split("\n")
        record = record[-1].strip()
        return record

    def scrape_athelete_stats(self, athlete_name):
        """
            Driver function to scrape the athlete's stats from
            the UFC website.

            :param athlete_name: The name of the athlete.
            :type athlete_name: str
            :returns: DefaultDict(list) of the athlete's stats
        
        """
        athlete_statistics = DefaultDict(list)
        athlete_statistics['name'].append(athlete_name)

        # Get the athlete's name in the format required
        athlete_name = athlete_name.lower().replace(" ", "-")

        # Get the html of the athlete's page on the UFC website
        url = self.BASE_URL + athlete_name
        page = requests.get(url)
        html_content = page.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Get the data from the html
        athlete_statistics['nickname'].append(self.scrape_athlete_nickname(soup))
        athlete_statistics['record'].append(self.scrape_athlete_record(soup))

        return athlete_statistics 


def main():
    ufc_scraper = UFCWebsiteScraper()
    athlete = "Khabib Nurmagomedov"
    stats = ufc_scraper.scrape_athelete_stats(athlete)
    print(stats)
    ufc_scraper.export_to_csv(stats)


if __name__ == "__main__":
    main()