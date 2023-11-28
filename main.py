import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

def get_title(soup):
    try:
        # outertag
        title = soup.find("span", attrs={'id':'productTitle'})
        # inner navigatablestring
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    
    return title_string

def get_price(soup):
    try:
        price = soup.find('span', attrs={'class':'a-offscreen'}).text
    except AttributeError:
        price = "N/A"
    
    return price

def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'id':'acrCustomerReviewText'}).text
    except AttributeError:
        rating = 'No reviews yet.'
    
    return rating

URL = 'https://www.amazon.com/s?k=headphones&crid=7VISOETH51V&sprefix=headphone%2Caps%2C499&ref=nb_sb_noss_2'
HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

page = requests.get(URL, headers= HEADERS)
print(page)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
links = soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
print(links)
links_list = []

for link in links:
    links_list.append(link.get('href'))

print(links_list)

d = {
    "title":[],
    "price": [],
    "rating": []
}

for link in links_list:
    if not link.startswith(('http://', 'https://')):
        link = 'https://www.amazon.com' + link
    new_page = requests.get(link, headers=HEADERS)
    new_soup = BeautifulSoup(new_page, 'html.parser')

    d['title'].append(get_title(new_soup))
    d['price'].append(get_price(new_soup))
    d['rating'].append(get_rating(new_soup))

print(d)

amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'].replace('', np.nan, inplace= True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)
