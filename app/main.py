from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.api.routes import router
from app.core.config import settings
from loguru import logger
import sys
import os

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level
)

# Create FastAPI app
app = FastAPI(
    title="Schema Validator Service",
    description="AI-powered schema validation and improvement recommendations service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2024-01-01T00:00:00Z"  # In real app, use datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "status_code": 500,
            "timestamp": "2024-01-01T00:00:00Z"  # In real app, use datetime.utcnow().isoformat()
        }
    )


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting Schema Validator Service...")
    logger.info(f"AI Provider: {settings.ai_provider}")
    logger.info(f"Vector DB: {settings.chroma_persist_directory}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down Schema Validator Service...")


# Include API routes
app.include_router(router, prefix="/api/v1", tags=["schema-validation"])


@app.get("/")
async def root():
    """Serve the frontend application."""
    from fastapi.responses import FileResponse
    
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    index_file = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        # Fallback to API info if frontend not available
        return {
            "service": "Schema Validator Service",
            "version": "1.0.0",
            "description": "AI-powered schema validation and improvement recommendations",
            "docs": "/docs",
            "health": "/api/v1/health",
            "frontend": "Frontend not found. Expected at /static/index.html",
            "admin": "/admin - Admin panel for managing best practices",
            "supported_endpoints": [
                "POST /api/v1/validate - Full schema validation",
                "POST /api/v1/validate/simple - Simple validation", 
                "GET /api/v1/schema-types - Supported schema types",
                "GET /api/v1/best-practices - Get best practices",
                "POST /api/v1/best-practices - Add best practice",
                "GET /api/v1/examples - Example schemas",
                "GET /api/v1/health - Health check",
                "GET /api/v1/stats - Service statistics"
            ]
        }


@app.get("/admin")
async def admin_panel():
    """Serve the admin panel."""
    from fastapi.responses import FileResponse
    
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    admin_file = os.path.join(static_dir, "admin.html")
    
    if os.path.exists(admin_file):
        return FileResponse(admin_file)
    else:
        return {
            "error": "Admin panel not found",
            "detail": "Admin panel expected at /static/admin.html"
        }


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Schema Validator Service API",
        version="1.0.0",
        description="""
        ## Schema Validator Service
        
        An AI-powered service for validating database schemas and providing improvement recommendations.
        
        ### Features:
        - **AI Analysis**: Uses OpenAI or Anthropic APIs for intelligent schema analysis
        - **Best Practices**: Vector database of curated schema best practices
        - **Multiple Formats**: Supports JSON Schema, SQL DDL, MongoDB, Avro, and more
        - **Detailed Recommendations**: Categorized recommendations with severity levels
        - **REST API**: Easy integration with existing tools and workflows
        
        ### Getting Started:
        1. Configure your AI provider API key in environment variables
        2. Use `/api/v1/validate` for full schema analysis
        3. Use `/api/v1/validate/simple` for quick recommendations
        4. Check `/api/v1/examples` for sample schemas to test with
        
        ### Supported Schema Types:
        - JSON Schema
        - SQL DDL (CREATE TABLE statements)
        - MongoDB Schema
        - Apache Avro
        - Protocol Buffers
        - BigQuery
        - Snowflake
        - Redshift
        - Elasticsearch
        """,
        routes=app.routes,
    )
    
    # Add some custom info
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 