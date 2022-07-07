import time

from src.scraper.ufc_scraper import UFCWebsiteScraper


def main():

    start_time = time.time()
                                  
    ufc_scraper = UFCWebsiteScraper()

    print("Updating file ufc_rankings.txt . . .")
    text_filepath = ufc_scraper.scrape_ufc_rankings_to_txt_file()
    current_rankings_list = ufc_scraper.current_rankings_list
    print("Update complete!")

    print("Scraping each fighter from the rankings . . .")

    results = ufc_scraper.threaded_scrape_athlete_stats(current_rankings_list)

    # with open(text_filepath, "r") as file:

    #     results = []

    #     for line in file:

    #         # Skip the line detailing the division
    #         if line.startswith("\t"):
    #             results.append(ufc_scraper.scrape_athelete_stats(line.strip()))

    print("Finished! Exporting to Excel . . .")
    excel_filepath = ufc_scraper.export_to_excel(results)
    print(f"Export complete! Please open {excel_filepath} to view data.")

    program_time = round(time.time() - start_time, 2)
    print(f"---------- {program_time} seconds ----------")


if __name__ == "__main__":
    main()
