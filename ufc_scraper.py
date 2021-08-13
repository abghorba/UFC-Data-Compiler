import bs4
import pandas as pd
import requests
import time


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
        data.to_excel('ufc_fighter_stats.xlsx', engine='xlsxwriter')


    def scrape_ufc_rankings_to_txt_file(self):
        """
            Scrapes the UFC rankings website to write into a txt file
            the fighters that we will collect data on.

            :returns: None
        
        """
        # Get the html for the rankings website
        url = 'https://www.ufc.com/rankings'
        page = requests.get(url)
        html_content = page.text
        soup = bs4.BeautifulSoup(html_content, 'html.parser')

        # Open the file we will write to
        with open('ufc_rankings.txt', 'w') as file:

            # Look at each grouping of rankings
            groupings = soup.find_all(class_='view-grouping')
            # Iterate through each grouping
            for grouping in groupings:
                if isinstance(grouping, bs4.element.Tag):
                    division = grouping.find(class_='view-grouping-header').get_text()
                    # Exclude the pound-for-pound ranking and women's featherweight
                    if division not in {"Pound-for-Pound Top Rank", "Women's Featherweight"}:
                        # Get the division's champion's name and clean the text
                        champion = grouping.find(class_='info')
                        champion = champion.find(class_='views-row').get_text().strip()
                        # Write the champion into file
                        file.write(champion + "\n")

                        # Get the top 15 fighters in the current division
                        top_15 = grouping.find_all(class_='views-field views-field-title')
                        for fighter in top_15:
                            # Get the top 15 fighter's name and clean the text
                            contender = fighter.find(class_='views-row').get_text().strip()
                            # Write the contender into file
                            file.write(contender + "\n")


    def scrape_athlete_biography(self, soup):
        """
            Scrapes the athlete's biography.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict

        """
        # Initialize the dictionary
        compiled_stats = dict()

        try:
            biography = soup.find(class_='c-bio__info-details')

            if biography is None:
                raise AttributeError()

            # Iterate through each child element   
            for child in biography.children:
                if isinstance(child, bs4.element.Tag):
                    bio_fields = child.findAll(class_='c-bio__field')
                    # Clean and gather data in each entry
                    for field in bio_fields:
                        label = field.find(class_='c-bio__label').get_text().lower().replace(" ", "_")
                        entry = field.find(class_='c-bio__text').get_text().replace("\n", "")
                        compiled_stats[label] = entry

        except AttributeError:
            # There is no biography section.
            compiled_stats.update(
                {'status': '',
                    'hometown': '',
                    'age': '',
                    'height': '',
                    'weight': '',
                    'octagon_debut': '',
                    'reach': '',
                    'leg_reach': ''}
            )

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
        except AttributeError:
            # Athlete does not have a nickname
            nickname = ""

        return nickname


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
        except AttributeError:
            # Athlete does not have a record
            record = ""
        
        return record


    def scrape_athlete_ranking(self, soup):
        """
            Scrapes the athlete's ranking.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: str of the athlete's record
        
        """
        try:
            ranking = soup.find(class_='c-hero__headline-suffix tz-change-inner').get_text()
            ranking = ranking.strip().split("\n")
            cleaned_ranking = []
            for line in ranking:
                cleaned_ranking.append(line.strip())
            ranking = ' '.join(cleaned_ranking)
            ranking = ranking.split('•')[0].strip()
        except AttributeError:
            # Athlete does not have a ranking
            ranking = ""

        return ranking


    def scrape_striking_accuracy(self, soup):
        """
            Scrapes the athlete's striking accuracy.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict
        
        """
        #Initialize the dictionary
        compiled_statistics = dict()

        try:
            striking_accuracy_html = soup.find(class_='l-overlap-group__item--odd')

            # Case when there is only one athlete detail card
            if not striking_accuracy_html:
                striking_accuracy_html = soup.find(class_='l-overlap-group__item--odd--full-width')

                # If the athlete detail card is not for Striking Accuracy, then it does not exist
                if striking_accuracy_html.find(class_='c-overlap--stats__title').get_text().lower().strip() != "striking accuracy":
                    raise AttributeError()

            # Gather the striking statistics
            significant_strike_accuracy = striking_accuracy_html.find(class_='e-chart-circle__percent').get_text()
            significant_strikes = striking_accuracy_html.find_all(class_='c-overlap__stats-value')
            significant_strikes_landed = significant_strikes[0].get_text()
            significant_strikes_attempted = significant_strikes[1].get_text()

            # Insert statistics into our dictionary
            compiled_statistics['significant_strikes_landed'] = significant_strikes_landed if significant_strikes_landed else '0'
            compiled_statistics['significant_strikes_attempted'] = significant_strikes_attempted if significant_strikes_attempted else '0'
            compiled_statistics['significant_strike_accuracy'] = significant_strike_accuracy if significant_strike_accuracy else '0'
        
        except AttributeError:
            # The Striking Accuracy detail card does not exist
            compiled_statistics.update(
                 {'significant_strikes_landed': '0',
                    'significant_strikes_attempted': '0',
                    'significant_strike_accuracy': '0'}
            )
            
        return compiled_statistics


    def scrape_grappling_accuracy(self, soup):
        """
            Scrapes the athlete's grappling accuracy.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict
        
        """
        #Initialize the dictionary
        compiled_statistics = dict()

        try:
            grappling_accuracy_html = soup.find(class_='l-overlap-group__item--even')

            # Case when there is only one athlete detail card
            if not grappling_accuracy_html:
                grappling_accuracy_html = soup.find(class_='l-overlap-group__item--odd--full-width')

                # If the athlete detail card is not for Grappling Accuracy, then it does not exist
                if grappling_accuracy_html.find(class_='c-overlap--stats__title').get_text().lower().strip() != "grappling accuracy":
                    raise AttributeError()

            # Gather the takedown statistics
            takedown_accuracy = grappling_accuracy_html.find(class_='e-chart-circle__percent').get_text()
            takedowns = grappling_accuracy_html.find_all(class_='c-overlap__stats-value')
            takedowns_landed = takedowns[0].get_text()
            takedowns_attempted = takedowns[1].get_text()

            # Insert statistics into our dictionary
            compiled_statistics['takedowns_landed'] = takedowns_landed if takedowns_landed else '0'
            compiled_statistics['takedowns_attempted'] = takedowns_attempted if takedowns_attempted else '0'
            compiled_statistics['takedown_accuracy'] = takedown_accuracy if takedown_accuracy else '0'
        
        except AttributeError:
            # The Grappling Accuracy detail card does not exist

            compiled_statistics.update(
                {'takedowns_landed': '0',
                    'takedowns_attempted': '0',
                    'takedown_accuracy': '0'}
            )
            
        return compiled_statistics


    def scrape_fight_metrics(self, soup):
        """
            Scrapes the athlete's fight metrics.

            :param soup: The html of the UFC athlete's page
            :type soup: BeautifulSoup
            :returns: dict
        
        """
        # Initialize the dictionary
        compiled_statistics = dict()

        try:
            fight_metric_html = soup.find(class_='l-container__content--narrow stats-records__outer-container')

            # Get all the rows of metrics that have 2 columns
            metric_rows = fight_metric_html.find_all(class_='c-stats-group-2col')
            # Iterate through each row
            for metric_row in metric_rows:
                if isinstance(metric_row, bs4.element.Tag):
                    # Get each column in the row
                    metric_columns = metric_row.find_all(class_='c-stat-compare')
                    # Iterate through each column in the row
                    for metric_column in metric_columns:
                        # Get the left and right section of the column
                        metric_left_section = metric_column.find(class_='c-stat-compare__group-1')
                        metric_right_section = metric_column.find(class_='c-stat-compare__group-2')

                        for metric_section in [metric_left_section, metric_right_section]:
                            # Extract the relevant information and clean the data
                            label = metric_section.find(class_='c-stat-compare__label').get_text()
                            label = label.lower().replace('sig. str.', 'significant strikes').replace('avg', 'average').replace(' ', '_')

                            #Try to get the following stat, otherwise assign a 0
                            stat_html = metric_section.find(class_='c-stat-compare__number')
                            stat = stat_html.get_text().replace('\n', '').replace(' ', '') if stat_html else '0'

                            # Append label suffix if it exists
                            label_suffix = metric_section.find(class_='c-stat-compare__label-suffix')
                            if label_suffix is not None:
                                label_suffix = label_suffix.get_text()
                                label_suffix = label_suffix.lower().replace(' ', '_')
                                label = label + '_' + label_suffix

                            # Insert label and stat into our dictionary
                            compiled_statistics[label] = stat

            # Get the last row of metrics that has 3 columns
            last_metric_row = fight_metric_html.find(class_='c-stats-group-3col')
            # Iterate through each column in the row
            for metric_column in last_metric_row:
                if isinstance(metric_column, bs4.element.Tag):
                    metric_section = metric_column.find(class_='c-stat-3bar')
                    if metric_section is None:
                        metric_section = metric_column.find(class_='c-stat-body')

                        # Extract the relevant information and clean the data
                        label = metric_section.find(class_='e-t5').get_text()
                        label = label.lower().replace('sig. str.', 'significant strikes').replace(' ', '_')

                        # Try to get the following stats, otherwise assign a 0
                        stat_head_html = metric_section.find(id="e-stat-body_x5F__x5F_head_value")
                        stat_head = stat_head_html.get_text().replace('\n', '').replace(' ', '') if stat_head_html else '0'

                        stat_body_html = metric_section.find(id="e-stat-body_x5F__x5F_body_value")
                        stat_body = stat_body_html.get_text().replace('\n', '').replace(' ', '') if stat_body_html else '0'

                        stat_leg_html = metric_section.find(id="e-stat-body_x5F__x5F_leg_value")
                        stat_leg = stat_leg_html.get_text().replace('\n', '').replace(' ', '') if stat_leg_html else '0'

                        # Insert into our dictionary
                        compiled_statistics[label+"_head"] = stat_head
                        compiled_statistics[label+"_body"] = stat_body
                        compiled_statistics[label+"_leg"] = stat_leg

                    else:
                        # Extract the relevant information and clean the data
                        label = metric_section.find(class_='c-stat-3bar__title').get_text()
                        label = label.lower().replace('sig. str.', 'significant strikes').replace(' ', '_')
                        metric_entries = metric_section.find_all(class_='c-stat-3bar__group')
                        for metric_entry in metric_entries:
                            if isinstance(metric_entry, bs4.element.Tag):
                                label_suffix = metric_entry.find(class_='c-stat-3bar__label').get_text()
                                label_suffix = label_suffix.replace("KO/TKO", "knockout").replace("DEC", "decision").replace("SUB", "submission").lower().strip()
                                full_label = label + "_" + label_suffix

                                # Try to get the following stat, otherwise assign a 0
                                stat_html = metric_entry.find(class_='c-stat-3bar__value')
                                stat = stat_html.get_text().split(" ")[0] if stat_html else '0'

                                # Insert into our dictionary
                                compiled_statistics[full_label] = stat

        except AttributeError:

            compiled_statistics.update(
                {'significant_strikes_landed_per_min': '0',
                    'significant_strikes_absorbed_per_min': '0',
                    'takedown_average_per_15_min': '0',
                    'submission_average_per_15_min': '0',
                    'significant_strikes_defense': '0',
                    'takedown_defense': '0',
                    'knockdown_ratio': '0',
                    'average_fight_time': '0:00',
                    'significant_strikes_by_position_standing': '0',
                    'significant_strikes_by_position_clinch': '0',
                    'significant_strikes_by_position_ground': '0',
                    'significant_strikes_by_target_head': '0',
                    'significant_strikes_by_target_body': '0',
                    'significant_strikes_by_target_leg': '0',
                    'win_by_way_knockout' : '0',
                    'win_by_way_decision': '0',
                    'win_by_way_submission':'0'}
            )

        return compiled_statistics


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

        # Get the html of the athlete's page on the UFC website
        url = self.BASE_URL + athlete_name.lower().replace(" ", "-")
        page = requests.get(url)
        if page.status_code != 200:
            print(f'{athlete_name} not found!')
        html_content = page.text
        soup = bs4.BeautifulSoup(html_content, 'html.parser')

        # Get the data from the html
        athlete_statistics['nickname'] = self.scrape_athlete_nickname(soup)
        athlete_statistics['record'] = self.scrape_athlete_record(soup)
        athlete_statistics['ranking'] = self.scrape_athlete_ranking(soup)
        athlete_statistics.update(self.scrape_athlete_biography(soup))
        athlete_statistics.update(self.scrape_striking_accuracy(soup))
        athlete_statistics.update(self.scrape_grappling_accuracy(soup))
        athlete_statistics.update(self.scrape_fight_metrics(soup))

        return athlete_statistics 


def main():
    start_time = time.time()
    ufc_scraper = UFCWebsiteScraper()

    print("Updating file ufc_rankings.txt . . .")
    ufc_scraper.scrape_ufc_rankings_to_txt_file()
    print("Update complete!")

    print("Scraping each fighter from the rankings . . .")
    with open('ufc_rankings.txt', 'r') as file:
        compiled_stats = []
        for line in file:
            compiled_stats.append(ufc_scraper.scrape_athelete_stats(line.strip()))

    print("Finished! Exporting to Excel . . .")
    ufc_scraper.export_to_excel(compiled_stats)
    print("Export complete! Please open ufc_fighter_stats.xlsx to view data.")
    
    program_time = round(time.time() - start_time, 2)
    print(f"---------- {program_time} seconds ----------")


if __name__ == "__main__":
    main() 