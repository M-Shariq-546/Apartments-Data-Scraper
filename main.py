from bs4 import BeautifulSoup as bs4
import requests
from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

url = "https://www.pararius.com/apartment-for-rent/amsterdam"
DRIVER_PATH = "C:\Chromedriver\chromedriver.exe"

options = Options()
options.headless = True

driver = webdriver.Chrome(service=Service(DRIVER_PATH),options=options)
driver.get(url)

html = driver.page_source
soup = bs4(html,'html.parser')

def getData():
    lists = soup.find_all('section' , class_ = "listing-search-item")

    information = []
    
    for list in lists:
        title = list.find('h2' ,
                class_="listing-search-item__title").text.replace('\n' , '')
        location = list.find('div' ,
                class_="listing-search-item__sub-title").text.replace('\n' , '')
        price = list.find('div' ,
                class_="listing-search-item__price").text.replace('\n' , '')
        #price_per_month = list.find('span' , class_="listing-detail-summary__price-postfix").text.replace('\n' , '')
        area = list.find('li' ,
                class_="illustrated-features__item illustrated-features__item--surface-area").text.replace('\n' , '')
        rooms = list.find('li' , 
                class_="illustrated-features__item illustrated-features__item--number-of-rooms").text.replace('\n' , '')
        info = [title.strip(),
                location.strip(),
                price.strip().split(" per")[0],
                area.strip(),
                str(rooms.strip().split(" rooms")[0])
               ]
        information.append(info.copy())
    return information

with open('Apartments.csv' , 'w' , encoding='utf8' , newline='') as file:
    thewriter = writer(file)
    header = ['Title' , 'Location' , 'Price' , 'Price Method'  , 'Number of Rooms']
    thewriter.writerow(header)
    
    lists = getData()
    for list in lists:
        thewriter.writerow(list)
