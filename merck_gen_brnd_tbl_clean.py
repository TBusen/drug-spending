from bs4 import BeautifulSoup
import pandas as pd


## downloaded from http://www.merckmanuals.com/professional/appendixes/brand-names-of-some-commonly-used-drugs
url = '~/Downloads/merck_gen_brnd_drug_nms.html'


# strip tags
with open(url,'rb') as f:
    soup = BeautifulSoup(f)
    
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
pd.DataFrame(cleaned_file).to_csv('~/Downloads/merck_gen_brnd_table_scrape.csv',index=False,header=True,sep='|')

        


    