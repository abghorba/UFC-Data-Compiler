# UFC Data Compiler

<h2> Description </h2>
This is to pull fighter data from the UFC website and compile into an Excel file.

<h2> Usage </h2>
Install dependencies by calling

        pip install -r requirements.txt

Then you can use the following command

        python scrape_data.py

This will first scrape the rankings websites for UFC fighters and compile it into the ufc_rankings.txt file. Then, the code will read each line of 
ufc_rankings.txt and scrape the data from each athlete's UFC webpage. This will all be compiled and exported into an Excel file with the data:

        ufc_fighter_stats.xlsx

Feel free to use the data any way you wish!