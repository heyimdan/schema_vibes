from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import List, Dict, Any
from app.models.schema import (
    SchemaValidationRequest, 
    SchemaValidationResponse, 
    BestPractice,
    SchemaType
)
from app.services.ai_service import AIService
from app.services.vector_store import VectorStoreService
from app.core.config import settings
from app.core.auth import auth_manager, require_admin_auth, is_authenticated
from loguru import logger
import hashlib
import datetime
from pydantic import BaseModel

router = APIRouter()

# Model configuration classes
class ModelConfigRequest(BaseModel):
    model: str

class ModelConfigResponse(BaseModel):
    current_model: str
    message: str = None

# Initialize services with error handling
vector_store = VectorStoreService()

try:
    ai_service = AIService()
    logger.info("AI service initialized successfully")
except Exception as e:
    logger.warning(f"AI service initialization failed: {e}")
    ai_service = None


@router.post("/validate", response_model=SchemaValidationResponse)
async def validate_schema(request: SchemaValidationRequest):
    """
    Validate a schema and get AI-powered recommendations for improvements.
    
    This endpoint analyzes the provided schema using AI and returns detailed
    recommendations based on best practices stored in the vector database.
    """
    try:
        logger.info(f"Received schema validation request for type: {request.schema_type}")
        
        # Check if AI service is available
        if ai_service is None:
            raise HTTPException(status_code=503, detail="AI service is not available. Please check server configuration.")
        
        # Validate schema content is not empty
        if not request.schema_content.strip():
            raise HTTPException(status_code=400, detail="Schema content cannot be empty")
        
        # Analyze the schema
        response = await ai_service.analyze_schema(request)
        
        # Generate schema ID for tracking
        schema_hash = hashlib.md5(request.schema_content.encode()).hexdigest()
        response.schema_id = f"{request.schema_type.value}_{schema_hash[:8]}"
        
        logger.info(f"Schema validation completed with ID: {response.schema_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error validating schema: {e}")
        raise HTTPException(status_code=500, detail=f"Schema validation failed: {str(e)}")


