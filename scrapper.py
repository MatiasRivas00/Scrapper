import requests
from bs4 import BeautifulSoup
from lxml import etree

class Scrapper:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.get("https://si3.bcentral.cl/Bdemovil/BDE/IndicadoresDiarios")
    def get_html(self, date: str) -> str:
        """
        Return html from si3.bcentral.cl that show prices in date

        Parameters:
            date (string) : date in day-month-year format
        Return:
            a response object
        """
        URL = f"https://si3.bcentral.cl/Bdemovil/BDE/IndicadoresDiarios?parentMenuName=Indicadores%20diarios&fecha={date}"
        response = self.session.get(URL)

        if response.status_code == 200:
            return response
        else:
            print(f"Error: there was a problem with GET request, status code = {response.status_code}")
    
    def get_prices(self, html):
        """
        Get the prices from banco central table

        Parameters:
            html: html content from banco central response
        Returns
            a dictionary with all the prices
        """
        soup = BeautifulSoup(html, 'html.parser')
        dom = etree.HTML(str(soup))
        TABLE_XPATH = '//*[@id="main"]/div/div/div/div[2]'
        VALUE_XPATH = 'tbody/tr/td[2]/p'
        get_price = lambda table: eval(dom.xpath(f'{TABLE_XPATH}/{table}/{VALUE_XPATH}')[0].text.replace(',', '').replace('-', '0'))

        return {
        "uf_price" :                get_price("table[1]"),
        "dollar_price" :            get_price("table[2]"),
        "euro_prince" :             get_price("table[3]"),
        "euro_per_dollar" :         get_price("table[4]"),
        "copper_price_per_libra" :  get_price("table[5]"),
        "gold_price_per_ozt" :      get_price("table[6]")
        }