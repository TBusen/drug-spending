from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd


## runs in python 3.5
## need to download the chromium webdriver
## reference the location of the executable
## https://sites.google.com/a/chromium.org/chromedriver/
path_to_chromedriver = '/Users/Travis/chromedriver'
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

text = soup.get_text()

# find block of text where drug names are stored

def find_drug_text(string,keyword):
    cleaned_temp = []
    beg_table = string[string.find(keyword)+11:]
    all_drugs = beg_table[:beg_table.find(keyword)]
    temp = all_drugs.split('\n')

    for i in temp:
        if i != '':
            cleaned_temp.append(i)
    return cleaned_temp

# parse the list into generic and brand key values
def parse_text(somelist):
    lod = []
    for index, name in enumerate(somelist):
        if index == 0 or index % 2 == 0:
            generic = name
        else:
            brand = name
            lod.append({'Generic':generic,'Brand':brand})
    return lod

# write to csv
cleaned_file = parse_text(find_drug_text(text,'BRAND NAMES'))
pd.DataFrame(cleaned_file).to_csv('/Users/Travis/Downloads/merck_gen_brnd_table_scrape.csv',index=False,header=True,sep='|')
