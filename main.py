# Code by Kanwar Adnan
# I couldnt find any API or url method so I continued using the worst method i.e webdriver
# pardon me.

from bs4 import BeautifulSoup as bs4
from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DRIVER_PATH = "C:\Chromedriver\chromedriver.exe"
url = "https://www.pararius.com/english"

class Browser:
    def __init__(self, driver_path , url):
        self.driver_path = driver_path
        self.url = url
        self.options = Options()
        self.options.headless = False

        self.driver = webdriver.Chrome(
            service = Service(self.driver_path),
            options = self.options)

        self.delay = 60
        self.first = True
        
        self.setup_browser()
        
    def setup_browser(self):
        self.driver.get(self.url)
        # Waiting for the website to load as it takes upto 5seconds to load
        try:
            myElem = WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'autocomplete__input')
                )
            )
        except TimeoutException:
            print("Loading took too much time!")
        except:
            return False
        else:
            if self.first:
                # Trying to accept the cookies in case they ask
                try:
                    myElem = WebDriverWait(self.driver, self.delay).until(
                        EC.element_to_be_clickable(
                            (By.ID,'onetrust-accept-btn-handler')
                        )
                    )
                except:
                    pass
                else:
                    self.driver.find_element(
                        By.ID,'onetrust-accept-btn-handler').click()
                    self.first = False
                    return True
        return True

    def get_next_link(self):
        try:
            next_page = self.driver.find_element(By.CLASS_NAME , 'pagination__link--next')
            next_link = next_page.get_property('href')
        except:
            next_link = None
        finally:
            return next_link
    
    def get_html(self, search):
        # if everything was fine we are going to search and return html
        self.driver.find_element(
            By.CLASS_NAME , 'autocomplete__input').clear()    
        self.driver.find_element(
            By.CLASS_NAME , 'autocomplete__input').send_keys(search)
        self.driver.find_element(
            By.NAME , 'search').click()
        html = self.driver.page_source
        next_link = self.get_next_link()
        return html , next_link

        
    def get_url(self , url):
        self.driver.get(url)
        next_link = self.get_next_link()
        return self.driver.page_source , next_link
    

class DataProcessor:
    def __init__(self):
        pass

    def process_data(self, html):
        soup = bs4(html,'html.parser')
        content = soup.find('ul' , {"data-controller":"search-list"})
        sections = content.findAll('section')

        information = []
        for section in sections:
            divs = section.findAll('div')
            temp = divs[5].text.strip().split('\n')
            info = {
                'title' : section.find('h2').text.strip(),
                'location' : divs[3].text.strip(),
                'price' : divs[4].text.strip().split(' ')[0],
                'surface' : temp[0].strip(),
                'rooms' : temp[1].split('rooms')[0].strip(),
                'interior' : temp[2].strip(),
            }
            information.append(info)

        return information
    
    def write_data(self , information: list):
        with open(f'Results.csv' , 'a',newline='') as file:
            thewriter = writer(file)
            header = list(information[0].keys())
            thewriter.writerow(header)

            for info in information:
                info = list(info.values())
                thewriter.writerow(info)
                
                
class Fetcher:
    def __init__(self , driver_path , url , search):
        self.driver_path = driver_path
        self.url = url
        self.search = search
        self.html = None
        self.next_url = None
        
        self.browser = Browser(self.driver_path , self.url)
        self.data_processor = DataProcessor()

    def get_html(self , search):
        if self.url:
            self.html , self.next_url = self.browser.get_html(search)
            return self.html
    
    def get(self):
        if self.next_url:
            self.html , self.next_url = self.browser.get_url(self.next_url)
            return self.html
        else:
            return self.get_html(self.search)
        
    def get_data(self):
        if self.html:
            return self.data_processor.process_data(self.html)
    
    def write_data(self):
        if self.html:
            data = self.get_data()
            return self.data_processor.write_data(data)
        
if __name__ == "__main__":
    search = "Nederland"
    fetcher = Fetcher(DRIVER_PATH , url , search)
    fetcher.get()
    data = fetcher.get_data()
    print(data)
# You can call fetcher.get() method infinite times to get results of next pages as well
# developer Kanwar Adnan , kanwaradnanrajput@gmail.com
