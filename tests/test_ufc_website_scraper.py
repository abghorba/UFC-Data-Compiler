import bs4
import requests
import os
import pytest

from src.scraper.ufc_scraper import UFCWebsiteScraper


scraper = UFCWebsiteScraper()

def get_soup(athlete_name):
    """
    Helper function to get the soup object from the website's HTML.
    
    :param athlete_name: Str of the fighter's name
    :return: BeautifulSoup object
    """
    athlete_name = athlete_name.lower().replace(" ", "-")
    url = "https://www.ufc.com/athlete/" + athlete_name
    page = requests.get(url)
    html_content = page.text
    soup = bs4.BeautifulSoup(html_content, "html.parser")

    return soup


def test_export_to_excel():
    """Test that export_to_excel() creates an Excel file at the returned filepath."""

    data = [{"test_0": 0}, {"test_1": 1}, {"test_2": 2}]
    excel_filepath = scraper.export_to_excel(data)

    assert os.path.exists(excel_filepath)
    assert os.path.getsize(excel_filepath) > 0


def test_scrape_ufc_rankings_to_txt_file():
    """
    Test scrape_ufc_rankings_to_txt_file() creates a Text file at the returned filepath
    and that instance variable current_rankings_list gets updated.

    """
    txt_filepath = scraper.scrape_ufc_rankings_to_txt_file()

    assert len(scraper.current_rankings_list) > 0
    assert os.path.exists(txt_filepath)
    assert os.path.getsize(txt_filepath) > 0


# Expected values for test_scrape_athelete_biography()
khabib_bio = {
    "status": "Retired",
    "hometown": "Dagestan Republic, Russia",
    "trains_at": "American Kickboxing Academy (AKA)",
    "age": "33",
    "height": "70.00",
    "weight": "155.00",
    "octagon_debut": "Jan. 21, 2012",
    "reach": "70.00",
    "leg_reach": "40.00",
}

mcgregor_bio = {
    "status": "Active",
    "hometown": "Dublin, Ireland",
    "trains_at": "SBG Ireland",
    "age": "33",
    "height": "69.00",
    "weight": "156.00",
    "octagon_debut": "Apr. 06, 2013",
    "reach": "74.00",
    "leg_reach": "40.00",
}

jones_bio = {
    "status": "Active",
    "hometown": "Rochester, United States",
    "age": "34",
    "height": "76.00",
    "weight": "204.00",
    "octagon_debut": "Aug. 09, 2008",
    "reach": "84.50",
    "leg_reach": "45.00",
}

andrew_bio = {
    "status": "",
    "hometown": "",
    "age": "",
    "height": "",
    "weight": "",
    "octagon_debut": "",
    "reach": "",
    "leg_reach": "",
}

@pytest.mark.parametrize(
    "athlete_name,expected_bio",
    [
        ("Khabib Nurmagomedov", khabib_bio),
        ("Conor McGregor", mcgregor_bio),
        ("Jon Jones", jones_bio),
        ("Andrew Ghorbani", andrew_bio)],
)
def test_scrape_athelete_biography(athlete_name, expected_bio):
    """
    Test that scrape_athlete_biography() parses the biography section correctly.
    
    :param athlete_name: Str of the fighter's name
    """

    soup = get_soup(athlete_name)
    scraped_bio = scraper.scrape_athlete_biography(soup)
    assert scraped_bio == expected_bio


@pytest.mark.parametrize(
    "athlete_name,expected_nickname",
    [
        ("Khabib Nurmagomedov", "The Eagle"),
        ( "Conor McGregor", "The Notorious"),
        ( "Jon Jones", "Bones"),
        ("Andrew Ghorbani", ""),
    ]
)
def test_scrape_athlete_nickname(athlete_name, expected_nickname):
    """
    Test that scrape_athlete_nickname() works correctly.
    
    :param athlete_name: Str of the fighter's name
    :param expected_nickname: Str of the expected nickname that should be scraped
    """

    soup = get_soup(athlete_name)
    scraped_nickname = scraper.scrape_athlete_nickname(soup)
    assert scraped_nickname == expected_nickname


@pytest.mark.parametrize(
    "athlete_name,expected_record",
    [
        ("Khabib Nurmagomedov", "29-0-0 (W-L-D)"),
        ("Conor McGregor", "22-6-0 (W-L-D)"),
        ("Jon Jones", "26-1-0 (W-L-D)"),
        ("Andrew Ghorbani", "")
    ],
)
def test_scrape_athlete_record(athlete_name, expected_record):
    """
    Test that scrape_athlete_record() works as intended.
    
    :param athlete_name: Str of the fighter's name
    :param expected_record: Str of the expected record that should be scraped
    """

    soup = get_soup(athlete_name)
    scraped_record = scraper.scrape_athlete_record(soup)
    assert scraped_record == expected_record


