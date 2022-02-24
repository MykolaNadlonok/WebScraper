# WebScraper
Web scraping car data set from the website https://www.cars-data.com/


The library Beautifulsoup was used for web scraping. The parser - lxml.

You need to install BeautifulSoup, requests, lxml in order to run the code.

The method of proceeding is in the following way:
We find needed elements on the beginning page. Then we find the corresponding html code for those objects. In my case, at the first page
I look for car brands. Each car brand includes href, which leads to all car models of that concrete car brand.

The flow is:
1. Scrape Car brands, go Next
2. Scrape Car models, go Next,
3. Scrape Car versions, go Next,
4. Scrape All specific Car versions, go Next,

NOW the tables with a lot of specifications will be available.

5. Scrape All needed specifications.

One example csv file (BMW_cars_data.csv) is included in this repository. It represents the scraped specifications data about BMW cars. It contains 6137 rows.

Also the same data is in the file BMW_cars.xlsx. It allows to analyze the result deeply, to find errors, and it is a workspace for cleaning the data
