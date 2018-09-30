import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

class get_from_gasbuddy():

    def __init__(self, address, fuel_type):
        self.fuel_type = fuel_type
        self.address = address


    def get_html(self,page):
        """
        To avoid of any other characters in url, transform them into utf-8
        :param url: target url
        :return: html text file
        """
        url = 'https://www.gasbuddy.com/home?search=urbana&fuel={}&cursor={}'.format(self.fuel_type,page)

        try:
            r = requests.get(url, timeout = 30)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text

        except:
            return 'ERROR1'

    def get_content(self):

        pages = [10,20,30,40]
        names = []
        adds = []
        prices = []
        for page in pages:
            html = self.get_html(page)
            soup = BeautifulSoup(html, 'lxml')

            names_html = soup.find_all('h3', class_='style__header3___3T2tm style__header___onURp style__snug___2HJ4K styles__stationNameHeader___24lb3')
            names.extend([name.text for name in names_html])
            adds_html = soup.find_all('div', class_='styles__address___8IK98')
            adds.extend(['{}, {}'.format(add.contents[0], add.contents[2]) for add in adds_html])
            prices_html = soup.find_all('span', class_='styles__price___3DxO5')
            prices.extend([float(price.text[1:5]) for price in prices_html])

        return pd.DataFrame({'names':names, 'adds':adds, 'price':prices})

    def get_price(self):
        dt = self.get_content()
        print(dt)
        price = dt.loc[dt.adds == self.address, 'price']
        print(price)
        return price



if '__main__' == __name__:

    data = pd.read_csv('./data/address_location.csv')
    add_zip = pd.DataFrame()
    add_zip['address'] = [' '.join(dat['Address'].split(' ')[0:-2]) for ind, dat in data.iterrows()]
    add_zip['zipCode'] = [dat['Address'].split(' ')[-2] for ind, dat in data.iterrows()]

    test = random.randint(0, add_zip.shape[0])
    zip_code = add_zip.loc[test,'zipCode']
    add = add_zip.loc[test, 'address']

    print(add)
    get = get_from_gasbuddy(address=add, fuel_type=1)
    gb = get.get_content()
    print(gb.loc[gb.adds == add,'price'])
