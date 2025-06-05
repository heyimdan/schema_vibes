#!/usr/bin/env python3
"""
Test script for the Admin Panel API endpoints.

This script demonstrates how to:
1. Add a new best practice
2. List all best practices  
3. Update an existing best practice
4. Delete a best practice

Usage:
    python test_admin_api.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health endpoint."""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service is healthy")
            print(f"   📊 AI Service: {data.get('ai_service', 'unknown')}")
            print(f"   🤖 AI Provider: {data.get('ai_provider', 'unknown')}")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False

def test_get_stats():
    """Test the stats endpoint."""
    print("\n📊 Testing Service Stats...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Stats retrieved successfully")
            print(f"   📚 Total Best Practices: {data.get('total_best_practices', 0)}")
            print(f"   🔧 Schema Types Supported: {data.get('supported_schema_types', 0)}")
            print(f"   🤖 AI Provider: {data.get('ai_provider', 'none')}")
            return data
        else:
            print(f"   ❌ Stats failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Stats error: {e}")
        return None

def test_list_best_practices():
    """Test listing all best practices."""
    print("\n📋 Testing List Best Practices...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/best-practices")
        if response.status_code == 200:
            practices = response.json()
            print(f"   ✅ Found {len(practices)} best practices")
            
            # Show some examples
            for i, practice in enumerate(practices[:3]):
                print(f"   📄 #{i+1}: {practice['id']} - {practice.get('metadata', {}).get('category', 'N/A')}")
            
            if len(practices) > 3:
                print(f"   ... and {len(practices) - 3} more")
            
            return practices
        else:
            print(f"   ❌ List failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"   ❌ List error: {e}")
        return []

def test_add_best_practice():
    """Test adding a new best practice."""
    print("\n➕ Testing Add Best Practice...")
    
    new_practice = {
        "id": "test_admin_001",
        "title": "Test Admin Practice",
        "description": "This is a test practice added via the admin API for demonstration purposes.",
        "category": "testing",
        "severity_if_missing": "low",
        "applicable_schema_types": ["json_schema", "sql_ddl"],
        "applicable_platforms": ["venice", "bigquery"],
        "examples": [
            "Good: This is a good example",
            "Bad: This is a bad example"
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/best-practices",
            json=new_practice,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Best practice added successfully")
            print(f"   💾 Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"   ❌ Add failed: {response.status_code}")
            if response.text:
                print(f"   📄 Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Add error: {e}")
        return False

def test_update_best_practice():
    """Test updating an existing best practice."""
    print("\n✏️ Testing Update Best Practice...")
    
    updated_practice = {
        "id": "test_admin_001",
        "title": "Updated Test Admin Practice",
        "description": "This practice has been updated via the admin API to show update functionality.",
        "category": "testing_updated",
        "severity_if_missing": "medium",
        "applicable_schema_types": ["json_schema", "sql_ddl", "mongodb"],
        "applicable_platforms": ["venice"],
        "examples": [
            "Good: Updated good example",
            "Bad: Updated bad example",
            "Note: This practice was updated"
        ]
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/v1/best-practices/test_admin_001",
            json=updated_practice,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Best practice updated successfully")
            print(f"   💾 Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"   ❌ Update failed: {response.status_code}")
            if response.text:
                print(f"   📄 Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Update error: {e}")
        return False

def test_delete_best_practice():
    """Test deleting a best practice."""
    print("\n🗑️ Testing Delete Best Practice...")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/v1/best-practices/test_admin_001")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Best practice deleted successfully")
            print(f"   💾 Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"   ❌ Delete failed: {response.status_code}")
            if response.text:
                print(f"   📄 Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Delete error: {e}")
        return False

def test_schema_types():
    """Test getting supported schema types."""
    print("\n🔧 Testing Schema Types...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/schema-types")
        if response.status_code == 200:
            schema_types = response.json()
            print(f"   ✅ Found {len(schema_types)} schema types")
            print(f"   📋 Types: {', '.join(schema_types)}")
            return schema_types
        else:
            print(f"   ❌ Schema types failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"   ❌ Schema types error: {e}")
        return []

def main():
    """Run all admin API tests."""
    print("🚀 Testing Admin Panel API Endpoints")
    print("=" * 50)
    
    # Basic health check
    if not test_health_check():
        print("\n❌ Service is not healthy. Please start the server first.")
        print("   Command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return
    
    # Get initial stats
    initial_stats = test_get_stats()
    initial_count = initial_stats.get('total_best_practices', 0) if initial_stats else 0
    
    # Test schema types
    test_schema_types()
    
    # List initial practices
    initial_practices = test_list_best_practices()
    
    # Test adding a practice
    if test_add_best_practice():
        time.sleep(1)  # Give it a moment to process
        
        # Verify it was added
        updated_practices = test_list_best_practices()
        if len(updated_practices) > len(initial_practices):
            print(f"   ✅ Verified: Practice count increased from {len(initial_practices)} to {len(updated_practices)}")
        
        # Test updating the practice
        if test_update_best_practice():
            time.sleep(1)
            
            # Test deleting the practice
            if test_delete_best_practice():
                time.sleep(1)
                
                # Verify it was deleted
                final_practices = test_list_best_practices()
                if len(final_practices) == len(initial_practices):
                    print(f"   ✅ Verified: Practice count returned to {len(final_practices)}")
                else:
                    print(f"   ⚠️ Warning: Practice count is {len(final_practices)}, expected {len(initial_practices)}")
    
    # Final stats
    final_stats = test_get_stats()
    final_count = final_stats.get('total_best_practices', 0) if final_stats else 0
    
    print("\n🎉 Admin API Test Complete!")
    print("=" * 50)
    print(f"Initial practice count: {initial_count}")
    print(f"Final practice count: {final_count}")
    print(f"Admin panel URL: {BASE_URL}/admin")
    print(f"Main app URL: {BASE_URL}/")
    print(f"API docs: {BASE_URL}/docs")

if __name__ == "__main__":
    main() 