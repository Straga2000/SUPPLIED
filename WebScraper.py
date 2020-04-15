import requests
from bs4 import BeautifulSoup

URL = 'https://www.cora.ro/search?categoryId=&queryStr=iaurt'
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')
#title = soup.find(id="product-details").get_text()
#price = soup.find(class="price").get_text()
#print(title.strip())

urls = []
urls = soup.find_all('span')
for obj in urls:
    try:
        link = obj.attrs['class']
        if link=='price':
            print(obj)

    except:
        print("Nu are link!")
#print(urls)