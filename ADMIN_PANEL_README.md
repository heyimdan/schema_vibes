# Admin Panel Documentation

## Overview

The Schema Validator Service includes a comprehensive admin panel for managing the vector database of best practices. The admin panel provides a modern web interface to visualize, add, edit, and delete schema validation best practices.

## Features

### 🎯 Dashboard
- **Statistics Overview**: View key metrics including total best practices, schema types, AI service status, and platform coverage
- **Visual Charts**: Interactive charts showing best practices distribution by category and platform
- **Real-time Data**: All data refreshes automatically and can be manually refreshed

### 📋 Best Practices Management
- **View All Practices**: Browse all best practices in a searchable, filterable table
- **Filter Options**: Filter by schema type, platform, or category
- **Detailed View**: See all metadata including severity, applicable schema types, and platforms
- **Edit/Delete Actions**: Direct buttons for modifying or removing practices

### ➕ Add New Practices
- **Guided Form**: Step-by-step form for adding new best practices
- **Validation**: Client-side validation ensures all required fields are filled
- **Schema Type Selection**: Multi-select checkboxes for applicable schema types
- **Platform Selection**: Optional platform-specific targeting
- **Examples Support**: Add multiple examples with line-by-line input

### 📊 Analytics
- **Category Analytics**: See which categories have the most best practices
- **Severity Distribution**: Understand the severity breakdown of your practices
- **Schema Coverage**: View how well each schema type is covered
- **Future Ready**: Designed to support activity tracking and usage metrics

## Accessing the Admin Panel

### Web Interface
Navigate to: `http://localhost:8000/admin`

### Direct API Access
The admin panel uses these API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/best-practices` | List all best practices |
| POST | `/api/v1/best-practices` | Add a new best practice |
| PUT | `/api/v1/best-practices/{id}` | Update an existing practice |
| DELETE | `/api/v1/best-practices/{id}` | Delete a practice |
| GET | `/api/v1/stats` | Get service statistics |
| GET | `/api/v1/schema-types` | Get supported schema types |

## Adding Best Practices

### Via Web Interface

1. **Navigate to Admin Panel**: Go to `http://localhost:8000/admin`
2. **Click "Add Practice"**: Use the sidebar navigation
3. **Fill Required Fields**:
   - Practice ID (unique identifier)
   - Title (clear, descriptive name)
   - Description (detailed explanation)
   - Category (e.g., naming, security, performance)
   - Severity (low, medium, high)
4. **Select Schema Types**: Choose which schema types this practice applies to
5. **Optional Platform Selection**: Target specific platforms if needed
6. **Add Examples**: Provide good/bad examples (one per line)
7. **Save**: Click the save button to add the practice

### Via API

```bash
curl -X POST "http://localhost:8000/api/v1/best-practices" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "custom_001",
    "title": "Use Consistent Field Ordering",
    "description": "Order fields logically within schemas for better readability",
    "category": "organization",
    "severity_if_missing": "low",
    "applicable_schema_types": ["json_schema", "sql_ddl"],
    "applicable_platforms": [],
    "examples": [
      "Good: id, name, email, created_at, updated_at",
      "Bad: email, updated_at, id, name, created_at"
    ]
  }'
```

### Via Python Script

```python
import requests

new_practice = {
    "id": "performance_001",
    "title": "Optimize Column Data Types",
    "description": "Choose the smallest appropriate data type to reduce storage",
    "category": "performance",
    "severity_if_missing": "medium",
    "applicable_schema_types": ["sql_ddl", "bigquery"],
    "applicable_platforms": ["bigquery", "snowflake"],
    "examples": [
        "Good: Use SMALLINT instead of INT for small numbers",
        "Good: Use VARCHAR(50) instead of TEXT for short strings",
        "Bad: Use TEXT for everything"
    ]
}

response = requests.post(
    "http://localhost:8000/api/v1/best-practices",
    json=new_practice
)

if response.status_code == 200:
    print("✅ Best practice added successfully!")
else:
    print(f"❌ Error: {response.text}")
```

## Best Practice Structure

### Required Fields
- **id**: Unique identifier (string)
- **title**: Human-readable name (string)
- **description**: Detailed explanation (string)
- **category**: Practice category (string)
- **severity_if_missing**: Impact level ("low", "medium", "high")
- **applicable_schema_types**: List of schema types (array)

### Optional Fields
- **applicable_platforms**: Target platforms (array, empty = all platforms)
- **examples**: Usage examples (array of strings)

### Supported Schema Types
- `json_schema`
- `sql_ddl`
- `mongodb`
- `avro`
- `protobuf`
- `bigquery`
- `snowflake`
- `redshift`
- `elasticsearch`

### Supported Platforms
- `venice`
- `bigquery`
- `snowflake`
- `redshift`
- `elasticsearch`
- `mongodb`
- `postgres`
- `mysql`

## Testing the Admin Panel

### Automated Testing
Run the included test script:

```bash
cd /Users/dawhite/schema_validator_service
python test_admin_api.py
```

This script will:
1. Check service health
2. Get current statistics
3. List existing best practices
4. Add a test practice
5. Update the test practice
6. Delete the test practice
7. Verify all operations completed successfully

### Manual Testing
1. **Start the Service**:
   ```bash
   cd /Users/dawhite/schema_validator_service
   source venv/bin/activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. **Access Admin Panel**: Open `http://localhost:8000/admin` in your browser

3. **Test Features**:
   - Browse the dashboard
   - Filter best practices
   - Add a new practice
   - Edit an existing practice
   - Delete a practice

## Security Considerations

### Current State
- **No Authentication**: The admin panel is currently open to anyone with access
- **Local Access**: Designed for localhost development/testing

### Production Recommendations
For production deployment, consider:
- **Authentication**: Add login/session management
- **Authorization**: Role-based access control
- **HTTPS**: Use SSL/TLS encryption
- **Rate Limiting**: Prevent abuse of admin endpoints
- **Audit Logging**: Track admin actions
- **IP Restrictions**: Limit admin access to specific IPs

## Troubleshooting

### Common Issues

1. **Admin Panel Won't Load**
   - Check if service is running: `curl http://localhost:8000/api/v1/health`
   - Verify static files exist: `ls static/admin.html`
   - Check server logs for errors

2. **Can't Add Best Practices**
   - Ensure unique practice ID
   - Check all required fields are filled
   - Verify schema types are from supported list
   - Check server logs for validation errors

3. **Vector Database Issues**
   - Check ChromaDB permissions
   - Verify `chroma_db` directory exists and is writable
   - Restart service to reinitialize database

4. **AI Service Not Available**
   - Check OpenAI API key configuration
   - Verify internet connectivity
   - Check API quota/billing status

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Practice ID already exists" | Duplicate ID | Use unique identifier |
| "Missing required fields" | Form validation | Fill all required fields |
| "Schema type not supported" | Invalid type | Use supported schema type |
| "AI service unavailable" | API/config issue | Check AI service configuration |
| "Vector store error" | Database issue | Check ChromaDB setup |

## API Documentation

Full API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Monitoring and Maintenance

### Health Checks
Monitor service health:
```bash
curl http://localhost:8000/api/v1/health
```

### Statistics Monitoring
Track usage and growth:
```bash
curl http://localhost:8000/api/v1/stats
```

### Backup Recommendations
- **Vector Database**: Backup `chroma_db` directory regularly
- **Configuration**: Keep environment variables documented
- **Best Practices**: Export practices periodically for backup

## Support

For issues or questions:
1. Check the main service logs
2. Review this documentation
3. Test with the provided test scripts
4. Check the API documentation at `/docs` 