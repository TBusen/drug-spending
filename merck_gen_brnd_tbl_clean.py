from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd


## runs in python 3.5
## need to download the chromium webdriver
## reference the location of the executable
## https://sites.google.com/a/chromium.org/chromedriver/
path_to_chromedriver = '/Users/Travis/webDrivers/chromedriver'
chrome = webdriver.Chrome(path_to_chromedriver)
## set windows size so it doesn't open in mobile version of set
# if opens in mobile site then you need to search for a different set of attributes
chrome.set_window_size(1600, 1600)
## the root site
chrome.get('http://www.merckmanuals.com/professional')
## drug name link doesn't become active until you hover over the menu.  This is the class to hover over
element_to_hover_over = chrome.find_element_by_xpath("//li[@class='item2 itemEdge main-menu-item leftSide ']")
## Perform the hover to expose the link
ActionChains(chrome).move_to_element(element_to_hover_over).perform()
## without the sleep you don't see the link, it loads too slow for the script
time.sleep(4)
## click on the link, find it by link name in the span tag
chrome.find_element_by_link_text('Drugs by Name, Generic and Brand').click()

# get the html of the current page
url = chrome.page_source
# do some magic
soup = BeautifulSoup(url)



##### Base xref table scraping #####

# find start of table
table_start = soup.find(class_="drugDrugTitleTrade drug-table")
# get list of drug names from table body
# generic and name brand drugs are listed by their html class
generic_name_drugs = table_start.table.tbody.find_all(class_='LexicompLink_active')
brand_name_drugs = table_start.table.tbody.find_all(class_='w-border')

data = []

# create list of dictionaries for each row
for i in range(len(generic_name_drugs)):
    data.append({table_start.table.thead.th.get_text():generic_name_drugs[i].get_text(),
                 table_start.table.thead.find(class_='w-border').get_text():brand_name_drugs[i].get_text()})

# clean up the text
def initcap(text):
    return text.str.title()

# convert to DataFrame then exort to CSV
df = pd.DataFrame(data).apply(initcap)

df.to_csv('/Users/Travis/Downloads/merck_gen_brnd_table_scrape.csv',header=True,index=False,sep='|')


#####################################

##### Generic drug pop up scraping #####

chrome.find_element_by_xpath("//tbody/tr/td").click()

for i in WebDriverWait(chrome, 6).until(EC.visibility_of_element_located((By.CLASS_NAME, 'lexi-main'))).find_elements_by_xpath("//p"):
    print(i.text)
