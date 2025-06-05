#!/usr/bin/env python3
"""Test API endpoints directly"""

from app.api.routes import get_supported_schema_types, get_example_schemas
import asyncio

async def test_endpoints():
    print('🔧 Testing API Endpoints...')
    
    # Test supported schema types
    types = await get_supported_schema_types()
    print(f'📋 Supported schema types: {types}')
    
    # Test example schemas
    examples = await get_example_schemas()
    print(f'📚 Available examples: {list(examples.keys())}')
    
    for name, info in examples.items():
        print(f'  • {name}: {info["description"]}')
    
    print('✅ API Endpoints working correctly!')

if __name__ == "__main__":
    asyncio.run(test_endpoints()) 