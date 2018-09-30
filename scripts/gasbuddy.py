import requests
from bs4 import BeautifulSoup

class get_from_gasbuddy:

    def __init__(self, zip_code, fuel_type):
        """
        :param zip_code: 5 digit zip code
        :param fuel_type:  {1:'regular', 2:'midgrade', 3:'premium', 4:'diesel'}
        """

        self.zip_code = zip_code
        self.fuel_type = fuel_type

    def get_html(self):
        """
        To avoid of any other characters in url, transform them into utf-8
        :param url: target url
        :return: html text file
        """
        url = 'https://www.gasbuddy.com/home?search={}&fuel={}'.format(self.zip_code, self.fuel_type)

        try:
            r = requests.get(url, timeout = 30)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text

        except:
            return 'ERROR1'

    def get_content(self):

        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')

        names_html = soup.find_all('h3', class_='style__header3___3T2tm style__header___onURp style__snug___2HJ4K styles__stationNameHeader___24lb3')
        names = [name.text for name in names_html]
        adds_html = soup.find_all('div', class_='styles__address___8IK98')
        adds = ['{}, {}'.format(add.contents[0], add.contents[2]) for add in adds_html]
        prices_html = soup.find_all('span', class_='styles__price___3DxO5')
        prices = [float(price.text[1:5]) for price in prices_html]

        for i in range(0,len(prices)):
            print("Station Name: ", names[i], 'Address: ', adds[i], 'Price: ', prices[i])

get = get_from_gasbuddy(zip_code=61801, fuel_type=1)
get.get_content()

