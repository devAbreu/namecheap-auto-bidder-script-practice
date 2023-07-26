# Namecheap Aftermarket Customer API Practice Script

This repository contains a Python script that I created to practice interacting with the [Namecheap Aftermarket Customer API](https://www.namecheap.com/support/knowledgebase/article.aspx/10522/15/auctions-bidding-guide/#api). The script automates the process of bidding on auctions.

## Description

The `main.py` script performs the following actions:

1. Retrieves a list of the current user's bids.
2. If the user is not the leading bidder in the first auction on the list, it retrieves the details of the auction.
3. If the auction is active and the minimum bid is less than a predefined amount, it places a bid on the auction.
4. If the bid is successful, it checks if the user is now the leading bidder.
5. If the bid is not successful because the maximum bid is below the increment, it extracts the maximum bid amount from the error message, adds 3 to it, and places a new bid with this amount.

This script was created as a practice exercise to learn how to interact with APIs using Python.

## Usage

To use this script, you will need to have Python installed on your machine and you will also need to install the dependencies listed in the `requirements.txt` file.

To run the script, you can use the following command:

```
python main.py
```

## Automatic Execution with Crontab

This script can be set up to run automatically at regular intervals using crontab. The following line can be added to your crontab file to run the script every 2 hours:

```
0 */2 * * * /<path>/env/bin/python /<path>/main.py
```

In this line, `/<path>/env/bin/python` should be replaced with the full path to the Python executable in your virtual environment, and `/<path>/main.py` should be replaced with the full path to the `main.py` script. The interval at which the script runs can be adjusted as needed.

## Environment Variables

This script uses the following environment variables:

- `API_BASE_URL`: The base URL of the API.
- `TOKEN`: The API token.

You can set these environment variables in your `.env` file.

## Author

This script was created by [devAbreu](https://github.com/devAbreu) as a practice exercise.
