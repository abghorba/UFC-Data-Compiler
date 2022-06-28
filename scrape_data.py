import logging
import os
import time

from datetime import datetime
from scraper.ufc_scraper import UFCWebsiteScraper


def main():

    start_time = time.time()

    log_filename = datetime.now().strftime("%d%m%Y%H%M%S") + f"-results"
    log_filepath = os.getcwd() + f"/logs/{log_filename}.log"
    
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(module)s.py - %(funcName)s - [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler(log_filepath),
                                    logging.StreamHandler()])
                                  
    ufc_scraper = UFCWebsiteScraper()

    logging.info("Updating file ufc_rankings.txt . . .")
    text_filepath = ufc_scraper.scrape_ufc_rankings_to_txt_file()
    logging.info("Update complete!")

    logging.info("Scraping each fighter from the rankings . . .")

    with open(text_filepath, "r") as file:

        compiled_stats = []

        for line in file:

            # Skip the line detailing the division
            if not line.startswith("\t"):
                continue

            compiled_stats.append(ufc_scraper.scrape_athelete_stats(line.strip()))

    logging.info("Finished! Exporting to Excel . . .")
    excel_filepath = ufc_scraper.export_to_excel(compiled_stats)
    logging.info(f"Export complete! Please open {excel_filepath} to view data.")

    program_time = round(time.time() - start_time, 2)
    logging.info(f"---------- {program_time} seconds ----------")


if __name__ == "__main__":
    main()
