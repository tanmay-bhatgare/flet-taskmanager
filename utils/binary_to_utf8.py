import base64
from dotenv import load_dotenv
import os

load_dotenv()

encoded_data = os.getenv("JWT_ENCRYPT_KEY_ENCODED")

def decode_to_binary():
    binary_data = base64.b64decode(encoded_data.encode("utf-8"))
    return binary_data