@pytest.mark.parametrize(
    "athlete_name,expected_ranking",
    [
        ("Khabib Nurmagomedov", "Former Fighter"),
        ("Conor McGregor", "#12 Lightweight Division"),
        ("Jon Jones", "Light Heavyweight Champion"),
        ("Andrew Ghorbani", "")
    ]
)
def test_scrape_athlete_ranking(athlete_name, expected_ranking):
    """
    Tests that scrape_athlete_ranking() works as intended.
    
    :param athlete_name: Str of the fighter's name
    :param expected_ranking: Str of the expected ranking that should be scraped 
    """

    soup = get_soup(athlete_name)
    scraped_ranking = scraper.scrape_athlete_ranking(soup)
    assert scraped_ranking == expected_ranking


# Expected values for test_scrape_striking_accuracy()
khabib_striking_stats = {
    "significant_strikes_landed": "705",
    "significant_strikes_attempted": "1444",
    "significant_strike_accuracy": "49%",
}

mcgregor_striking_stats = {
    "significant_strikes_landed": "599",
    "significant_strikes_attempted": "1204",
    "significant_strike_accuracy": "50%",
}

jones_striking_stats = {
    "significant_strikes_landed": "1463",
    "significant_strikes_attempted": "2526",
    "significant_strike_accuracy": "58%",
}

andrew_striking_stats = {
    "significant_strikes_landed": "0",
    "significant_strikes_attempted": "0",
    "significant_strike_accuracy": "0",
}

@pytest.mark.parametrize(
    "athlete_name,expected_striking_stats",
    [
        ("Khabib Nurmagomedov", khabib_striking_stats),
        ("Conor McGregor", mcgregor_striking_stats),
        ("Jon Jones", jones_striking_stats),
        ("Andrew Ghorbani", andrew_striking_stats)
    ]
)
def test_scrape_striking_accuracy(athlete_name, expected_striking_stats):
    """
    Tests that scrape_striking_accuracy() works as intended.
    
    :param athlete_name: Str of the fighter's name
    :param expected_striking_stats: Dict of the expected striking stats that should be scraped
    """

    soup = get_soup(athlete_name)
    scraped_striking_stats = scraper.scrape_striking_accuracy(soup)
    assert scraped_striking_stats == expected_striking_stats


# Expected values for test_scrape_grappling_accuracy()
khabib_grappling_stats = {
    "takedowns_landed": "49",
    "takedowns_attempted": "127",
    "takedown_accuracy": "48%",
}

mcgregor_grappling_stats = {
    "takedowns_landed": "0",
    "takedowns_attempted": "9",
    "takedown_accuracy": "56%",
}

jones_grappling_stats = {
    "takedowns_landed": "36",
    "takedowns_attempted": "95",
    "takedown_accuracy": "44%",
}

andrew_grappling_stats = {
    "takedowns_landed": "0",
    "takedowns_attempted": "0",
    "takedown_accuracy": "0",
}

@pytest.mark.parametrize(
    "athlete_name,expected_grappling_stats",
    [
        ("Khabib Nurmagomedov", khabib_grappling_stats),
        ("Conor McGregor", mcgregor_grappling_stats),
        ("Jon Jones", jones_grappling_stats),
        ("Andrew Ghorbani", andrew_grappling_stats)
    ]
)
def test_scrape_grappling_accuracy(athlete_name, expected_grappling_stats):
    """Tests that scrape_grappling_accuracy() works as intended.
    
    :param athlete_name: Str of the fighter's name
    :param expected_grappling_stats: Dict of the expected grappling stats that should be scraped
    """
    
    soup = get_soup(athlete_name)
    scraped_grappling_stats = scraper.scrape_grappling_accuracy(soup)
    assert scraped_grappling_stats == expected_grappling_stats


# Expected values for test_scrape_fight_metrics()
khabib_fight_metrics = {
    "significant_strikes_landed_per_min": "4.10",
    "significant_strikes_absorbed_per_min": "1.75",
    "takedown_average_per_15_min": "5.32",
    "submission_average_per_15_min": "0.79",
    "significant_strikes_defense": "65%",
    "takedown_defense": "85%",
    "knockdown_ratio": "0.17",
    "average_fight_time": "13:13",
    "significant_strikes_by_position_standing": "298",
    "significant_strikes_by_position_clinch": "27",
    "significant_strikes_by_position_ground": "380",
    "significant_strikes_by_target_head": "604",
    "significant_strikes_by_target_body": "65",
    "significant_strikes_by_target_leg": "36",
    "win_by_way_knockout": "8",
    "win_by_way_decision": "10",
    "win_by_way_submission": "11",
}

