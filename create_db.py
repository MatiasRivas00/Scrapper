from datetime import datetime, timedelta
from scrapper import Scrapper
import pandas as pd
import sqlite3

# Constants
DATE_FORMAT = "%d-%m-%Y"
sp = Scrapper()

# Date Inputs
init_date = input("Ingresa la fecha inicial en formato dd-mm-aaaa (ej: 25-12-2022): ")
end_date = input("Ingresa la fecha final en formato dd-mm-aaaa (ej: 25-12-2022): ")

# Dates Validation
try:
    init_date = datetime.strptime(init_date, DATE_FORMAT)
    end_date = datetime.strptime(end_date, DATE_FORMAT)
except:
    print("Error: fecha en formato correcto")
    exit()

# Initializing Variables
curr_date = init_date
one_day = timedelta(days=1)
prices_by_date = {}

# Collecting Prices Data
while curr_date != end_date:
    str_curr_date = curr_date.strftime(DATE_FORMAT)
    response = sp.get_html(str_curr_date)
    prices = sp.get_prices(response.content)
    prices_by_date[str_curr_date] = prices

    curr_date += one_day

# Creating Database From DataFrame
df = pd.DataFrame.from_dict(prices_by_date, orient="index")
df.index.name = "date"

con = sqlite3.connect("prices_history.db")
cur = con.cursor()

df.to_sql("prices_history", con, if_exists="replace", index=True, index_label="date")

# Visualizing Result
for row in cur.execute('SELECT * FROM prices_history;'):
    print(row)

# Closing Database Connection
con.close()