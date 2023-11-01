from bs4 import BeautifulSoup
import requests
import logging


def scrap_flipcart():
    with requests.Session() as session:
        logging.info('Started scraping on Flipkart')
        URL = "https://www.flipkart.com/search?q=playstation+5&sid=4rr%2Cx1m&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_na&as-pos=1&as-type=RECENT&suggestionId=playstation+5%7CGaming+Consoles&requestId=d063276a-976d-4d25-8d5c-ae3cc6547824&as-backfill=on"

        payload={}
        headers = {
                'Cookie': 'ci_session=se5ndh8br4u71l0hik5r60qafjmu6uni'
                }


        webpage = requests.get(URL, headers=headers, data=payload)

        soup = BeautifulSoup(webpage.text, "html.parser")

        try:
            links = soup.find_all("a", attrs={'class':'s1Q9rs'})

            link = links[0].get('href')

            product_list = "https://www.flipkart.com" + link

            new_webpage = requests.get(product_list, headers=headers, data=payload)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            logging.info('Scraped data from Flipkart')
            price = new_soup.soup.find('div', class_='_30jeq3 _16Jk6d')

            price = price.text.strip()
        
        except AttributeError:
            logging.info('Failed to scrap data from Flipkart')


    return price