"""
Encryption Key Generator
------------------------
Utility script to generate a secure encryption key for API key storage.

Run this script to generate a new encryption key:
    python -m app.db_utils.generate_encryption_key

Copy the output to your .env file as ENCRYPTION_KEY.
"""

from cryptography.fernet import Fernet


def generate_key():
    """
    Generate a new Fernet encryption key.
    
    This key should be stored securely in environment variables
    and NEVER committed to version control.
    """
    key = Fernet.generate_key()
    
    print("\n" + "="*60)
    print("🔐 Encryption Key Generator")
    print("="*60 + "\n")
    print("Generated Encryption Key:")
    print(f"\n{key.decode()}\n")
    print("="*60)
    print("\n⚠️  IMPORTANT SECURITY NOTES:")
    print("   1. Copy this key to your .env file as ENCRYPTION_KEY")
    print("   2. NEVER commit this key to version control")
    print("   3. Keep this key secure and backed up")
    print("   4. Generate a new key for each environment")
    print("   5. If key is lost, all encrypted API keys are unrecoverable")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    generate_key()