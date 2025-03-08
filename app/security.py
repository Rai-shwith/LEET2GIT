from cryptography.fernet import Fernet
from app.config import settings

KEY = settings.encryption_key
SALT = settings.encryption_salt

def encrypt_token(token: str) -> str:
    """Encrypt the GitHub token with the given key and salt."""
    f = Fernet(KEY)
    token_with_salt = token + SALT
    encrypted_token = f.encrypt(token_with_salt.encode())
    return encrypted_token.decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt the encrypted token and verify the salt."""
    f = Fernet(KEY)
    decrypted_token_with_salt = f.decrypt(encrypted_token.encode()).decode()
    
    if not decrypted_token_with_salt.endswith(SALT):
        raise ValueError("Invalid token or salt")
    
    return decrypted_token_with_salt[:-len(SALT)]
