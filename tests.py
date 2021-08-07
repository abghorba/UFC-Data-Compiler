import ufc_scraper
import bs4
import requests
import pytest


class TestUFCWebsiteScraper():

    def get_soup(self, athlete_name):
        athlete_name = athlete_name.lower().replace(" ", "-")
        url = "https://www.ufc.com/athlete/" + athlete_name
        page = requests.get(url)
        html_content = page.text
        soup = bs4.BeautifulSoup(html_content, 'html.parser')

        return soup


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_athelete_biography(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_bio = scraper.scrape_athlete_biography(soup)

        khabib_bio = {'status': 'Retired',
                        'hometown': 'Dagestan Republic, Russia',
                        'trains_at': 'AKA (American Kickboxing Academy) San Jose',
                        'age': '32',
                        'height': '70.00',
                        'weight': '155.00',
                        'octagon_debut': 'Jan. 21, 2012',
                        'reach': '70.00',
                        'leg_reach': '40.00'}

        mcgregor_bio = {'status': 'Active',
                        'hometown': 'Dublin, Ireland',
                        'trains_at': 'SBG Ireland',
                        'age': '32',
                        'height': '69.00',
                        'weight': '145.00',
                        'octagon_debut': 'Apr. 06, 2013',
                        'reach': '74.00',
                        'leg_reach': '40.00'}

        jones_bio = {'status': 'Active',
                        'hometown': 'Rochester, United States',
                        'age': '33',
                        'height': '76.00',
                        'weight': '205.00',
                        'octagon_debut': 'Aug. 09, 2008',
                        'reach': '84.50',
                        'leg_reach': '45.00'}

        if athlete_name == 'Khabib Nurmagomedov':
            assert len(scraped_bio) == len(khabib_bio)
            assert scraped_bio == khabib_bio
        elif athlete_name == 'Conor McGregor':
            assert len(scraped_bio) == len(mcgregor_bio)
            assert scraped_bio == mcgregor_bio
        elif athlete_name == 'Jon Jones':
            assert len(scraped_bio) == len(jones_bio)
            assert scraped_bio == jones_bio


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_athlete_nickname(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_nickname = scraper.scrape_athlete_nickname(soup)

        khabib_nickname = 'The Eagle'
        mcgregor_nickname = 'The Notorious'
        jones_nickname = 'Bones'

        if athlete_name == 'Khabib Nurmagomedov':
            assert scraped_nickname == khabib_nickname
        elif athlete_name == 'Conor McGregor':
            assert scraped_nickname == mcgregor_nickname
        elif athlete_name == 'Jon Jones':
            assert scraped_nickname == jones_nickname


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_athlete_record(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_record = scraper.scrape_athlete_record(soup)

        khabib_record = '29-0-0 (W-L-D)'
        mcgregor_record = '22-6-0 (W-L-D)'
        jones_record = '26-1-0 (W-L-D)'

        if athlete_name == 'Khabib Nurmagomedov':
            assert scraped_record == khabib_record
        elif athlete_name == 'Conor McGregor':
            assert scraped_record == mcgregor_record
        elif athlete_name == 'Jon Jones':
            assert scraped_record == jones_record


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_athlete_ranking(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_ranking = scraper.scrape_athlete_ranking(soup)

        khabib_ranking = 'Former Fighter'
        mcgregor_ranking = '#9 Lightweight Division'
        jones_ranking = 'Light Heavyweight Champion'

        if athlete_name == 'Khabib Nurmagomedov':
            assert scraped_ranking == khabib_ranking
        elif athlete_name == 'Conor McGregor':
            assert scraped_ranking == mcgregor_ranking
        elif athlete_name == 'Jon Jones':
            assert scraped_ranking == jones_ranking


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_striking_accuracy(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_striking_stats = scraper.scrape_striking_accuracy(soup)

        khabib_striking_stats = {'significant_strikes_landed': '705',
                                    'significant_strikes_attempted': '1444',
                                    'significant_strike_accuracy': '49%'}

        mcgregor_striking_stats = {'significant_strikes_landed': '599',
                                    'significant_strikes_attempted': '1204',
                                    'significant_strike_accuracy': '50%'}

        jones_striking_stats = {'significant_strikes_landed': '1463',
                                    'significant_strikes_attempted': '2526',
                                    'significant_strike_accuracy': '58%'}

        if athlete_name == 'Khabib Nurmagomedov':
            assert len(scraped_striking_stats) == len(khabib_striking_stats)
            assert scraped_striking_stats == khabib_striking_stats
        elif athlete_name == 'Conor McGregor':
            assert len(scraped_striking_stats) == len(mcgregor_striking_stats)
            assert scraped_striking_stats == mcgregor_striking_stats
        elif athlete_name == 'Jon Jones':
            assert len(scraped_striking_stats) == len(jones_striking_stats)
            assert scraped_striking_stats == jones_striking_stats


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_grappling_accuracy(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_grappling_stats = scraper.scrape_grappling_accuracy(soup)

        khabib_grappling_stats = {'takedowns_landed': '49',
                                    'takedowns_attempted': '127',
                                    'takedown_accuracy': '48%'}

        mcgregor_grappling_stats = {'takedowns_landed': '0',
                                    'takedowns_attempted': '9',
                                    'takedown_accuracy': '56%'}

        jones_grappling_stats = {'takedowns_landed': '36',
                                    'takedowns_attempted': '95',
                                    'takedown_accuracy': '44%'}

        if athlete_name == 'Khabib Nurmagomedov':
            assert len(scraped_grappling_stats) == len(khabib_grappling_stats)
            assert scraped_grappling_stats == khabib_grappling_stats
        elif athlete_name == 'Conor McGregor':
            assert len(scraped_grappling_stats) == len(mcgregor_grappling_stats)
            assert scraped_grappling_stats == mcgregor_grappling_stats
        elif athlete_name == 'Jon Jones':
            assert len(scraped_grappling_stats) == len(jones_grappling_stats)
            assert scraped_grappling_stats == jones_grappling_stats


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_fight_metrics(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        soup = self.get_soup(athlete_name)
        scraped_fight_metrics = scraper.scrape_fight_metrics(soup)

        khabib_fight_metrics = {'significant_strikes_landed_per_min': '4.10',
                                'significant_strikes_absorbed_per_min': '1.75',
                                'takedown_average_per_15_min': '5.32',
                                'submission_average_per_15_min': '0.79',
                                'significant_strikes_defense': '65%',
                                'takedown_defense': '85%',
                                'knockdown_ratio': '0.17',
                                'average_fight_time': '13:13',
                                'significant_strikes_by_position_standing': '298',
                                'significant_strikes_by_position_clinch': '27',
                                'significant_strikes_by_position_ground': '380',
                                'significant_strikes_by_target_head': '604',
                                'significant_strikes_by_target_body': '65',
                                'significant_strikes_by_target_leg': '36',
                                'win_by_way_knockout' : '8',
                                'win_by_way_decision': '10',
                                'win_by_way_submission':'11'}

        mcgregor_fight_metrics = {'significant_strikes_landed_per_min': '5.32',
                                    'significant_strikes_absorbed_per_min': '4.66',
                                    'takedown_average_per_15_min': '0.67',
                                    'submission_average_per_15_min': '0.13',
                                    'significant_strikes_defense': '54%',
                                    'takedown_defense': '67%',
                                    'knockdown_ratio': '1.73',
                                    'average_fight_time': '08:02',
                                    'significant_strikes_by_position_standing': '461',
                                    'significant_strikes_by_position_clinch': '61',
                                    'significant_strikes_by_position_ground': '77',
                                    'significant_strikes_by_target_head': '419',
                                    'significant_strikes_by_target_body': '102',
                                    'significant_strikes_by_target_leg': '78',
                                    'win_by_way_knockout' : '19',
                                    'win_by_way_decision': '2',
                                    'win_by_way_submission':'1'}

        jones_fight_metrics = {'significant_strikes_landed_per_min': '4.30',
                                'significant_strikes_absorbed_per_min': '2.22',
                                'takedown_average_per_15_min': '1.85',
                                'submission_average_per_15_min': '0.44',
                                'significant_strikes_defense': '64%',
                                'takedown_defense': '95%',
                                'knockdown_ratio': '0.22',
                                'average_fight_time': '15:28',
                                'significant_strikes_by_position_standing': '953',
                                'significant_strikes_by_position_clinch': '248',
                                'significant_strikes_by_position_ground': '262',
                                'significant_strikes_by_target_head': '687',
                                'significant_strikes_by_target_body': '359',
                                'significant_strikes_by_target_leg': '417',
                                'win_by_way_knockout' : '10',
                                'win_by_way_decision': '7',
                                'win_by_way_submission':'6'}

        if athlete_name == 'Khabib Nurmagomedov':
            assert len(scraped_fight_metrics) == len(khabib_fight_metrics)
            assert scraped_fight_metrics == khabib_fight_metrics
        elif athlete_name == 'Conor McGregor':
            assert len(scraped_fight_metrics) == len(mcgregor_fight_metrics)
            assert scraped_fight_metrics == mcgregor_fight_metrics
        elif athlete_name == 'Jon Jones':
            assert len(scraped_fight_metrics) == len(jones_fight_metrics)
            assert scraped_fight_metrics == jones_fight_metrics


    @pytest.mark.parametrize("athlete_name", [
        "Khabib Nurmagomedov",
        "Conor McGregor",
        "Jon Jones"
    ])
    def test_scrape_athelete_stats(self, athlete_name):
        scraper = ufc_scraper.UFCWebsiteScraper()
        scraped_stats = scraper.scrape_athelete_stats(athlete_name)

        khabib_stats = {'name': 'Khabib Nurmagomedov',
                        'record': '29-0-0 (W-L-D)',
                        'nickname': 'The Eagle',
                        'ranking': "Former Fighter",
                        'status': 'Retired',
                        'hometown': 'Dagestan Republic, Russia',
                        'trains_at': 'AKA (American Kickboxing Academy) San Jose',
                        'age': '32',
                        'height': '70.00',
                        'weight': '155.00',
                        'octagon_debut': 'Jan. 21, 2012',
                        'reach': '70.00',
                        'leg_reach': '40.00',
                        'significant_strikes_landed': '705',
                        'significant_strikes_attempted': '1444',
                        'significant_strike_accuracy': '49%',
                        'takedowns_landed': '49',
                        'takedowns_attempted': '127',
                        'takedown_accuracy': '48%',
                        'significant_strikes_landed_per_min': '4.10',
                        'significant_strikes_absorbed_per_min': '1.75',
                        'takedown_average_per_15_min': '5.32',
                        'submission_average_per_15_min': '0.79',
                        'significant_strikes_defense': '65%',
                        'takedown_defense': '85%',
                        'knockdown_ratio': '0.17',
                        'average_fight_time': '13:13',
                        'significant_strikes_by_position_standing': '298',
                        'significant_strikes_by_position_clinch': '27',
                        'significant_strikes_by_position_ground': '380',
                        'significant_strikes_by_target_head': '604',
                        'significant_strikes_by_target_body': '65',
                        'significant_strikes_by_target_leg': '36',
                        'win_by_way_knockout' : '8',
                        'win_by_way_decision': '10',
                        'win_by_way_submission':'11'}

        mcgregor_stats = {'name': 'Conor McGregor',
                        'record': '22-6-0 (W-L-D)',
                        'nickname': 'The Notorious',
                        'ranking': '#9 Lightweight Division',
                        'status': 'Active',
                        'hometown': 'Dublin, Ireland',
                        'trains_at': 'SBG Ireland',
                        'age': '32',
                        'height': '69.00',
                        'weight': '145.00',
                        'octagon_debut': 'Apr. 06, 2013',
                        'reach': '74.00',
                        'leg_reach': '40.00',
                        'significant_strikes_landed': '599',
                        'significant_strikes_attempted': '1204',
                        'significant_strike_accuracy': '50%',
                        'takedowns_landed': '0',
                        'takedowns_attempted': '9',
                        'takedown_accuracy': '56%',
                        'significant_strikes_landed_per_min': '5.32',
                        'significant_strikes_absorbed_per_min': '4.66',
                        'takedown_average_per_15_min': '0.67',
                        'submission_average_per_15_min': '0.13',
                        'significant_strikes_defense': '54%',
                        'takedown_defense': '67%',
                        'knockdown_ratio': '1.73',
                        'average_fight_time': '08:02',
                        'significant_strikes_by_position_standing': '461',
                        'significant_strikes_by_position_clinch': '61',
                        'significant_strikes_by_position_ground': '77',
                        'significant_strikes_by_target_head': '419',
                        'significant_strikes_by_target_body': '102',
                        'significant_strikes_by_target_leg': '78',
                        'win_by_way_knockout' : '19',
                        'win_by_way_decision': '2',
                        'win_by_way_submission':'1'}

        jones_stats = {'name': 'Jon Jones',
                        'nickname': 'Bones',
                        'record': '26-1-0 (W-L-D)',
                        'ranking': 'Light Heavyweight Champion',
                        'status': 'Active',
                        'hometown': 'Rochester, United States',
                        'age': '33',
                        'height': '76.00',
                        'weight': '205.00',
                        'octagon_debut': 'Aug. 09, 2008',
                        'reach': '84.50',
                        'leg_reach': '45.00',
                        'significant_strikes_landed': '1463',
                        'significant_strikes_attempted': '2526',
                        'significant_strike_accuracy': '58%',
                        'takedowns_landed': '36',
                        'takedowns_attempted': '95',
                        'takedown_accuracy': '44%',
                        'significant_strikes_landed_per_min': '4.30',
                        'significant_strikes_absorbed_per_min': '2.22',
                        'takedown_average_per_15_min': '1.85',
                        'submission_average_per_15_min': '0.44',
                        'significant_strikes_defense': '64%',
                        'takedown_defense': '95%',
                        'knockdown_ratio': '0.22',
                        'average_fight_time': '15:28',
                        'significant_strikes_by_position_standing': '953',
                        'significant_strikes_by_position_clinch': '248',
                        'significant_strikes_by_position_ground': '262',
                        'significant_strikes_by_target_head': '687',
                        'significant_strikes_by_target_body': '359',
                        'significant_strikes_by_target_leg': '417',
                        'win_by_way_knockout' : '10',
                        'win_by_way_decision': '7',
                        'win_by_way_submission':'6'}

        if athlete_name == 'Khabib Nurmagomedov':
            assert len(scraped_stats) == len(khabib_stats)
            assert scraped_stats == khabib_stats
        elif athlete_name == 'Conor McGregor':
            assert len(scraped_stats) == len(mcgregor_stats)
            assert scraped_stats == mcgregor_stats
        elif athlete_name == 'Jon Jones':
            assert len(scraped_stats) == len(jones_stats)
            assert scraped_stats == jones_stats