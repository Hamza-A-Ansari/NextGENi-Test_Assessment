from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import logging

def scrap_amazon():
    with requests.Session() as session:
        logging.info('Started scraping on Amazon')
        URL = "https://www.amazon.com/s?k=playstation+5&crid=3BV45YDFQQE2G&sprefix=playstation+4%2Caps%2C269&ref=nb_sb_noss_2"

        # Headers for request
        load_dotenv()
        user_agent = os.getenv('user_agent')
        HEADERS = ({'User-Agent':user_agent, 'Accept-Language': 'en-US, en;q=0.5'}) #add your user agent

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        type(webpage.content)

        # Soup Object containiang all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        try:
            # Fetch links as List of Tag Objects
            links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

            link = links[0].get('href')

            product_list = "https://amazon.com" + link

            # print(product_list)

            new_webpage = requests.get(product_list, headers=HEADERS)

            # Soup Object containiang all data
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # print(new_soup)

            new_soup.find("span", attrs={"id":'productTitle'}).text.strip()

            logging.info('Scraped data from Amazon')
            price = new_soup.find("span", attrs={"class":'a-price a-text-price a-size-medium'}).find("span", attrs={"class": "a-offscreen"}).text

            # Convert Dollar into Indian Rupees
            price = price * 83.28 # Current Dollar to INR

        except AttributeError:
            logging.info('Failed to scrap data from Amazon')

    return price
