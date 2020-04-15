import requests
from bs4 import BeautifulSoup

URL = 'https://carrefour.ro/it-c/telefoane-tablete-gadget-uri/telefonie-fixa-si-teleconferinta'
content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser')

elem = soup.find_all("span", class_="price")
price_list =[]
for it in elem:
    pret = it.get_text().strip()
    pret = pret.replace(',','.')
    converted_pret = float(pret[:-4])
    price_list.append(converted_pret)
print(price_list)
print(min(price_list))


