from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_token(token: str, key: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CFB8(key[:16]))
    encryptor = cipher.encryptor()
    encrypted_token = encryptor.update(token.encode()) + encryptor.finalize()
    return encrypted_token


def decrypt_token(encrypted_token: bytes, key: bytes) -> str:
    cipher = Cipher(algorithms.AES(key), modes.CFB8(key[:16]))
    decryptor = cipher.decryptor()
    decrypted_token = decryptor.update(encrypted_token) + decryptor.finalize()
    return decrypted_token.decode()
