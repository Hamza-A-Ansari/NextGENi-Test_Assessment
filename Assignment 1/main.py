import pandas as pd
from amazon import scrap_amazon
from flipkart import scrap_flipcart
import logging

def main():
    # Create Logging file
    logging.basicConfig(
        # filename=os.getenv('LOG_FILE'),
        filename='app.log',
        filemode='a',
        format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO )
    
    # Scrap the data from Amazon
    amazon_price = scrap_amazon

    # Scrap the data from flipkart
    flipkart_price = scrap_flipcart

    logging.info(f'The price of PlayStation 5 on Amazon is {amazon_price} INR whereas the price on flipkart is {flipkart_price} INR. So I suggest you to buy PlayStaion 5 on Amazon')

