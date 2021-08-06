import bs4
import pandas as pd
import requests


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


    def scrape_athlete_biography(self, soup):
        """
            Scrapes the athlete's biography.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict

        """
        biography = soup.find(class_='c-bio__info-details')
        compiled_stats = dict()

        for child in biography.children:
            if isinstance(child, bs4.element.Tag):
                bio_fields = child.findAll(class_='c-bio__field')
                for field in bio_fields:
                    label = field.find(class_='c-bio__label').get_text().lower().replace(" ", "_")
                    entry = field.find(class_='c-bio__text').get_text().replace("\n", "")
                    compiled_stats[label] = entry

        return compiled_stats


    def scrape_athlete_nickname(self, soup):
        """
            Scrapes the athlete's nickname.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: str of the athlete's nickname

        """
        try:
            nickname = soup.find(class_='field field-name-nickname').get_text()
            nickname = nickname.replace("\"", "")
            return nickname
        except:
            return ""


    def scrape_athlete_record(self, soup):
        """
            Scrapes the athlete's record.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: str of the athlete's record
        
        """
        try:
            record = soup.find(class_='c-hero__headline-suffix tz-change-inner').get_text()
            record = record.strip().split("\n")
            record = record[-1].strip()
            return record
        except:
            return ""


    def scrape_striking_accuracy(self, soup):
        """
            Scrapes the athlete's striking accuracy.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict
        
        """
        try:
            striking_accuracy_html = soup.find(class_='l-overlap-group__item--odd')
            significant_strike_accuracy = striking_accuracy_html.find(class_='e-chart-circle__percent').get_text()
            significant_strikes = striking_accuracy_html.find_all(class_='c-overlap__stats-value')
            significant_strikes_landed = significant_strikes[0].get_text()
            significant_strikes_attempted = significant_strikes[1].get_text()

            compiled_statistics = dict()
            compiled_statistics['significant_strikes_landed'] = significant_strikes_landed
            compiled_statistics['significant_strikes_attempted'] = significant_strikes_attempted
            compiled_statistics['significant_strike_accuracy'] = significant_strike_accuracy

            return compiled_statistics
        
        except:
            return dict()


    def scrape_grappling_accuracy(self, soup):
        """
            Scrapes the athlete's grappling accuracy.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict
        
        """
        try:
            grappling_accuracy_html = soup.find(class_='l-overlap-group__item--even')
            takedowns_accuracy = grappling_accuracy_html.find(class_='e-chart-circle__percent').get_text()
            takedowns = grappling_accuracy_html.find_all(class_='c-overlap__stats-value')
            takedowns_landed = takedowns[0].get_text()
            takedowns_attempted = takedowns[1].get_text()

            compiled_statistics = dict()
            compiled_statistics['takedowns_landed'] = takedowns_landed
            compiled_statistics['takedowns_attempted'] = takedowns_attempted
            compiled_statistics['takedown_accuracy'] = takedowns_accuracy

            return compiled_statistics
        
        except:
            return dict()


    def scrape_fight_metrics(self, soup):
        """
            Scrapes the athlete's grappling accuracy.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict
        
        """
        try:
            fight_metric_html = soup.find(class_='l-container__content--narrow stats-records__outer-container')
            compiled_statistcs = dict()

            # Get all the rows of metrics that have 2 columns
            metric_rows = fight_metric_html.find_all(class_='c-stats-group-2col')
            # Iterate through each row
            for metric_row in metric_rows:
                if isinstance(metric_row, bs4.element.Tag):
                    # Get each section in the row
                    metric_sections = metric_row.find_all(class_='c-stat-compare')
                    # Iterate through each section in the row
                    for metric_section in metric_sections:
                        if isinstance(metric_section, bs4.element.Tag):
                            # Get the left and right metric the section
                            metric_left_entry = metric_section.find(class_='c-stat-compare__group-1')
                            metric_right_entry = metric_section.find(class_='c-stat-compare__group-2')

                            for metric_entry in [metric_left_entry, metric_right_entry]:
                                # Extract the relevant information and clean the data
                                label = metric_entry.find(class_='c-stat-compare__label').get_text()
                                label = label.lower().replace('sig. str.', 'significant strikes').replace('avg', 'average').replace(' ', '_')

                                label_suffix = metric_entry.find(class_='c-stat-compare__label-suffix')
                                if label_suffix is not None:
                                    label_suffix = label_suffix.get_text()
                                    label_suffix = label_suffix.lower().replace(' ', '_')
                                    label = label + '_' + label_suffix

                                stat = metric_entry.find(class_='c-stat-compare__number').get_text().replace('\n', '').replace(' ', '')

                                # Insert label and stat into our dictionary
                                compiled_statistcs[label] = stat

            # Get the last row of metrics that has 3 columns
            metric_row = fight_metric_html.find(class_='c-stats-group-3col')

            return compiled_statistcs


        except Exception as e:
            print(e)
            return dict()


    def scrape_athelete_stats(self, athlete_name):
        """
            Driver function to scrape the athlete's stats from
            the UFC website.

            :param athlete_name: The name of the athlete.
            :type athlete_name: str
            :returns: dict of the athlete's stats
        
        """
        athlete_statistics = dict()
        athlete_statistics['name'] = athlete_name

        # Get the athlete's name in the format required
        athlete_name = athlete_name.lower().replace(" ", "-")

        # Get the html of the athlete's page on the UFC website
        url = self.BASE_URL + athlete_name
        page = requests.get(url)
        html_content = page.text
        soup = bs4.BeautifulSoup(html_content, 'html.parser')

        # Get the data from the html
        # athlete_statistics['nickname'] = self.scrape_athlete_nickname(soup)
        # athlete_statistics['record'] = self.scrape_athlete_record(soup)
        # athlete_statistics.update(self.scrape_athlete_biography(soup))
        # athlete_statistics.update(self.scrape_striking_accuracy(soup))
        # athlete_statistics.update(self.scrape_grappling_accuracy(soup))
        print(self.scrape_fight_metrics(soup))

        return athlete_statistics 


def main():
    ufc_scraper = UFCWebsiteScraper()
    compiled_stats = []
    athletes= ["Khabib Nurmagomedov",] #"Conor McGregor", 
    #             "Jon Jones", "Kamaru Usman", "Francis Ngannou",
    #             "Georges St-Pierre", "Anderson Silva"]

    for athlete in athletes:
        print(athlete)
        compiled_stats.append(ufc_scraper.scrape_athelete_stats(athlete))

    ufc_scraper.export_to_excel(compiled_stats)


if __name__ == "__main__":
    main()