# -*- coding: utf-8 -*-
"""
main.py
Created on: 07/26/2023
@author: https://github.com/devAbreu
"""

import os
import re
from dotenv import load_dotenv
import logging
import requests

load_dotenv()

"""
Setup and configuration for the script.

This block of code sets up logging, retrieves environment variables, and sets a constant.

1. `dir_path` and `filename`: These lines determine the directory path of the current script 
   and the filename for the log file.

2. `logging.basicConfig`: This line sets up basic configuration for the logging module. 
   Logs will be written to the file specified by `filename`, with a log level of DEBUG. 
   The format of the log messages is also specified.

3. `API_BASE_URL`: This line retrieves the base URL of the API from an environment variable.

4. `token`: This line retrieves the API token from an environment variable.

5. `headers`: This line sets up the headers for the API requests. The Authorization header 
   is set to "Bearer {token}", where "{token}" is the API token retrieved earlier.

6. `MIN_BID`: This line sets a constant for the minimum bid amount.
"""

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'filelog.log')

logging.basicConfig(filename=filename,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


API_BASE_URL = os.getenv('API_BASE_URL')

token = os.getenv('TOKEN')

headers = {"Authorization": f"Bearer {token}"}

MIN_BID = 100


def get_auction_by_id(sales_id: int) -> object | None:
    """
    Retrieves details of a specific auction by its ID.

    This function sends a GET request to the API's "/api/sales/{sales_id}" endpoint, 
    passing the sales ID as a parameter. The function returns the 
    JSON response from the API if the request is successful, and None otherwise.

    The function also logs the JSON response from the API for debugging purposes.

    Args:
        sales_id (int): The ID of the auction to retrieve.

    Returns:
        object: The JSON response from the API, containing the details of the auction, 
        if the request is successful.
        None: If the request is not successful.
    """
    response = requests.get(f"{API_BASE_URL}/api/sales/{sales_id}",
                            headers=headers)

    if response.status_code == 200:
        logging.info(response.json())
        return response.json()
    return None


def bid_to_auction(auction_id: str, amount: int) -> object | None:
    """
    Places a bid on a specific auction.

    This function sends a POST request to the API's "/api/sales/{auction_id}/bids" endpoint, 
    passing the auction ID and the bid amount as parameters. The function returns the 
    JSON response from the API if the request is successful, and None otherwise.

    The function also logs the JSON response from the API for debugging purposes.

    Args:
        auction_id (str): The ID of the auction to bid on.
        amount (int): The amount to be bid.

    Returns:
        object: The JSON response from the API, containing the result of the bid, 
        if the request is successful.
        None: If the request is not successful.
    """
    response = requests.post(f"{API_BASE_URL}/api/sales/{auction_id}/bids",
                             headers=headers, data={"maxAmount": amount})

    if response.status_code == 200:
        logging.info(response.json())
        return response.json()
    elif response.status_code == 422:
        logging.info(response.json())
        return response.json()
    logging.info(response.status_code)
    logging.info(response.json())
    return None


def list_my_bids() -> object | None:
    """
    Retrieves a list of the current user's bids from the API.

    This function sends a GET request to the API's "/api/user/bids" endpoint, 
    passing a specific sale ID as a query parameter. The function returns the 
    JSON response from the API if the request is successful, and None otherwise.

    The function also logs the JSON response from the API for debugging purposes.

    Note: This function is implemented in this way as a practice exercise. It assumes that the sale ID 
    is hard-coded and does not change. In a real-world application, the sale ID might need to be passed 
    as a parameter or retrieved dynamically.

    Returns:
        object: The JSON response from the API, containing a list of the user's bids, 
        if the request is successful.
        None: If the request is not successful.
    """

    # Example sale ID = UNtL5dPLLNLcccqSwUjR2x
    response = requests.get(f"{API_BASE_URL}/api/user/bids?sale=UNtL5dPLLNLcccqSwUjR2x",
                            headers=headers)

    if response.status_code == 200:
        logging.info(response.json())
        return response.json()
    return None


if __name__ == "__main__":
    """
    This block of code performs the following steps:

    1. Retrieves a list of the current user's bids by calling the `list_my_bids` function.

    2. If the `list_my_bids` function returns a non-None result, it checks if the user is 
    currently the leading bidder for the first item in the list.

    3. If the user is the leading bidder, it logs a message and does nothing else.

    4. If the user is not the leading bidder, it retrieves the details of the auction by 
    calling the `get_auction_by_id` function with the sale ID of the first item.

    5. If the auction is active and the minimum bid is less than a predefined constant 
    `MIN_BID`, it places a bid on the auction by calling the `bid_to_auction` function 
    with the auction ID and the current minimum bid plus 1.

    6. If the bid is successful, it checks if the user is now the leading bidder and logs 
    the result. If the bid is not successful due to the maximum bid being below the 
    increment, it extracts the maximum bid amount from the error message, adds 3 to it, 
    and places a new bid with this amount.

    Note: This block of code is implemented in this way as a practice exercise. It assumes 
    that the user only wants to bid on the first item in their list of bids, and that they 
    want to increase their bid by 1 (or by 3 in case of an error) each time. In a real-world 
    application, the logic might need to be adjusted to fit the user's bidding strategy.
    """
    my_bids = list_my_bids()

    if my_bids is not None:
        if my_bids['items'][0]['isLeadingBid']:
            logging.info("Do nothing... I'm the bidder leader")
        else:
            sale_id = my_bids['items'][0]['saleId']
            auction = get_auction_by_id(sale_id)

            if auction["status"] == "active" and auction["minBid"] < MIN_BID:
                bid_to_auction_result = bid_to_auction(
                    auction["id"], auction["minBid"] + 1)
                if bid_to_auction_result is not None:
                    try:
                        if bid_to_auction_result["isLeadingBid"] in bid_to_auction_result:
                            logging.info(bid_to_auction_result)
                    except KeyError as err:
                        logging.error(err)

                    if bid_to_auction_result["code"] == 'ERR_MAX_BID_BELOW_INCREMENT' and bid_to_auction_result["status"] == 422:
                        numbers = re.findall(
                            r'\d+', bid_to_auction_result["message"])
                        max_bid_amount_to_beat = int(max(numbers))
                        bid_to_auction_result = bid_to_auction(
                            auction["id"], max_bid_amount_to_beat + 3)
                        logging.info(bid_to_auction_result)
