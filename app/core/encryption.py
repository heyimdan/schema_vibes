import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional
from loguru import logger


class EncryptionService:
    """Service for encrypting and decrypting sensitive data like API keys."""
    
    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize the encryption service.
        
        Args:
            master_key: Master key for encryption. If not provided, will try to get from environment.
        """
        self.master_key = master_key or os.environ.get("SCHEMA_VALIDATOR_MASTER_KEY")
        if not self.master_key:
            # Generate a new master key if none exists
            self.master_key = self._generate_master_key()
            logger.warning("No master key found, generated a new one. Please store it securely!")
            logger.info(f"Generated master key: {self.master_key}")
        
        self._fernet = self._create_fernet_key()
    
    def _generate_master_key(self) -> str:
        """Generate a new master key."""
        return base64.urlsafe_b64encode(os.urandom(32)).decode()
    
    def _create_fernet_key(self) -> Fernet:
        """Create a Fernet encryption key from the master key."""
        # Use PBKDF2 to derive a key from the master key
        master_key_bytes = self.master_key.encode()
        salt = b"schema_validator_salt"  # In production, use a random salt stored securely
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key_bytes))
        return Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext string.
        
        Args:
            plaintext: The string to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        try:
            encrypted_bytes = self._fernet.encrypt(plaintext.encode())
            return base64.urlsafe_b64encode(encrypted_bytes).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            raise
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt an encrypted string.
        
        Args:
            encrypted_text: Base64 encoded encrypted string
            
        Returns:
            Decrypted plaintext string
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode())
            decrypted_bytes = self._fernet.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            raise
    
    def encrypt_api_key(self, api_key: str) -> str:
        """
        Encrypt an API key.
        
        Args:
            api_key: The API key to encrypt
            
        Returns:
            Encrypted API key with prefix for identification
        """
        encrypted = self.encrypt(api_key)
        return f"encrypted:{encrypted}"
    
    def decrypt_api_key(self, encrypted_api_key: str) -> str:
        """
        Decrypt an API key.
        
        Args:
            encrypted_api_key: The encrypted API key (with or without prefix)
            
        Returns:
            Decrypted API key
        """
        # Remove prefix if present
        if encrypted_api_key.startswith("encrypted:"):
            encrypted_api_key = encrypted_api_key[10:]
        
        return self.decrypt(encrypted_api_key)
    
    def is_encrypted(self, value: str) -> bool:
        """
        Check if a value is encrypted.
        
        Args:
            value: The value to check
            
        Returns:
            True if the value appears to be encrypted
        """
        return value.startswith("encrypted:")


# Global encryption service instance
_encryption_service: Optional[EncryptionService] = None


def get_encryption_service() -> EncryptionService:
    """Get the global encryption service instance."""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service


def encrypt_api_key(api_key: str) -> str:
    """Convenience function to encrypt an API key."""
    return get_encryption_service().encrypt_api_key(api_key)


def decrypt_api_key(encrypted_api_key: str) -> str:
    """Convenience function to decrypt an API key."""
    return get_encryption_service().decrypt_api_key(encrypted_api_key)


def is_encrypted(value: str) -> bool:
    """Convenience function to check if a value is encrypted."""
    return get_encryption_service().is_encrypted(value) 