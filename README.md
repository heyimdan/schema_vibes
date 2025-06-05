# Schema Validator Service

An AI-powered service for validating database schemas and providing intelligent improvement recommendations. This service combines Large Language Models (LLMs) with a vector database of curated best practices to deliver actionable schema optimization suggestions.

## Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT-4 or Anthropic Claude for intelligent schema analysis
- 📊 **Vector Database**: ChromaDB stores and retrieves relevant best practices using semantic search
- 🔧 **Multiple Schema Formats**: Supports JSON Schema, SQL DDL, MongoDB, Avro, BigQuery, Snowflake, and more
- 📝 **Detailed Recommendations**: Categorized suggestions with severity levels and expected impact
- 🚀 **REST API**: Easy integration with existing tools and workflows
- 📚 **Best Practices Management**: Add, update, and manage schema best practices
- 🐳 **Docker Ready**: Complete containerization for easy deployment

## Supported Schema Types

- **JSON Schema** - JSON Schema Draft 7 specifications
- **SQL DDL** - CREATE TABLE statements
- **MongoDB** - MongoDB schema validation rules
- **Apache Avro** - Avro schema definitions
- **Protocol Buffers** - Protobuf schema files
- **BigQuery** - Google BigQuery table schemas
- **Snowflake** - Snowflake DDL
- **Redshift** - Amazon Redshift schemas
- **Elasticsearch** - Elasticsearch mapping definitions

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- OpenAI API key OR Anthropic API key

### Environment Setup

1. **Clone and setup the project:**
```bash
git clone <repository-url>
cd schema_validator_service
```

2. **Create environment file:**
```bash
cp .env.example .env
```

3. **Configure your environment variables in `.env`:**
```bash
# Choose your AI provider
AI_PROVIDER=openai  # or 'anthropic'
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional: Redis for caching
REDIS_URL=redis://localhost:6379/0
```

### Option 1: Docker Compose (Recommended)

```bash
# Set your API key
export OPENAI_API_KEY=your_key_here

# Start the services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f schema-validator
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### 1. Full Schema Validation

```bash
curl -X POST "http://localhost:8000/api/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "schema_content": "CREATE TABLE users (id INT, name VARCHAR(50), email VARCHAR(100));",
    "schema_type": "sql_ddl",
    "context": "User management table for web application",
    "include_best_practices": true
  }'
```

**Response:**
```json
{
  "schema_id": "sql_ddl_a1b2c3d4",
  "overall_score": 6,
  "recommendations": [
    {
      "category": "constraints",
      "severity": "high",
      "description": "Primary key constraint missing",
      "suggestion": "Add PRIMARY KEY constraint to id column",
      "impact": "Ensures data integrity and enables efficient indexing"
    }
  ],
  "best_practices_applied": ["Clear naming conventions"],
  "missing_best_practices": ["Primary key definition", "NOT NULL constraints"],
  "summary": "Schema has good naming but lacks essential constraints",
  "processing_time": 2.34
}
```

### 2. Simple Validation

```bash
curl -X POST "http://localhost:8000/api/v1/validate/simple" \
  -H "Content-Type: application/json" \
  -d '{
    "schema_content": "...",
    "schema_type": "json_schema"
  }'
```

### 3. Get Example Schemas

```bash
curl "http://localhost:8000/api/v1/examples"
```

### 4. Manage Best Practices

```bash
# Get all best practices
curl "http://localhost:8000/api/v1/best-practices"

# Get practices for specific schema type
curl "http://localhost:8000/api/v1/best-practices?schema_type=sql_ddl"

# Add new best practice
curl -X POST "http://localhost:8000/api/v1/best-practices" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "custom_001",
    "title": "Use Meaningful Column Names",
    "description": "Column names should clearly indicate the data they contain",
    "category": "naming",
    "applicable_schema_types": ["sql_ddl"],
    "examples": ["Good: customer_email", "Bad: ce"],
    "severity_if_missing": "medium"
  }'
```

## Integration Examples

### Python Client

```python
import requests

class SchemaValidator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def validate_schema(self, schema_content, schema_type, context=None):
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

# Usage
validator = SchemaValidator()
result = validator.validate_schema(
    schema_content="CREATE TABLE products (id INT, name TEXT);",
    schema_type="sql_ddl",
    context="E-commerce product catalog"
)

print(f"Score: {result['overall_score']}/10")
for rec in result['recommendations']:
    print(f"• {rec['description']} - {rec['suggestion']}")
```

### JavaScript/Node.js Client

```javascript
const axios = require('axios');

class SchemaValidator {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async validateSchema(schemaContent, schemaType, context = null) {
        const response = await axios.post(`${this.baseUrl}/api/v1/validate`, {
            schema_content: schemaContent,
            schema_type: schemaType,
            context: context,
            include_best_practices: true
        });
        return response.data;
    }
}

