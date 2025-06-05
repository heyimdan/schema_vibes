#!/usr/bin/env python3
"""
Quick test script - run this to see the Schema Validator in action
No server needed!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Schema Validator Quick Demo")
    print("=" * 50)
    
    # Test 1: Configuration
    print("\n1️⃣ Testing Configuration...")
    from app.core.config import settings
    print(f"   ✅ AI Provider: {settings.ai_provider}")
    print(f"   ✅ Port: {settings.api_port}")
    
    # Test 2: Schema Models
    print("\n2️⃣ Testing Schema Models...")
    from app.models.schema import SchemaValidationRequest, SchemaType
    
    request = SchemaValidationRequest(
        schema_content="CREATE TABLE users (id INT, name VARCHAR(50), email VARCHAR(100));",
        schema_type=SchemaType.SQL_DDL,
        context="User management table",
        include_best_practices=True
    )
    print(f"   ✅ Created request for {request.schema_type} schema")
    print(f"   📝 Schema: {request.schema_content[:50]}...")
    
    # Test 3: Vector Store
    print("\n3️⃣ Testing Vector Store...")
    from app.services.vector_store import VectorStoreService
    
    vector_store = VectorStoreService()
    practices = vector_store.get_all_practices_for_schema_type(SchemaType.SQL_DDL)
    print(f"   ✅ Vector store initialized")
    print(f"   📚 Found {len(practices)} best practices for SQL DDL")
    
    # Test 4: API Endpoints (without server)
    print("\n4️⃣ Testing API Functions...")
    from app.api.routes import get_supported_schema_types, get_example_schemas
    import asyncio
    
    async def test_api():
        types = await get_supported_schema_types()
        examples = await get_example_schemas()
        print(f"   ✅ {len(types)} schema types supported")
        print(f"   📚 {len(examples)} example schemas available")
        
        print("\n   📋 Supported types:")
        for i, schema_type in enumerate(types[:5], 1):
            print(f"      {i}. {schema_type}")
        
        print("\n   📝 Available examples:")
        for name, info in examples.items():
            print(f"      • {name}: {info['description']}")
    
    asyncio.run(test_api())
    
    # Test 5: Show Example Usage
    print("\n5️⃣ Example API Usage:")
    print("""   
   # To start the server:
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   
   # Then test with curl:
   curl -X POST "http://localhost:8000/api/v1/validate" \\
     -H "Content-Type: application/json" \\
     -d '{
       "schema_content": "CREATE TABLE products (id INT, name TEXT);",
       "schema_type": "sql_ddl",
       "context": "Product catalog",
       "include_best_practices": true
     }'
   
   # Or visit: http://localhost:8000/docs
   """)
    
    print("\n" + "=" * 50)
    print("🎉 All components working! Ready to start the server.")
    print("\n💡 To start the server:")
    print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 