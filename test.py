from scrapper import Scrapper
import pandas as pd
import sqlite3


scr = Scrapper()
response = scr.get_html("31-12-2022")
prices = scr.get_prices(response.content)

dict = {}
print(prices)
