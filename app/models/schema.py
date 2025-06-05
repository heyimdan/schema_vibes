from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class SchemaType(str, Enum):
    JSON_SCHEMA = "json_schema"
    AVRO = "avro"
    PROTOBUF = "protobuf"
    SQL_DDL = "sql_ddl"
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
    REDSHIFT = "redshift"


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Platform(str, Enum):
    VENICE = "venice"
    ESPRESSO = "espresso"
    KAFKA = "kafka"
    PINOT = "pinot"
    MYSQL = "mysql"
    TIDB = "tidb"
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"


class SchemaValidationRequest(BaseModel):
    schema_content: str = Field(..., description="The schema content to validate")
    schema_type: SchemaType = Field(..., description="Type of schema")
    context: Optional[str] = Field(None, description="Additional context about the schema usage")
    include_best_practices: bool = Field(True, description="Include best practices in the analysis")
    platform: Optional[Platform] = Field(None, description="Target data platform for platform-specific recommendations")


class Recommendation(BaseModel):
    category: str = Field(..., description="Category of the recommendation")
    severity: SeverityLevel = Field(..., description="Severity level of the issue")
    description: str = Field(..., description="Detailed description of the issue")
    suggestion: str = Field(..., description="Specific improvement suggestion")
    impact: str = Field(..., description="Expected impact of implementing the change")


class SchemaValidationResponse(BaseModel):
    schema_id: Optional[str] = Field(None, description="Unique identifier for this validation")
    overall_score: int = Field(..., ge=1, le=10, description="Overall schema quality score (1-10)")
    recommendations: List[Recommendation] = Field(..., description="List of recommendations")
    best_practices_applied: List[str] = Field(..., description="Best practices already applied in the schema")
    missing_best_practices: List[str] = Field(..., description="Best practices missing from the schema")
    summary: str = Field(..., description="Overall summary of schema quality")
    processing_time: Optional[float] = Field(None, description="Time taken to process the request")


class BestPractice(BaseModel):
    id: str = Field(..., description="Unique identifier for the best practice")
    title: str = Field(..., description="Title of the best practice")
    description: str = Field(..., description="Detailed description")
    category: str = Field(..., description="Category (naming, indexing, normalization, etc.)")
    applicable_schema_types: List[SchemaType] = Field(..., description="Schema types this practice applies to")
    applicable_platforms: List[Platform] = Field(default=[], description="Platforms this practice applies to (empty = all platforms)")
    examples: List[str] = Field(default=[], description="Examples of good and bad practices")
    severity_if_missing: SeverityLevel = Field(..., description="Severity if this practice is missing")


class ValidationHistory(BaseModel):
    id: str = Field(..., description="Unique identifier")
    schema_type: SchemaType = Field(..., description="Type of schema validated")
    schema_hash: str = Field(..., description="Hash of the schema content")
    overall_score: int = Field(..., description="Overall score given")
    recommendations_count: int = Field(..., description="Number of recommendations provided")
    timestamp: str = Field(..., description="When the validation was performed")
    user_id: Optional[str] = Field(None, description="User who requested the validation") 