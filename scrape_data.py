from ufc_scraper import UFCWebsiteScraper
import time

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