// Usage
const validator = new SchemaValidator();
validator.validateSchema(
    `{
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
        }
    }`,
    'json_schema'
).then(result => {
    console.log(`Score: ${result.overall_score}/10`);
    result.recommendations.forEach(rec => {
        console.log(`• ${rec.description} - ${rec.suggestion}`);
    });
});
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client App    │────│  FastAPI Server  │────│   AI Provider   │
│                 │    │                  │    │ (OpenAI/Claude) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                │
                       ┌────────▼─────────┐
                       │   ChromaDB       │
                       │ (Vector Store)   │
                       │ Best Practices   │
                       └──────────────────┘
```

### Components

1. **FastAPI Server**: REST API with comprehensive endpoints
2. **AI Service**: Interfaces with OpenAI/Anthropic APIs for schema analysis
3. **Vector Store**: ChromaDB for storing and retrieving best practices
4. **Best Practices Database**: Curated knowledge base of schema optimization guidelines

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider to use (`openai` or `anthropic`) | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | Required if using Anthropic |
| `API_HOST` | Server host | `0.0.0.0` |
| `API_PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `True` |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB data directory | `./chroma_db` |
| `REDIS_URL` | Redis URL for caching | `redis://localhost:6379/0` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

### Project Structure

```
schema_validator_service/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   │   └── config.py          # Configuration
│   │   └── schema.py          # Pydantic models
│   │   ├── ai_service.py      # AI integration
│   │   └── vector_store.py    # ChromaDB integration
│   └── main.py                # FastAPI application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Multi-container setup
└── README.md                  # This file
```

### Adding New Schema Types

1. Add the new type to `SchemaType` enum in `app/models/schema.py`
2. Update the AI prompt in `app/core/config.py` if needed
3. Add schema-specific best practices in `app/services/vector_store.py`
4. Test with example schemas

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Security & Encryption

### API Key Encryption for Production

For secure public deployment, the service supports API key encryption to protect sensitive credentials:

#### Encrypting Your API Keys

1. **Run the encryption utility:**
```bash
python encrypt_api_key.py
```

2. **The script will:**
   - Generate a secure master key
   - Encrypt your current OpenAI API key
   - Create production configuration files
   - Provide deployment instructions

#### Example Output:
```
🔐 Schema Validator API Key Encryption Utility
==================================================
✅ Found OpenAI API key in environment: sk-proj-44-XNyF...

1. MASTER KEY (Store this securely!):
   SCHEMA_VALIDATOR_MASTER_KEY=1pfQUrO6gXjTc95uvcMI9tGyxAHP85JmTk-xQm08ons=

2. ENCRYPTED API KEY:
   OPENAI_API_KEY=encrypted:Z0FBQUFBQm9RZ3NXczFKS1Vh...
```

#### Production Deployment with Encrypted Keys

1. **Environment Variables:**
```bash
export SCHEMA_VALIDATOR_MASTER_KEY="your_master_key_here"
export OPENAI_API_KEY="encrypted:your_encrypted_key_here"
```

2. **Docker Compose:**
```yaml
version: '3.8'
services:
  schema-validator:
    build: .
    environment:
      - SCHEMA_VALIDATOR_MASTER_KEY=${SCHEMA_VALIDATOR_MASTER_KEY}
      - OPENAI_API_KEY=${ENCRYPTED_OPENAI_API_KEY}
    ports:
      - "8000:8000"
```

3. **Use the production template:**
```bash
# Copy and configure the environment template
cp env.template .env.production
# Edit .env.production with your encrypted values
```

#### Security Best Practices

- **Never commit the master key to version control**
- **Store the master key in a secure secret management system** (AWS Secrets Manager, Azure Key Vault, etc.)
- **Use different master keys for different environments** (staging, production)
- **The encrypted API key is safe to store in configuration files**
- **Rotate keys periodically** by re-running the encryption script

#### Key Features

- **Automatic Detection**: The service automatically detects encrypted vs. plain API keys
- **Fallback Support**: Works with both encrypted and unencrypted keys for development
- **Zero Configuration**: No code changes needed, just set environment variables
- **Secure Encryption**: Uses Fernet (symmetric encryption) with PBKDF2 key derivation

## Monitoring and Deployment

### Health Checks

```bash
curl http://localhost:8000/api/v1/health
```

### Metrics

```bash
curl http://localhost:8000/api/v1/stats
```

### Production Deployment

1. **Security**: Configure proper CORS origins and authentication
2. **Scaling**: Use multiple replicas behind a load balancer
3. **Monitoring**: Set up logging, metrics, and alerting
4. **Persistence**: Ensure ChromaDB data is persisted with volumes

## Troubleshooting

### Common Issues

1. **AI Provider API Key Not Set**
   - Ensure your API key is properly configured in environment variables
   - Check that the key has sufficient permissions and credits

2. **ChromaDB Permission Issues**
   - Ensure the ChromaDB directory is writable
   - Check Docker volume permissions

3. **High Response Times**
   - Consider enabling Redis caching
   - Use simpler validation endpoint for quick checks

### Logs

```bash
# Docker Compose
docker-compose logs -f schema-validator

# Local development
# Logs are printed to stdout with structured formatting
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `http://localhost:8000/docs`
3. Open an issue on GitHub 