mcgregor_fight_metrics = {
    "significant_strikes_landed_per_min": "5.32",
    "significant_strikes_absorbed_per_min": "4.66",
    "takedown_average_per_15_min": "0.67",
    "submission_average_per_15_min": "0.13",
    "significant_strikes_defense": "54%",
    "takedown_defense": "67%",
    "knockdown_ratio": "1.73",
    "average_fight_time": "08:02",
    "significant_strikes_by_position_standing": "461",
    "significant_strikes_by_position_clinch": "61",
    "significant_strikes_by_position_ground": "77",
    "significant_strikes_by_target_head": "419",
    "significant_strikes_by_target_body": "102",
    "significant_strikes_by_target_leg": "78",
    "win_by_way_knockout": "19",
    "win_by_way_decision": "2",
    "win_by_way_submission": "1",
}

jones_fight_metrics = {
    "significant_strikes_landed_per_min": "4.30",
    "significant_strikes_absorbed_per_min": "2.22",
    "takedown_average_per_15_min": "1.85",
    "submission_average_per_15_min": "0.44",
    "significant_strikes_defense": "64%",
    "takedown_defense": "95%",
    "knockdown_ratio": "0.22",
    "average_fight_time": "15:28",
    "significant_strikes_by_position_standing": "953",
    "significant_strikes_by_position_clinch": "248",
    "significant_strikes_by_position_ground": "262",
    "significant_strikes_by_target_head": "687",
    "significant_strikes_by_target_body": "359",
    "significant_strikes_by_target_leg": "417",
    "win_by_way_knockout": "10",
    "win_by_way_decision": "7",
    "win_by_way_submission": "6",
}

andrew_fight_metrics = {
    "significant_strikes_landed_per_min": "0",
    "significant_strikes_absorbed_per_min": "0",
    "takedown_average_per_15_min": "0",
    "submission_average_per_15_min": "0",
    "significant_strikes_defense": "0",
    "takedown_defense": "0",
    "knockdown_ratio": "0",
    "average_fight_time": "0:00",
    "significant_strikes_by_position_standing": "0",
    "significant_strikes_by_position_clinch": "0",
    "significant_strikes_by_position_ground": "0",
    "significant_strikes_by_target_head": "0",
    "significant_strikes_by_target_body": "0",
    "significant_strikes_by_target_leg": "0",
    "win_by_way_knockout": "0",
    "win_by_way_decision": "0",
    "win_by_way_submission": "0",
}

@pytest.mark.parametrize(
    "athlete_name,expected_fight_metrics",
    [
        ("Khabib Nurmagomedov", khabib_fight_metrics),
        ("Conor McGregor", mcgregor_fight_metrics),
        ("Jon Jones", jones_fight_metrics),
        ("Andrew Ghorbani", andrew_fight_metrics)],
)
def test_scrape_fight_metrics(athlete_name, expected_fight_metrics):
    """
    Tests that scrape_fight_metrics() works as intended.
    
    :param athlete_name: Str of the fighter's name
    :param expected_fight_metrics: Dict of the expected fight metrics that should be scraped
    """

    soup = get_soup(athlete_name)
    scraped_fight_metrics = scraper.scrape_fight_metrics(soup)
    assert scraped_fight_metrics == expected_fight_metrics


# Expected values for test_scrape_athlete_stats()
khabib_stats = {
    "name": "Khabib Nurmagomedov",
    "record": "29-0-0 (W-L-D)",
    "nickname": "The Eagle",
    "ranking": "Former Fighter",
    "status": "Retired",
    "hometown": "Dagestan Republic, Russia",
    "trains_at": "American Kickboxing Academy (AKA)",
    "age": "33",
    "height": "70.00",
    "weight": "155.00",
    "octagon_debut": "Jan. 21, 2012",
    "reach": "70.00",
    "leg_reach": "40.00",
    "significant_strikes_landed": "705",
    "significant_strikes_attempted": "1444",
    "significant_strike_accuracy": "49%",
    "takedowns_landed": "49",
    "takedowns_attempted": "127",
    "takedown_accuracy": "48%",
    "significant_strikes_landed_per_min": "4.10",
    "significant_strikes_absorbed_per_min": "1.75",
    "takedown_average_per_15_min": "5.32",
    "submission_average_per_15_min": "0.79",
    "significant_strikes_defense": "65%",
    "takedown_defense": "85%",
    "knockdown_ratio": "0.17",
    "average_fight_time": "13:13",
    "significant_strikes_by_position_standing": "298",
    "significant_strikes_by_position_clinch": "27",
    "significant_strikes_by_position_ground": "380",
    "significant_strikes_by_target_head": "604",
    "significant_strikes_by_target_body": "65",
    "significant_strikes_by_target_leg": "36",
    "win_by_way_knockout": "8",
    "win_by_way_decision": "10",
    "win_by_way_submission": "11",
}

