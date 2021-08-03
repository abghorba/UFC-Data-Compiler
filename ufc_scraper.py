import requests
from bs4 import BeautifulSoup

class UFCWebsiteScraper():
    def __init__(self):
        self.BASE_URL = "https://www.ufc.com/athlete/"

    def scrape_athlete_nickname(self, soup):
        nickname = soup.find(class_='field field-name-nickname').get_text()
        return nickname

    def scrape_athlete_record(self, soup):
        record = soup.find(class_='c-hero__headline-suffix tz-change-inner').get_text()
        record = record.strip().split("\n")
        record = record[-1].strip()
        return record

    def scrape_athelete_stats(self, athlete_name):
        url = self.BASE_URL + athlete_name
        page = requests.get(url)
        html_content = page.text
        soup = BeautifulSoup(html_content, 'html.parser')
        print(self.scrape_athlete_nickname(soup))
        print(self.scrape_athlete_record(soup))


def main():
    ufc_scraper = UFCWebsiteScraper()
    athlete = "khabib-nurmagomedov"
    ufc_scraper.scrape_athelete_stats(athlete)


if __name__ == "__main__":
    main()