@router.post("/validate/simple")
async def validate_schema_simple(
    schema_content: str,
    schema_type: SchemaType
) -> Dict[str, Any]:
    """
    Get simple recommendations for a schema without full analysis.
    
    This is a lighter-weight endpoint that returns just a list of key recommendations.
    """
    try:
        # Check if AI service is available
        if ai_service is None:
            raise HTTPException(status_code=503, detail="AI service is not available. Please check server configuration.")
            
        if not schema_content.strip():
            raise HTTPException(status_code=400, detail="Schema content cannot be empty")
        
        recommendations = await ai_service.get_schema_recommendations_only(
            schema_content, schema_type
        )
        
        return {
            "schema_type": schema_type.value,
            "recommendations": recommendations,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting simple recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Simple validation failed: {str(e)}")


@router.get("/schema-types")
async def get_supported_schema_types() -> List[str]:
    """Get a list of all supported schema types."""
    return [schema_type.value for schema_type in SchemaType]


# Authentication routes
@router.post("/auth/login")
async def login(request: Request, password: str = Form(...)):
    """Admin login endpoint."""
    try:
        if auth_manager.verify_password(password):
            # Create session
            token = auth_manager.create_session(request)
            
            # Create response with redirect to admin panel
            response = RedirectResponse(url="/static/admin.html", status_code=302)
            
            # Set secure cookie
            response.set_cookie(
                key="admin_session",
                value=token,
                max_age=3600,  # 1 hour
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="lax"
            )
            
            logger.info(f"Admin login successful from IP: {request.client.host if request.client else 'unknown'}")
            return response
        else:
            # Invalid password - redirect back to login
            response = RedirectResponse(url="/static/admin.html?error=invalid", status_code=302)
            logger.warning(f"Admin login failed from IP: {request.client.host if request.client else 'unknown'}")
            return response
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        response = RedirectResponse(url="/static/admin.html?error=server", status_code=302)
        return response


@router.post("/auth/logout")
async def logout(request: Request):
    """Admin logout endpoint."""
    try:
        token = auth_manager.get_session_token_from_request(request)
        if token:
            auth_manager.invalidate_session(token)
        
        response = RedirectResponse(url="/static/admin.html", status_code=302)
        response.delete_cookie("admin_session")
        
        logger.info("Admin logout successful")
        return response
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        response = RedirectResponse(url="/static/admin.html", status_code=302)
        return response


@router.get("/auth/status")
async def auth_status(request: Request) -> Dict[str, Any]:
    """Check authentication status."""
    try:
        authenticated = is_authenticated(request)
        return {
            "authenticated": authenticated,
            "active_sessions": auth_manager.get_session_count() if authenticated else 0
        }
    except Exception as e:
        logger.error(f"Auth status error: {e}")
        return {"authenticated": False, "active_sessions": 0}


@router.get("/best-practices")
async def get_best_practices(schema_type: SchemaType = None) -> List[Dict[str, Any]]:
    """
    Get best practices, optionally filtered by schema type.
    """
    try:
        if schema_type:
            practices = vector_store.get_all_practices_for_schema_type(schema_type)
        else:
            # Get all practices
            all_results = vector_store.collection.get()
            practices = []
            for i, doc in enumerate(all_results["documents"]):
                practices.append({
                    "id": all_results["ids"][i],
                    "content": doc,
                    "metadata": all_results["metadatas"][i]
                })
        
        return practices
        
    except Exception as e:
        logger.error(f"Error getting best practices: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get best practices: {str(e)}")


@router.post("/best-practices")
async def add_best_practice(
    practice: BestPractice,
    request: Request,
    _: bool = Depends(require_admin_auth)
) -> Dict[str, str]:
    """Add a new best practice to the vector store."""
    try:
        success = vector_store.add_best_practice(practice)
        if success:
            return {"message": f"Best practice {practice.id} added successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to add best practice")
            
    except Exception as e:
        logger.error(f"Error adding best practice: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add best practice: {str(e)}")


@router.put("/best-practices/{practice_id}")
async def update_best_practice(
    practice_id: str, 
    practice: BestPractice,
    request: Request,
    _: bool = Depends(require_admin_auth)
) -> Dict[str, str]:
    """Update an existing best practice."""
    try:
        # Ensure the practice ID matches
        practice.id = practice_id
        
        success = vector_store.update_practice(practice)
        if success:
            return {"message": f"Best practice {practice_id} updated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update best practice")
            
    except Exception as e:
        logger.error(f"Error updating best practice: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update best practice: {str(e)}")


@router.delete("/best-practices/{practice_id}")
async def delete_best_practice(
    practice_id: str,
    request: Request,
    _: bool = Depends(require_admin_auth)
) -> Dict[str, str]:
    """Delete a best practice from the vector store."""
    try:
        success = vector_store.delete_practice(practice_id)
        if success:
            return {"message": f"Best practice {practice_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Best practice not found")
            
    except Exception as e:
        logger.error(f"Error deleting best practice: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete best practice: {str(e)}")


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    try:
        # Test vector store connection
        _ = vector_store.collection.count()
        
        # Test AI service configuration
        ai_status = "available" if ai_service else "unavailable"
        ai_provider = ai_service.provider if ai_service else "none"
        
        return {
            "status": "healthy",
            "ai_service": ai_status,
            "ai_provider": ai_provider,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@router.get("/stats")
async def get_service_stats() -> Dict[str, Any]:
    """Get service statistics."""
    try:
        # Get vector store stats
        collection_count = vector_store.collection.count()
        
        return {
            "total_best_practices": collection_count,
            "supported_schema_types": len(SchemaType),
            "ai_provider": ai_service.provider if ai_service else "none",
            "ai_service_status": "available" if ai_service else "unavailable",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/config/model", response_model=ModelConfigResponse)
async def get_current_model() -> ModelConfigResponse:
    """Get the current GPT model configuration."""
    try:
        return ModelConfigResponse(current_model=settings.gpt_model)
    except Exception as e:
        logger.error(f"Error getting current model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get current model: {str(e)}")


@router.post("/config/model", response_model=ModelConfigResponse)
async def update_gpt_model(
    config_request: ModelConfigRequest,
    request: Request,
    _: bool = Depends(require_admin_auth)
) -> ModelConfigResponse:
    """Update the GPT model configuration."""
    try:
        # Validate the model name (basic validation)
        valid_models = [
            "gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo",
            "gpt-4", "gpt-4-turbo-preview"
        ]
        
        if config_request.model not in valid_models:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model. Must be one of: {', '.join(valid_models)}"
            )
        
        # Update the settings
        settings.gpt_model = config_request.model
        
        # Log the change
        logger.info(f"GPT model updated to: {config_request.model}")
        
        return ModelConfigResponse(
            current_model=config_request.model,
            message=f"Model updated to {config_request.model} successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update model: {str(e)}")


# Example schemas for testing
@router.get("/examples")
async def get_example_schemas() -> Dict[str, Dict[str, str]]:
    """Get example schemas for testing the service."""
    return {
        "avro": {
            "description": "Example Avro schema for user events (Venice/Espresso/Kafka)",
            "content": """{
  "type": "record",
  "name": "UserEvent",
  "namespace": "com.company.events",
  "fields": [
    {
      "name": "userId",
      "type": "long",
      "doc": "Unique user identifier"
    },
    {
      "name": "eventType",
      "type": {
        "type": "enum",
        "name": "EventType",
        "symbols": ["CLICK", "VIEW", "PURCHASE", "LOGIN"]
      },
      "doc": "Type of user event"
    },
    {
      "name": "timestamp",
      "type": "long",
      "doc": "Event timestamp in milliseconds"
    },
    {
      "name": "properties",
      "type": {
        "type": "map",
        "values": "string"
      },
      "default": {},
      "doc": "Additional event properties"
    }
  ]
}"""
        },
        "protobuf": {
            "description": "Example Protocol Buffers schema for Kafka messages",
            "content": """syntax = "proto3";

package com.company.messages;

message UserProfile {
  int64 user_id = 1;
  string email = 2;
  string first_name = 3;
  string last_name = 4;
  int32 age = 5;
  repeated string interests = 6;
  
  message Address {
    string street = 1;
    string city = 2;
    string country = 3;
    string postal_code = 4;
  }
  
  Address address = 7;
  int64 created_at = 8;
  int64 updated_at = 9;
}"""
        },
        "json_schema": {
            "description": "Example JSON Schema for Kafka/Pinot events",
            "content": """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "PageViewEvent",
  "properties": {
    "userId": {
      "type": "integer",
      "description": "Unique user identifier"
    },
    "sessionId": {
      "type": "string",
      "description": "Session identifier"
    },
    "pageUrl": {
      "type": "string",
      "format": "uri",
      "description": "URL of the viewed page"
    },
    "timestamp": {
      "type": "integer",
      "description": "Event timestamp in milliseconds"
    },
    "userAgent": {
      "type": "string",
      "description": "Browser user agent"
    },
    "referrer": {
      "type": "string",
      "format": "uri",
      "description": "Referrer URL"
    }
  },
  "required": ["userId", "sessionId", "pageUrl", "timestamp"]
}"""
        },
        "sql_ddl": {
            "description": "Example SQL DDL for MySQL/TiDB user table",
            "content": """CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);"""
        }
    } 