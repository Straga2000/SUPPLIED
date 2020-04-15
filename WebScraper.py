import requests
import smtplib
from bs4 import BeautifulSoup

URL = 'https://carrefour.ro/it-c/telefoane-tablete-gadget-uri/telefonie-fixa-si-teleconferinta'

content = requests.get(URL)
soup = BeautifulSoup(content.text, 'html.parser')
#
# elem = soup.find_all("span", class_="price", recursive=True)
# price_list =[]
# for it in elem:
#     pret = it.get_text().strip()
#     pret = pret.replace(',','.')
#     converted_pret = float(pret[:-4])
#     price_list.append(converted_pret)
# print(price_list)
# print(min(price_list))

result = []

def find_all_objects(soup, tagType, attr, attrValue):
    elements = soup.find_all()

    if len(elements) == 0:
        result.append(soup.text)

    for elem in elements:
        try:
            if elem.name == tagType:
                #print(elem)
                if elem.get(attr) is not None:
                    for attribute in elem[attr]:
                        if attribute == attrValue:
                            find_all_objects(elem, tagType, attr, attrValue)
                # if elem.attrs.get(attr) is not None or attr is None:
                #     if elem.attrs.get(attr) == attrValue or attrValue is None:
                #         result.append(elem.string)
        except:
            print("Nu e afisabil")


find_all_objects(soup, "span", "class", "price")

minim = None
for elem in result:

    pret = elem.strip()
    pret = pret.replace(',','.')
    pret = float(pret[:-4])

    if minim is None:
        minim = pret
    elif minim > pret:
        minim = pret


print(minim)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('food.tracker.prices@gmail.com','mqgjzndoxjhmlzbk')
    subject = 'Smallest price'
    body = 'Check the link: '
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'food.tracker.prices@gmail.com',
        'mihai.bulaceanu@gmail.com',
        msg
    )
    print('SENT')

    server.quit()

send_mail()
