import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import hashlib
import base64
from icecream import ic

# Load the environment variables from .env file
load_dotenv()

# Get the secret key from the .env file
SECRET_KEY = os.getenv("JWT_ENCRYPTION_KEY")


# Function to generate a key from the secret
def generate_key(secret):
    # Hash the secret to ensure it's 32 bytes long (Fernet requires 32 bytes)
    key = hashlib.sha256(secret.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


# Encrypt the JWT token
def encrypt_jwt(token):
    try:
        fernet = generate_key(SECRET_KEY)
        encrypted_token = fernet.encrypt(token.encode())
        # Convert encrypted bytes to a Base64 encoded string
        return base64.urlsafe_b64encode(encrypted_token).decode()
    except Exception as e:
        ic("Encryption failed", e)
        return None


# Decrypt the JWT token
def decrypt_jwt(encrypted_token):
    try:
        fernet = generate_key(SECRET_KEY)
        # Decode the Base64 encoded string back to bytes before decryption
        encrypted_token_bytes = base64.urlsafe_b64decode(encrypted_token.encode())
        decrypted_token = fernet.decrypt(encrypted_token_bytes).decode()
        return decrypted_token
    except Exception as e:
        ic("Decryption failed", e)
        return None


if __name__ == "__main__":
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwiZXhwIjoxNzI1OTgwNzE4fQ.oqkean7Gb83MlLIoGrfhvdmliZRYo2h9SZus1RxdXEE"

    encrypted = encrypt_jwt(jwt_token)
    print(encrypted)
    decrypted = decrypt_jwt(encrypted)
    print(decrypted)
