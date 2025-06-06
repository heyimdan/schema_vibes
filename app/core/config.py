from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # AI Provider Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ai_provider: str = "openai"  # or 'anthropic'
    gpt_model: str = "gpt-4o-mini"  # configurable GPT model
    
    # Authentication Configuration
    admin_password: Optional[str] = None  # Admin panel password (can be encrypted)
    session_secret: Optional[str] = None  # Secret for session signing
    
    # Encryption Configuration
    master_key: Optional[str] = None  # For encrypting/decrypting API keys
    
    # Vector Database Configuration
    # Use persistent disk mount point for Render, fallback to local for development
    chroma_persist_directory: str = os.environ.get("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    collection_name: str = "schema_best_practices"
    # Control whether to auto-populate default best practices (disable in production)
    auto_populate_defaults: bool = os.environ.get("AUTO_POPULATE_DEFAULTS", "true").lower() == "true"
    
    # Database Configuration
    database_url: str = "sqlite:///./schema_validator.db"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_decrypted_openai_key(self) -> Optional[str]:
        """Get the decrypted OpenAI API key."""
        if not self.openai_api_key:
            # Try to get from environment if not in config
            self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            return None
            
        # Import here to avoid circular imports
        from app.core.encryption import is_encrypted, decrypt_api_key
        
        if is_encrypted(self.openai_api_key):
            return decrypt_api_key(self.openai_api_key)
        else:
            return self.openai_api_key
    
    def get_decrypted_anthropic_key(self) -> Optional[str]:
        """Get the decrypted Anthropic API key."""
        if not self.anthropic_api_key:
            # Try to get from environment if not in config
            self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
            
        if not self.anthropic_api_key:
            return None
            
        # Import here to avoid circular imports
        from app.core.encryption import is_encrypted, decrypt_api_key
        
        if is_encrypted(self.anthropic_api_key):
            return decrypt_api_key(self.anthropic_api_key)
        else:
            return self.anthropic_api_key
    
    def get_decrypted_admin_password(self) -> str:
        """Get the decrypted admin password."""
        if not self.admin_password:
            # Try to get from environment if not in config
            self.admin_password = os.environ.get("ADMIN_PASSWORD")
        
        if not self.admin_password:
            # Default password if none configured
            return "secret"
            
        # Import here to avoid circular imports
        from app.core.encryption import is_encrypted, decrypt_api_key
        
        if is_encrypted(self.admin_password):
            return decrypt_api_key(self.admin_password)
        else:
            return self.admin_password
    
    def get_session_secret(self) -> str:
        """Get the session secret for signing sessions."""
        if not self.session_secret:
            # Try to get from environment if not in config
            self.session_secret = os.environ.get("SESSION_SECRET")
        
        if not self.session_secret:
            # Generate a default session secret based on master key or random
            import secrets
            return secrets.token_urlsafe(32)
            
        return self.session_secret


settings = Settings()


# Schema validation configuration
SUPPORTED_SCHEMA_TYPES = [
    "json_schema",
    "avro",
    "protobuf", 
    "sql_ddl"
]

# AI prompts configuration
SCHEMA_ANALYSIS_PROMPT = """
You are an expert database schema architect. Analyze the provided schema and provide detailed recommendations for improvements.

Consider the following aspects:
1. **Naming Conventions**: Are field names clear, consistent, and follow best practices?
2. **Data Types**: Are the data types appropriate and efficient?
3. **Constraints**: Are there missing or inappropriate constraints?
4. **Indexing**: Are there indexing opportunities for performance?
5. **Normalization**: Is the schema properly normalized or denormalized as needed?
6. **Scalability**: Will this schema scale well with data growth?
7. **Security**: Are there any security considerations?
8. **Documentation**: Is the schema self-documenting?

Schema Type: {schema_type}
Schema Content:
{schema_content}

Best Practices Context:
{best_practices_context}

Provide your analysis in the following JSON format:
{{
    "overall_score": <1-10>,
    "recommendations": [
        {{
            "category": "<category>",
            "severity": "<low|medium|high>",
            "description": "<detailed description>",
            "suggestion": "<specific improvement suggestion>",
            "impact": "<expected impact of the change>"
        }}
    ],
    "best_practices_applied": ["<list of applied best practices>"],
    "missing_best_practices": ["<list of missing best practices>"],
    "summary": "<overall summary of the schema quality>"
}}
"""
