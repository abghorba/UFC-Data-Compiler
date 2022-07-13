import time

from src.scraper.ufc_scraper import UFCWebsiteScraper


def main():

    start_time = time.time()
                                  
    ufc_scraper = UFCWebsiteScraper()

    print("Scraping the UFC Rankings website . . .")
    text_filepath = ufc_scraper.scrape_ufc_rankings_to_txt_file()
    print(f"Finished! Scraped UFC Rankings to {text_filepath}")

    print("Scraping each fighter from the rankings . . .")
    current_rankings_list = ufc_scraper.current_rankings_list
    results = ufc_scraper.threaded_scrape_athlete_stats(current_rankings_list)
    print("Finished!")

    print("Exporting data to Excel. . .")
    excel_filepath = ufc_scraper.export_to_excel(results)
    print(f"Finished! Scraped data to {excel_filepath}")

    program_time = round(time.time() - start_time, 2)

    print(f"--------------- {program_time} seconds ---------------")


if __name__ == "__main__":
    main()
