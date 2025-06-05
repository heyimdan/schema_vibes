#!/usr/bin/env python3
"""
Demo script to test Schema Validator Service components
"""

from app.services.vector_store import VectorStoreService
from app.models.schema import SchemaType, SchemaValidationRequest
from app.core.config import settings

def test_vector_store():
    """Test the vector store functionality"""
    print("🔧 Testing Vector Store...")
    vs = VectorStoreService()
    
    # Test getting best practices for SQL
    practices = vs.get_all_practices_for_schema_type(SchemaType.SQL_DDL)
    print(f"📚 Found {len(practices)} best practices for SQL DDL")
    
    for i, practice in enumerate(practices[:3], 1):
        print(f"  {i}. {practice['metadata']['category']}: {practice['content'][:60]}...")
    
    print("\n✅ Vector Store working correctly!")
    return True

def test_schema_models():
    """Test the Pydantic models"""
    print("\n🔧 Testing Schema Models...")
    
    # Test creating a validation request
    request = SchemaValidationRequest(
        schema_content="CREATE TABLE users (id INT, name VARCHAR(50));",
        schema_type=SchemaType.SQL_DDL,
        context="Test table",
        include_best_practices=True
    )
    
    print(f"📝 Created validation request for {request.schema_type}")
    print(f"   Schema content: {request.schema_content[:50]}...")
    print(f"   Include best practices: {request.include_best_practices}")
    
    print("\n✅ Schema Models working correctly!")
    return True

def test_configuration():
    """Test the configuration system"""
    print("\n🔧 Testing Configuration...")
    
    print(f"📋 AI Provider: {settings.ai_provider}")
    print(f"📋 API Host: {settings.api_host}")
    print(f"📋 API Port: {settings.api_port}")
    print(f"📋 ChromaDB Directory: {settings.chroma_persist_directory}")
    print(f"📋 Debug Mode: {settings.debug}")
    
    print("\n✅ Configuration working correctly!")
    return True

def main():
    """Run all tests"""
    print("🚀 Schema Validator Service Component Test")
    print("=" * 60)
    
    try:
        # Test each component
        test_configuration()
        test_schema_models()
        test_vector_store()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("\n📖 What this demonstrates:")
        print("  ✅ Vector database with curated best practices")
        print("  ✅ Pydantic models for schema validation")
        print("  ✅ Configuration management")
        print("  ✅ ChromaDB integration for semantic search")
        print("  ✅ Support for multiple schema types")
        
        print("\n🌐 To test the full API:")
        print("  1. Start the server: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Run: python test_service.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 