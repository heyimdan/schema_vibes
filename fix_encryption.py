#!/usr/bin/env python3
"""
Script to re-encrypt OpenAI API key with the correct master key
"""
import os
import sys

# Set the correct master key that's on Render
os.environ['SCHEMA_VALIDATOR_MASTER_KEY'] = '1pfQUrO6gXjTc95uvcMI9tGyxAHP85JmTk-xQm08ons='

from app.core.encryption import encrypt_api_key

def main():
    print("=== OpenAI API Key Re-encryption ===")
    print("This will re-encrypt your API key with the correct master key")
    print()
    
    # Get the real API key
    real_api_key = input("Enter your actual OpenAI API key (starts with sk-): ").strip()
    
    if not real_api_key or not real_api_key.startswith('sk-'):
        print("❌ Invalid API key format. Should start with 'sk-'")
        sys.exit(1)
    
    try:
        # Encrypt with the correct master key
        encrypted_key = encrypt_api_key(real_api_key)
        
        print()
        print("✅ Successfully encrypted!")
        print()
        print("🔑 Use this encrypted API key on Render:")
        print("Environment Variable: OPENAI_API_KEY")
        print("Value:")
        print(encrypted_key)
        print()
        print("📝 Copy the value above and update your Render environment variables")
        
    except Exception as e:
        print(f"❌ Encryption failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 