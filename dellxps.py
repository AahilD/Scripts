import requests
from bs4 import BeautifulSoup

URL = "https://www.dell.com/en-ca/shop/dell-laptops/xps-13-laptop/spd/xps-13-9300-laptop"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

price = 0
for span in soup.find_all("span", {"class": "ps-simple-dell-price"}):
    print(span.getText())
