from bs4 import BeautifulSoup
import requests
from csv import writer


url = "https://www.pararius.com/apartment-for-rent/amsterdam"

page = requests.get(url)

soup = BeautifulSoup(page.content , 'html.parser')

lists = soup.find_all('section' , class_ = "listing-search-item")


with open('Apartments.csv' , 'w' , encoding='utf8' , newline='') as file:
    thewriter = writer(file)
    header = ['Title' , 'Location' , 'Price' , 'Price Method'  , 'Number of Rooms']
    thewriter.writerow(header)
    
    for list in lists:
        title = list.find('h2' , class_="listing-search-item__title").text.replace('\n' , '')
        location = list.find('div' , class_="listing-search-item__sub-title").text.replace('\n' , '')
        price = list.find('div' , class_="listing-search-item__price").text.replace('\n' , '')
        #price_per_month = list.find('span' , class_="listing-detail-summary__price-postfix").text.replace('\n' , '')
        area = list.find('li' , class_="illustrated-features__item illustrated-features__item--surface-area").text.replace('\n' , '')
        rooms = list.find('li' , class_="illustrated-features__item illustrated-features__item--number-of-rooms").text.replace('\n' , '')
        info = [title, location, price, area, rooms]
        print(info)
        thewriter.writerow(info)