#!/usr/bin/env python3
"""
Utility script to encrypt API keys for secure deployment.

This script helps you:
1. Encrypt your current API keys
2. Generate a master key for encryption
3. Create environment configuration for production deployment

Usage:
    python encrypt_api_key.py
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.encryption import EncryptionService, encrypt_api_key


def main():
    print("🔐 Schema Validator Encryption Utility")
    print("=" * 50)
    
    # Check if we have an existing API key
    current_openai_key = os.environ.get("OPENAI_API_KEY")
    
    if current_openai_key:
        print(f"✅ Found OpenAI API key in environment: {current_openai_key[:15]}...")
    else:
        print("❌ No OpenAI API key found in environment")
        current_openai_key = input("Please enter your OpenAI API key: ").strip()
        if not current_openai_key:
            print("❌ No API key provided. Exiting.")
            return
    
    # Ask about admin password
    print("\n🛡️  Admin Password Configuration")
    admin_password = input("Enter admin password (default: 'secret'): ").strip()
    if not admin_password:
        admin_password = "secret"
    
    # Initialize encryption service (this will generate a master key if none exists)
    print("\n🔑 Initializing encryption service...")
    encryption_service = EncryptionService()
    
    # Encrypt the API key and admin password
    print("🔒 Encrypting API key...")
    encrypted_key = encryption_service.encrypt_api_key(current_openai_key)
    
    print("🔒 Encrypting admin password...")
    encrypted_admin_password = encryption_service.encrypt_api_key(admin_password)
    
    print("\n✅ Encryption completed!")
    print("=" * 50)
    print("📋 DEPLOYMENT CONFIGURATION")
    print("=" * 50)
    
    print("\n1. MASTER KEY (Store this securely!):")
    print("   Set this as environment variable: SCHEMA_VALIDATOR_MASTER_KEY")
    print(f"   Value: {encryption_service.master_key}")
    
    print("\n2. ENCRYPTED API KEY:")
    print("   Use this in your configuration file or environment:")
    print(f"   OPENAI_API_KEY={encrypted_key}")
    
    print("\n3. ENCRYPTED ADMIN PASSWORD:")
    print("   Use this in your configuration file or environment:")
    print(f"   ADMIN_PASSWORD={encrypted_admin_password}")
    
    # Create .env.production file
    env_production_content = f"""# Production Environment Configuration for Schema Validator
# =======================================================

# Master key for decrypting API keys (CRITICAL - STORE SECURELY!)
SCHEMA_VALIDATOR_MASTER_KEY={encryption_service.master_key}

# Encrypted API Keys
OPENAI_API_KEY={encrypted_key}

# Encrypted Admin Password
ADMIN_PASSWORD={encrypted_admin_password}

# Application Configuration
AI_PROVIDER=openai
GPT_MODEL=gpt-4o-mini
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8000

# Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
DATABASE_URL=sqlite:///./schema_validator.db

# Logging
LOG_LEVEL=INFO
"""
    
    with open(".env.production", "w") as f:
        f.write(env_production_content)
    
    print("\n3. PRODUCTION ENVIRONMENT FILE:")
    print("   Created: .env.production")
    print("   This file contains your encrypted configuration.")
    
    # Create deployment instructions
    deployment_instructions = """# Schema Validator Deployment Instructions

## Secure Credential Configuration

Your API keys and admin password have been encrypted for secure deployment. Follow these steps:

### 1. Environment Variables for Production

Set these environment variables on your production server:

```bash
export SCHEMA_VALIDATOR_MASTER_KEY="{master_key}"
export OPENAI_API_KEY="{encrypted_key}"
export ADMIN_PASSWORD="{encrypted_admin_password}"
```

### 2. Docker Deployment

If using Docker, add these to your docker-compose.yml:

```yaml
version: '3.8'
services:
  schema-validator:
    build: .
    environment:
      - SCHEMA_VALIDATOR_MASTER_KEY={master_key}
      - OPENAI_API_KEY={encrypted_key}
      - ADMIN_PASSWORD={encrypted_admin_password}
      - AI_PROVIDER=openai
      - DEBUG=false
    ports:
      - "8000:8000"
```

### 3. Security Best Practices

1. **Never commit the master key to version control**
2. **Store the master key in a secure secret management system**
3. **Use different master keys for different environments**
4. **Rotate keys periodically**

### 4. Environment-Specific Configuration

- **Development**: Use unencrypted keys in `.env` (not committed)
- **Staging**: Use encrypted keys with staging master key
- **Production**: Use encrypted keys with production master key

### 5. Key Rotation

To rotate your API key:
1. Get new API key from OpenAI
2. Run this encryption script again
3. Update environment variables with new encrypted key
4. Deploy updated configuration

## Testing Encrypted Configuration

You can test your encrypted configuration locally:

```bash
# Set the master key
export SCHEMA_VALIDATOR_MASTER_KEY="{master_key}"

# Set the encrypted API key
export OPENAI_API_KEY="{encrypted_key}"

# Set the encrypted admin password
export ADMIN_PASSWORD="{encrypted_admin_password}"

# Start the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The application will automatically decrypt the credentials at runtime.
""".format(
    master_key=encryption_service.master_key,
    encrypted_key=encrypted_key,
    encrypted_admin_password=encrypted_admin_password
)
    
    with open("DEPLOYMENT_SECURITY.md", "w") as f:
        f.write(deployment_instructions)
    
    print("   Created: DEPLOYMENT_SECURITY.md")
    print("   Contains detailed deployment instructions.")
    
    print("\n⚠️  IMPORTANT SECURITY NOTES:")
    print("   1. Store the master key in a secure location (password manager, secrets vault)")
    print("   2. Never commit the master key to version control")
    print("   3. Use different master keys for different environments")
    print("   4. The encrypted API key is safe to store in configuration files")
    
    # Test decryption
    print("\n🧪 Testing decryption...")
    try:
        decrypted_api_key = encryption_service.decrypt_api_key(encrypted_key)
        decrypted_admin_password = encryption_service.decrypt_api_key(encrypted_admin_password)
        
        api_key_test = decrypted_api_key == current_openai_key
        admin_password_test = decrypted_admin_password == admin_password
        
        if api_key_test and admin_password_test:
            print("✅ API key encryption/decryption test successful!")
            print("✅ Admin password encryption/decryption test successful!")
        else:
            if not api_key_test:
                print("❌ API key encryption/decryption test failed!")
            if not admin_password_test:
                print("❌ Admin password encryption/decryption test failed!")
    except Exception as e:
        print(f"❌ Encryption/decryption test failed: {e}")
    
    print("\n🎉 Setup complete! Your credentials are now encrypted and ready for secure deployment.")


if __name__ == "__main__":
    main() 