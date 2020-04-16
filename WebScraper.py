import requests
from bs4 import BeautifulSoup
import smtplib

store = ["Emag", "Carrefour", "Auchan"]

def find_minimum(search):

    price = []
    search = search.split()
    length = len(search)

    if length > 1:
        value = ""
        for i in range(length):
            if i == 0:
                value += search[0]
            else:
                value += "+" + search[i]
    else:
        search = search[0]

    #emag

    try:
        URL = "https://www.emag.ro/search/" + search + "?ref=effective_search"
        #"https://www.emag.ro/search/" + search
        content = requests.get(URL)
        soup = BeautifulSoup(content.text, 'html.parser')
        rez = soup.find_all("p", attrs="product-new-price")
        minim = None

        for elem in rez:

            elem = elem.contents

            if len(elem) >= 2:
                fractie = elem[1].text
                pret = float(elem[0].replace(".", "") + "." + fractie)
                #print(pret)

                if minim is None:
                    minim = pret
                elif minim > pret:
                    minim = pret

        if minim is None:
            price.append(0)
        else:
            price.append(minim)
    except:
        price.append(0)

    # carrefour
    URL = "https://carrefour.ro/catalogsearch/result/?q=" + search
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    rez = soup.find_all("span", attrs="price")
    minim = None

    for elem in rez:

        pret = elem.text.strip()
        pret = pret.split("Lei/bucata")[0]
        pret = pret.replace(",", ".")

        try:
            pret = float(pret)

            if minim is None:
                minim = pret
            if minim > pret:
                minim = pret
        except:
            pret = None

    if minim is None:
        price.append(0)
    else:
        price.append(minim)

    #auchan
    URL = "https://www.auchan.ro/store/search/?text=" + search
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    rez = soup.find_all("span")
    attr = "data-price"
    minim = None

    for elem in rez:
        if elem.get(attr) is not None:
            pret = float(elem[attr])

            if minim is None:
                minim = pret
            elif minim > pret:
                minim = pret

    if minim is None:
        price.append(0)
    else:
        price.append(minim)

    #print(*price)

    minim = None

    if minim is None and price[0] != 0:
        minim = price[0]

    if (minim is None or minim > price[1]) and price[1] != 0:
        minim = price[1]

    if (minim is None or minim > price[2]) and price[2] != 0:
        minim = price[2]

    if minim is None:
        return "no", -1
    else:
        for i in range(3):
            if minim == price[i]:
                return store[i], minim


#vec = ['apa', 'vin']

#for obj in vec:
#    print(find_minimum(obj))

def send_mail(input, sender, password, receiver):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, password)

    body = 'Hello!\n'
    subject = 'Smallest price'

    shops = {}

    for obj in input:
        store, minim = find_minimum(obj)

        if shops.get(store) is None:
            shops[store] = []
        shops[store].append((obj, minim))

    for store in shops:
        line  = "\nCheck {0}! This is where you can find the best price ever for:\n\n".format(store)
        for obj in shops[store]:
            line += ">     " + obj[0] + " at the best price of " + str(obj[1]) + "\n"
        body += line

    body += "\nWe have the best price solutions for your budget! Same quality for less! Maximize your satisfaction and save your money!\n\nBest wishes,\nSUPPLIED Team:)"

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail('food.tracker.prices@gmail.com',receiver,msg)
    print('SENT')
    server.quit()


send_mail(["nuci", "calculator", "creioane", "laptop"],'food.tracker.prices@gmail.com', 'mqgjzndoxjhmlzbk', 'alemsb29@gmail.com')
send_mail(["geaca", "laptop", "prune", "masina"],'food.tracker.prices@gmail.com', 'mqgjzndoxjhmlzbk', 'johnny.savu.99@gmail.com')
