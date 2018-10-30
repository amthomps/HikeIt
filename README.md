# HikeIt
A web app to help hikers make informed decisions when searching for new trails  

http://hikeit.site/

## DataCollection_Trip_Reports.ipynb  
This notebook contains the code for scraping trail reviews from the Washington Trails Association website wta.org.  Remember to scrape respectfully and avoid overloading servers.  These reports were collected over several days.  

The scraping code contains two parts.  First, a list of urls for recent trip reports (trail reviews) was collected from the trip reports page.  This step was necessary because I could not find a pattern to the urls of consecutive reports, there is a string in the url that seems to be random.  Scraping the list first allowed me to ensure I was retrieving recent reports.

The second part is walks through the list of trip report urls and scrapes the pages one by one.  For the product, I only used the free text from the report, the title, and the date.  Although I didn't end up using it, I also scraped other details on the page, such as the number of people who found the review helpful and any tags that the user selected to accompany their review.

## Topic_Modeling_Trail_Reviews.ipynb
This notebook contains a few topic models I tried for extracting relevant topics in the free text.  The product allows the user to select their topic of interest; this model assigns paragraphs to topics to allow this retrieval.

## Website/
This file contains code needed to run the website.
