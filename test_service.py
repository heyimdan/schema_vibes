#!/usr/bin/env python3
"""
Test script for the Schema Validator Service
Demonstrates various API endpoints and functionality
"""

import requests
import json
import time
from typing import Dict, Any


class SchemaValidatorClient:
    """Client for testing the Schema Validator Service"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the service is healthy"""
        response = self.session.get(f"{self.base_url}/api/v1/health")
        return response.json()
    
    def get_supported_types(self):
        """Get supported schema types"""
        response = self.session.get(f"{self.base_url}/api/v1/schema-types")
        return response.json()
    
    def validate_schema(self, schema_content: str, schema_type: str, context: str = None) -> Dict[str, Any]:
        """Validate a schema with full analysis"""
        payload = {
            "schema_content": schema_content,
            "schema_type": schema_type,
            "context": context,
            "include_best_practices": True
        }
        response = self.session.post(f"{self.base_url}/api/v1/validate", json=payload)
        return response.json()
    
    def simple_validate(self, schema_content: str, schema_type: str) -> Dict[str, Any]:
        """Simple validation without full analysis"""
        response = self.session.post(
            f"{self.base_url}/api/v1/validate/simple",
            json={"schema_content": schema_content, "schema_type": schema_type}
        )
        return response.json()
    
    def get_examples(self) -> Dict[str, Any]:
        """Get example schemas"""
        response = self.session.get(f"{self.base_url}/api/v1/examples")
        return response.json()


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_validation_result(result: Dict[str, Any]):
    """Pretty print validation results"""
    print(f"📊 Overall Score: {result.get('overall_score', 'N/A')}/10")
    print(f"⏱️  Processing Time: {result.get('processing_time', 'N/A'):.2f}s")
    
    recommendations = result.get('recommendations', [])
    if recommendations:
        print(f"\n📝 Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.get('severity', 'low'), "🔵")
            print(f"  {i}. {severity_icon} [{rec.get('category', 'general').upper()}] {rec.get('description', 'No description')}")
            print(f"     💡 Suggestion: {rec.get('suggestion', 'No suggestion')}")
            print(f"     📈 Impact: {rec.get('impact', 'No impact described')}")
            print()
    
    best_practices = result.get('best_practices_applied', [])
    if best_practices:
        print(f"✅ Applied Best Practices: {', '.join(best_practices)}")
    
    missing_practices = result.get('missing_best_practices', [])
    if missing_practices:
        print(f"❌ Missing Best Practices: {', '.join(missing_practices)}")
    
    summary = result.get('summary', '')
    if summary:
        print(f"\n📋 Summary: {summary}")


def main():
    """Main test function"""
    print("🚀 Schema Validator Service Test")
    print("Testing various schemas and API endpoints...")
    
    client = SchemaValidatorClient()
    
    # Health check
    print_section("Health Check")
    try:
        health = client.health_check()
        print(f"✅ Service Status: {health.get('status', 'unknown')}")
        print(f"🤖 AI Provider: {health.get('ai_provider', 'unknown')}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("Make sure the service is running on http://localhost:8000")
        return
    
    # Get supported types
    print_section("Supported Schema Types")
    try:
        types = client.get_supported_types()
        print("📋 Supported types:")
        for schema_type in types:
            print(f"  • {schema_type}")
    except Exception as e:
        print(f"❌ Failed to get supported types: {e}")
    
    # Test SQL DDL validation
    print_section("Test 1: SQL DDL Schema")
    sql_schema = """
    CREATE TABLE users (
        id INT,
        name VARCHAR(50),
        email VARCHAR(100),
        created_at TIMESTAMP
    );
    """
    
    try:
        result = client.validate_schema(
            schema_content=sql_schema,
            schema_type="sql_ddl",
            context="User management table for web application"
        )
        print_validation_result(result)
    except Exception as e:
        print(f"❌ SQL validation failed: {e}")
    
    # Test JSON Schema validation
    print_section("Test 2: JSON Schema")
    json_schema = """{
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"}
        }
    }"""
    
    try:
        result = client.validate_schema(
            schema_content=json_schema,
            schema_type="json_schema",
            context="User profile validation schema"
        )
        print_validation_result(result)
    except Exception as e:
        print(f"❌ JSON Schema validation failed: {e}")
    
    # Test MongoDB schema
    print_section("Test 3: MongoDB Schema")
    mongodb_schema = """{
        "bsonType": "object",
        "required": ["_id", "name"],
        "properties": {
            "_id": {"bsonType": "objectId"},
            "name": {"bsonType": "string"},
            "tags": {"bsonType": "array"}
        }
    }"""
    
    try:
        result = client.validate_schema(
            schema_content=mongodb_schema,
            schema_type="mongodb",
            context="Document collection schema"
        )
        print_validation_result(result)
    except Exception as e:
        print(f"❌ MongoDB validation failed: {e}")
    
    # Test simple validation
    print_section("Test 4: Simple Validation")
    simple_schema = "CREATE TABLE products (id INT, name TEXT);"
    
    try:
        result = client.simple_validate(simple_schema, "sql_ddl")
        print("📝 Simple Recommendations:")
        for i, rec in enumerate(result.get('recommendations', []), 1):
            print(f"  {i}. {rec}")
    except Exception as e:
        print(f"❌ Simple validation failed: {e}")
    
    # Get examples
    print_section("Available Examples")
    try:
        examples = client.get_examples()
        print("📚 Example schemas available:")
        for schema_type, info in examples.items():
            print(f"  • {schema_type}: {info.get('description', 'No description')}")
    except Exception as e:
        print(f"❌ Failed to get examples: {e}")
    
    print_section("Test Complete")
    print("✅ All tests completed!")
    print("🌐 Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    main() 