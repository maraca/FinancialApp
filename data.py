""" Pulls QUANDL API data and autoloads database """

import json, urllib
import model
from model import Ticker, Price
from datetime import datetime

# FIXME: need to input real tickers in ticker list
ticker_list = ["MX_FB", "MX_COST"]
ticker_url_list = []

def build_ticker_url(ticker_list):
	""" Queries the url using the desired ticker and token"""
	for ticker in ticker_list:
		url = "https://www.quandl.com/api/v1/datasets/YAHOO/"
		token = open("tokens.txt").read()
		ticker_url = url + ticker + ".json?auth_token=" + token
		ticker_url_list.append(ticker_url)
	return ticker_url_list

def load_ticker_data(ticker_url_list, session):
	for ticker_url in ticker_url_list:	
		u = urllib.urlopen(ticker_url)
		data = u.read()
		newdata = json.loads(data)

		# FIXME- "code" pulls the url query, not the actual symbol
		ticker_symbol = newdata["code"]
		ticker_name = newdata["name"]
		
		# prices pulls a list of lists (consisting of date, open, high, 
			# low, close, volume. adjusted close)
		prices = newdata["data"]

		for price in prices:
			date = price[0]
			date_format = datetime.strptime(date, "%Y-%m-%d")
			date_format = date_format.date()
			close_price = price[4]
			new_ticker_price = Price(ticker_symbol=ticker_symbol, 
				date=date_format, close_price=close_price)
			session.add(new_ticker_price)

		# create new instance of the Ticker class called new_ticker
		new_ticker = Ticker(symbol=ticker_symbol, name=ticker_name)
        # add each instance to session
		session.add(new_ticker)
    # commit after all instances are added
	session.commit()


def main(session):
	load_ticker_data(build_ticker_url(ticker_list), session)

if __name__ == "__main__":
    session = model.session
    main(session)
	