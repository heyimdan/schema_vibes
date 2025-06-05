#!/usr/bin/env python3
"""
Manual test script showing how to use the Schema Validator Service
Run this after starting the server with: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

import requests
import json

def test_with_curl_commands():
    """Show equivalent curl commands for testing"""
    print("🌐 Manual Testing Guide")
    print("=" * 60)
    
    print("\n1️⃣ Start the server:")
    print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
    
    print("\n2️⃣ Test health check:")
    print("   curl http://localhost:8000/api/v1/health")
    
    print("\n3️⃣ Get supported schema types:")
    print("   curl http://localhost:8000/api/v1/schema-types")
    
    print("\n4️⃣ Get example schemas:")
    print("   curl http://localhost:8000/api/v1/examples")
    
    print("\n5️⃣ Test schema validation (without AI):")
    print("""   curl -X POST "http://localhost:8000/api/v1/validate" \\
     -H "Content-Type: application/json" \\
     -d '{
       "schema_content": "CREATE TABLE users (id INT, name VARCHAR(50));",
       "schema_type": "sql_ddl",
       "context": "User table for web app",
       "include_best_practices": false
     }'""")
    
    print("\n6️⃣ View interactive API docs:")
    print("   Open: http://localhost:8000/docs")
    
    print("\n7️⃣ To enable AI analysis:")
    print("   - Add your API key to .env file:")
    print("     OPENAI_API_KEY=sk-your-key-here")
    print("   - Or:")
    print("     ANTHROPIC_API_KEY=sk-ant-your-key-here")
    print("   - Restart the server")

def test_example_schemas():
    """Show example schemas for testing"""
    print("\n📚 Example Schemas for Testing")
    print("=" * 60)
    
    examples = {
        "sql_ddl": """CREATE TABLE customers (
    id INT,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP,
    status VARCHAR(20)
);""",
        
        "json_schema": """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "email": {"type": "string", "format": "email"}
  },
  "required": ["id", "name"]
}""",
        
        "mongodb": """{
  "bsonType": "object",
  "required": ["_id", "name"],
  "properties": {
    "_id": {"bsonType": "objectId"},
    "name": {"bsonType": "string"},
    "email": {"bsonType": "string"},
    "tags": {"bsonType": "array"}
  }
}"""
    }
    
    for schema_type, content in examples.items():
        print(f"\n🔧 {schema_type.upper()} Example:")
        print(content)

def show_integration_example():
    """Show how to integrate with your console"""
    print("\n🔗 Integration with Your Data Console")
    print("=" * 60)
    
    integration_code = '''
# Python integration example
import requests

class SchemaValidator:
    def __init__(self, base_url="http://your-validator-service:8000"):
        self.base_url = base_url
    
    def validate_schema(self, schema_content, schema_type, context=None):
        """Validate a schema and get recommendations"""
        response = requests.post(
            f"{self.base_url}/api/v1/validate",
            json={
                "schema_content": schema_content,
                "schema_type": schema_type,
                "context": context,
                "include_best_practices": True
            }
        )
        return response.json()
    
    def get_quick_recommendations(self, schema_content, schema_type):
        """Get quick recommendations without full analysis"""
        response = requests.post(
            f"{self.base_url}/api/v1/validate/simple",
            json={
                "schema_content": schema_content,
                "schema_type": schema_type
            }
        )
        return response.json()

# Usage in your console
validator = SchemaValidator()

# When user creates a new store schema
user_schema = "CREATE TABLE products (id INT, name TEXT);"
result = validator.validate_schema(user_schema, "sql_ddl", "Product catalog")

# Display recommendations in your UI
for rec in result["recommendations"]:
    print(f"⚠️  {rec['severity'].upper()}: {rec['description']}")
    print(f"💡 Suggestion: {rec['suggestion']}")
'''
    
    print(integration_code)

def main():
    """Run all manual tests"""
    test_with_curl_commands()
    test_example_schemas()
    show_integration_example()
    
    print("\n" + "=" * 60)
    print("🎯 Quick Start Summary:")
    print("1. Start server: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
    print("2. Visit: http://localhost:8000/docs")
    print("3. Test with the examples above")
    print("4. Add your AI API key for full functionality")

if __name__ == "__main__":
    main() 