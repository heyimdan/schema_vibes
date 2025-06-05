# Schema Vibe Check 🌟

An AI-powered schema validation service that gives your schemas a fun "vibe check" with intelligent recommendations and cute scoring messages. This service combines Large Language Models with a vector database of curated best practices to deliver actionable schema optimization suggestions.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT models or Anthropic Claude for intelligent schema analysis
- 📊 **Vector Database**: ChromaDB stores and retrieves relevant best practices using semantic search
- 🔧 **Multiple Schema Formats**: Supports JSON Schema, SQL DDL, Avro, Protobuf, BigQuery, Snowflake, and Redshift
- 🎯 **Cute Vibe Scoring**: Fun messages based on your schema's vibe score (1-10)
- 📝 **Detailed Recommendations**: Categorized suggestions with severity levels and expected impact
- 🚀 **REST API**: Easy integration with existing tools and workflows
- 🎨 **Modern Web UI**: Beautiful interface for interactive schema validation
- 🔐 **Admin Panel**: Secure admin interface for managing best practices and configurations
- 🛡️ **Production Security**: Encrypted API keys and password-protected admin features
- 🚢 **Cloud Deployment**: Ready for deployment on Render and other cloud platforms
- 🐳 **Docker Ready**: Complete containerization for easy deployment

## 📋 Supported Schema Types

- **JSON Schema** - JSON Schema specifications
- **SQL DDL** - CREATE TABLE statements
- **Apache Avro** - Avro schema definitions
- **Protocol Buffers** - Protobuf schema files
- **BigQuery** - Google BigQuery table schemas
- **Snowflake** - Snowflake DDL statements
- **Redshift** - Amazon Redshift schemas

## 🏢 Supported Platforms

- **Venice** - LinkedIn's Venice database
- **Espresso** - LinkedIn's Espresso database
- **Kafka** - Apache Kafka
- **Pinot** - Apache Pinot
- **MySQL** - MySQL database
- **TiDB** - TiDB database  
- **BigQuery** - Google BigQuery
- **Snowflake** - Snowflake data warehouse

## 🚀 Quick Start

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

# Admin panel password (encrypted in production)
ADMIN_PASSWORD=secret

# Master key for encryption (generate with encrypt_api_key.py)
SCHEMA_VALIDATOR_MASTER_KEY=your_master_key_here
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
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Cloud Deployment (Render)

