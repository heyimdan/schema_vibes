#!/usr/bin/env python3
"""
Direct test of OpenAI API with user's key and GPT-4o-mini
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_openai_direct():
    """Test OpenAI API directly"""
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        import openai
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No OpenAI API key found in .env file")
            return False
            
        print(f"🔑 Using API key: {api_key[:20]}...")
        
        # Create client
        client = openai.OpenAI(api_key=api_key)
        
        # Test simple request
        print("🚀 Testing GPT-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello! API is working.' and nothing else."}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        # Test schema analysis 
        print("\n🔍 Testing schema analysis...")
        schema_prompt = """
        Analyze this SQL schema and provide 2-3 quick recommendations:
        
        CREATE TABLE products (id INT, name TEXT);
        
        Respond in JSON format with recommendations.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert database schema architect."},
                {"role": "user", "content": schema_prompt}
            ],
            temperature=0.1,
            max_tokens=300
        )
        
        result = response.choices[0].message.content
        print(f"📋 Schema Analysis: {result[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing OpenAI API with GPT-4o-mini")
    print("=" * 50)
    
    if test_openai_direct():
        print("\n🎉 Success! Your API key works with GPT-4o-mini")
        print("💡 The service should now work with AI-powered recommendations")
    else:
        print("\n❌ API test failed")
        print("🔧 Possible solutions:")
        print("   1. Check your OpenAI billing/quota at https://platform.openai.com/usage")
        print("   2. Try Anthropic Claude instead")
        print("   3. Use the service without AI (basic validation only)") 