mcgregor_stats = {
    "name": "Conor McGregor",
    "record": "22-6-0 (W-L-D)",
    "nickname": "The Notorious",
    "ranking": "#12 Lightweight Division",
    "status": "Active",
    "hometown": "Dublin, Ireland",
    "trains_at": "SBG Ireland",
    "age": "33",
    "height": "69.00",
    "weight": "156.00",
    "octagon_debut": "Apr. 06, 2013",
    "reach": "74.00",
    "leg_reach": "40.00",
    "significant_strikes_landed": "599",
    "significant_strikes_attempted": "1204",
    "significant_strike_accuracy": "50%",
    "takedowns_landed": "0",
    "takedowns_attempted": "9",
    "takedown_accuracy": "56%",
    "significant_strikes_landed_per_min": "5.32",
    "significant_strikes_absorbed_per_min": "4.66",
    "takedown_average_per_15_min": "0.67",
    "submission_average_per_15_min": "0.13",
    "significant_strikes_defense": "54%",
    "takedown_defense": "67%",
    "knockdown_ratio": "1.73",
    "average_fight_time": "08:02",
    "significant_strikes_by_position_standing": "461",
    "significant_strikes_by_position_clinch": "61",
    "significant_strikes_by_position_ground": "77",
    "significant_strikes_by_target_head": "419",
    "significant_strikes_by_target_body": "102",
    "significant_strikes_by_target_leg": "78",
    "win_by_way_knockout": "19",
    "win_by_way_decision": "2",
    "win_by_way_submission": "1",
}

jones_stats = {
    "name": "Jon Jones",
    "nickname": "Bones",
    "record": "26-1-0 (W-L-D)",
    "ranking": "Light Heavyweight Champion",
    "status": "Active",
    "hometown": "Rochester, United States",
    "age": "34",
    "height": "76.00",
    "weight": "204.00",
    "octagon_debut": "Aug. 09, 2008",
    "reach": "84.50",
    "leg_reach": "45.00",
    "significant_strikes_landed": "1463",
    "significant_strikes_attempted": "2526",
    "significant_strike_accuracy": "58%",
    "takedowns_landed": "36",
    "takedowns_attempted": "95",
    "takedown_accuracy": "44%",
    "significant_strikes_landed_per_min": "4.30",
    "significant_strikes_absorbed_per_min": "2.22",
    "takedown_average_per_15_min": "1.85",
    "submission_average_per_15_min": "0.44",
    "significant_strikes_defense": "64%",
    "takedown_defense": "95%",
    "knockdown_ratio": "0.22",
    "average_fight_time": "15:28",
    "significant_strikes_by_position_standing": "953",
    "significant_strikes_by_position_clinch": "248",
    "significant_strikes_by_position_ground": "262",
    "significant_strikes_by_target_head": "687",
    "significant_strikes_by_target_body": "359",
    "significant_strikes_by_target_leg": "417",
    "win_by_way_knockout": "10",
    "win_by_way_decision": "7",
    "win_by_way_submission": "6",
}

andrew_stats = {
    "name": "Andrew Ghorbani",
    "nickname": "",
    "record": "",
    "ranking": "",
    "status": "",
    "hometown": "",
    "age": "",
    "height": "",
    "weight": "",
    "octagon_debut": "",
    "reach": "",
    "leg_reach": "",
    "significant_strikes_landed": "0",
    "significant_strikes_attempted": "0",
    "significant_strike_accuracy": "0",
    "takedowns_landed": "0",
    "takedowns_attempted": "0",
    "takedown_accuracy": "0",
    "significant_strikes_landed_per_min": "0",
    "significant_strikes_absorbed_per_min": "0",
    "takedown_average_per_15_min": "0",
    "submission_average_per_15_min": "0",
    "significant_strikes_defense": "0",
    "takedown_defense": "0",
    "knockdown_ratio": "0",
    "average_fight_time": "0:00",
    "significant_strikes_by_position_standing": "0",
    "significant_strikes_by_position_clinch": "0",
    "significant_strikes_by_position_ground": "0",
    "significant_strikes_by_target_head": "0",
    "significant_strikes_by_target_body": "0",
    "significant_strikes_by_target_leg": "0",
    "win_by_way_knockout": "0",
    "win_by_way_decision": "0",
    "win_by_way_submission": "0",
}

@pytest.mark.parametrize(
    "athlete_name,expected_stats",
    [
        ("Khabib Nurmagomedov", khabib_stats),
        ("Conor McGregor", mcgregor_stats),
        ("Jon Jones", jones_stats),
        ("Andrew Ghorbani", andrew_stats),
    ]
)
def test_scrape_athelete_stats(athlete_name, expected_stats):
    """
    Tests that scrape_athlete_stats() works as intended.

    :param athlete_name: Str of the fighter's name
    :param expected_stats: Dict of the expected stats that should be scraped
    """

    scraped_stats = scraper.scrape_athelete_stats(athlete_name)
    assert scraped_stats == expected_stats