See the [Render Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🌐 Web Interface

Visit `http://localhost:8000` to access the beautiful web interface:

- **Main Page**: Interactive schema validation with examples
- **Admin Panel**: `http://localhost:8000/admin.html` (password: `secret`)
- **API Docs**: `http://localhost:8000/docs` for OpenAPI documentation

### Vibe Check Messages ✨

Your schema gets a fun message based on its vibe score:
- **Score 8-10**: "Your schema has amazing vibes! ✨"
- **Score 6-7**: "Your schema has good vibes! 😊"
- **Score 4-5**: "Your schema has mixed vibes 🤔"
- **Score 0-3**: "Your schema did not pass the vibe check 😬"

## 🔌 API Usage

### 1. Full Schema Validation

```bash
curl -X POST "http://localhost:8000/api/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "schema_content": "CREATE TABLE users (id INT, name VARCHAR(50), email VARCHAR(100));",
    "schema_type": "sql_ddl",
    "context": "User management table for web application",
    "include_best_practices": true,
    "platform": "mysql"
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
  "summary": "Your schema has good vibes! 😊 Good naming but lacks essential constraints.",
  "processing_time": 2.34
}
```

### 2. Get Available Schema Types

```bash
curl "http://localhost:8000/api/v1/schema-types"
```

### 3. Get Example Schemas

```bash
curl "http://localhost:8000/api/v1/examples"
```

### 4. Health Check

```bash
curl "http://localhost:8000/api/v1/health"
```

## 🔐 Admin Panel Features

Access the admin panel at `/admin.html` with password `secret`:

- **Statistics Dashboard**: View validation metrics and trends
- **Best Practices Management**: Add, edit, and delete best practices
- **GPT Model Configuration**: Switch between different OpenAI models
- **Schema Type Management**: View supported schema types
- **Authentication**: Secure login with session management

### Admin API Endpoints

```bash
# Login (required for admin operations)
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"password": "secret"}'

# Get statistics
curl "http://localhost:8000/api/v1/stats" \
  -H "Cookie: session_token=your_session_token"

# Manage best practices
curl "http://localhost:8000/api/v1/best-practices" \
  -H "Cookie: session_token=your_session_token"

# Update GPT model
curl -X POST "http://localhost:8000/api/v1/config/model" \
  -H "Content-Type: application/json" \
  -H "Cookie: session_token=your_session_token" \
  -d '{"model": "gpt-4o"}'
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web UI        │────│  FastAPI Server  │────│   AI Provider   │
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
2. **Web Interface**: Modern HTML/CSS/JS frontend with admin panel
3. **AI Service**: Interfaces with OpenAI/Anthropic APIs for schema analysis
4. **Vector Store**: ChromaDB for storing and retrieving best practices
5. **Authentication System**: Secure admin panel with session management
6. **Encryption Service**: Production-ready API key encryption

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider (`openai` or `anthropic`) | `openai` |
| `OPENAI_API_KEY` | OpenAI API key (supports encryption) | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key (supports encryption) | Required if using Anthropic |
| `ADMIN_PASSWORD` | Admin panel password (supports encryption) | `secret` |
| `SCHEMA_VALIDATOR_MASTER_KEY` | Master key for encryption | Auto-generated |
| `API_HOST` | Server host | `0.0.0.0` |
| `API_PORT` | Server port | `8000` |
| `DEBUG` | Enable debug mode | `True` |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB data directory | `./chroma_db` |

## 🔒 Security & Encryption

### Production API Key Encryption

For secure public deployment, encrypt your API keys:

1. **Run the encryption utility:**
```bash
python encrypt_api_key.py
```

2. **Use the generated encrypted values:**
```bash
export SCHEMA_VALIDATOR_MASTER_KEY="1pfQUrO6gXjTc95uvcMI9tGyxAHP85JmTk-xQm08ons="
export OPENAI_API_KEY="encrypted:Z0FBQUFBQm9RZ3NXczF..."
export ADMIN_PASSWORD="encrypted:Z0FBQUFBQm9RZzYzYUR..."
```

3. **Deploy with encrypted credentials** - see [Deployment Checklist](DEPLOYMENT_CHECKLIST.md)

## 🛠️ Development

### Project Structure

```
schema_validator_service/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints with auth
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── encryption.py      # API key encryption
│   │   └── auth.py            # Authentication system
│   ├── models/
│   │   └── schema.py          # Pydantic models and enums
│   ├── services/
│   │   ├── ai_service.py      # AI integration
│   │   └── vector_store.py    # ChromaDB integration
│   └── main.py                # FastAPI application
├── static/                    # Web UI files
│   ├── index.html             # Main interface
│   ├── admin.html             # Admin panel
│   ├── styles.css             # Main styles
│   ├── admin.css              # Admin styles
│   ├── script.js              # Main JavaScript
│   └── admin.js               # Admin JavaScript
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── render.yaml                # Render deployment config
├── encrypt_api_key.py         # Encryption utility
└── README.md                  # This file
```

### Adding New Schema Types

1. Add the new type to `SchemaType` enum in `app/models/schema.py`
2. Add platform support to `Platform` enum if needed
3. Update best practices in `app/services/vector_store.py`
4. Add examples to the web interface
5. Test with the admin panel

### Adding New Platforms

1. Add to `Platform` enum in `app/models/schema.py`
2. Create platform-specific best practices
3. Update the AI prompts if needed
4. Test platform-specific recommendations

## 🚀 Deployment Options

### Render (Recommended)

1. Fork this repository
2. Connect to Render
3. Set environment variables (see [Render Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md))
4. Deploy with encrypted API keys

### Docker

```bash
# Build and run
docker build -t schema-vibe-check .
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e ADMIN_PASSWORD=your_password \
  schema-vibe-check
```

### Local Production

```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export DEBUG=False
export OPENAI_API_KEY=encrypted:your_encrypted_key

# Run with production settings
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📊 Monitoring

### Health Checks

```bash
curl http://localhost:8000/api/v1/health
```

### Admin Statistics

Access comprehensive statistics through the admin panel:
- Total validations performed
- Average schema scores
- Most common issues
- Schema type popularity
- Platform usage metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both web UI and API
5. Update documentation if needed
6. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🎯 Support

For issues and questions:
1. Check the [Deployment Checklist](DEPLOYMENT_CHECKLIST.md)
2. Review the admin panel for configuration issues
3. Check the API documentation at `/docs`
4. Open an issue on GitHub

---

**Ready to give your schemas a vibe check?** 🌟 Start validating and get those amazing vibes! ✨ 