import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.models.schema import BestPractice, SchemaType, Platform
from loguru import logger
import json
import os


class VectorStoreService:
    def __init__(self):
        # Ensure the persist directory exists
        self._ensure_persist_directory()
        
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        self.collection = self._get_or_create_collection()
    
    def _ensure_persist_directory(self):
        """Ensure the ChromaDB persistence directory exists."""
        persist_dir = settings.chroma_persist_directory
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(persist_dir, exist_ok=True)
            
            # Check if directory is writable
            test_file = os.path.join(persist_dir, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            logger.info(f"ChromaDB persistence directory ready: {persist_dir}")
            
        except Exception as e:
            logger.error(f"Failed to setup ChromaDB persistence directory {persist_dir}: {e}")
            raise
    
    def _get_or_create_collection(self):
        """Get or create the best practices collection."""
        try:
            collection = self.client.get_collection(name=settings.collection_name)
            logger.info(f"Retrieved existing collection: {settings.collection_name}")
        except ValueError:
            collection = self.client.create_collection(
                name=settings.collection_name,
                metadata={"description": "Schema validation best practices"}
            )
            logger.info(f"Created new collection: {settings.collection_name}")
            
            # Only populate initial best practices if enabled (disabled in production)
            if settings.auto_populate_defaults:
                logger.info("Auto-populating default best practices (development mode)")
                self._populate_initial_best_practices(collection)
            else:
                logger.info("Skipping auto-population of defaults (production mode)")
        
        return collection
    
    def _populate_initial_best_practices(self, collection):
        """Populate the collection with initial best practices."""
        initial_practices = self._get_initial_best_practices()
        
        documents = []
        metadatas = []
        ids = []
        
        for practice in initial_practices:
            documents.append(f"{practice.title}: {practice.description}")
            metadatas.append({
                "category": practice.category,
                "schema_types": json.dumps([st.value for st in practice.applicable_schema_types]),
                "platforms": json.dumps([p.value for p in practice.applicable_platforms]),
                "severity": practice.severity_if_missing.value,
                "examples": json.dumps(practice.examples)
            })
            ids.append(practice.id)
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Populated collection with {len(initial_practices)} best practices")
    
    def _get_initial_best_practices(self) -> List[BestPractice]:
        """Get the initial set of best practices."""
        return [
            BestPractice(
                id="naming_001",
                title="Use Clear and Descriptive Field Names",
                description="Field names should be self-documenting and follow consistent naming conventions. Avoid abbreviations and single-letter names.",
                category="naming",
                applicable_schema_types=[st for st in SchemaType],
                examples=[
                    "Good: customer_email, order_total_amount",
                    "Bad: ce, ota, x, temp"
                ],
                severity_if_missing="medium"
            ),
            BestPractice(
                id="naming_002",
                title="Use Consistent Naming Convention",
                description="Stick to one naming convention throughout the schema (snake_case, camelCase, or PascalCase).",
                category="naming",
                applicable_schema_types=[st for st in SchemaType],
                examples=[
                    "Good: user_name, first_name, last_name (all snake_case)",
                    "Bad: userName, first_name, LastName (mixed conventions)"
                ],
                severity_if_missing="low"
            ),
            BestPractice(
                id="types_001",
                title="Use Appropriate Data Types",
                description="Choose the most specific and appropriate data type for each field to ensure data integrity and optimal storage.",
                category="data_types",
                applicable_schema_types=[st for st in SchemaType],
                examples=[
                    "Good: Use INTEGER for IDs, DECIMAL for currency, TIMESTAMP for dates",
                    "Bad: Use VARCHAR for everything"
                ],
                severity_if_missing="high"
            ),
            BestPractice(
                id="constraints_001",
                title="Define NOT NULL Constraints",
                description="Explicitly define which fields are required by adding NOT NULL constraints where appropriate.",
                category="constraints",
                applicable_schema_types=[SchemaType.SQL_DDL, SchemaType.BIGQUERY, SchemaType.SNOWFLAKE, SchemaType.REDSHIFT],
                examples=[
                    "Good: customer_id INTEGER NOT NULL",
                    "Bad: customer_id INTEGER (allowing nulls for required field)"
                ],
                severity_if_missing="medium"
            ),
            BestPractice(
                id="indexing_001",
                title="Add Indexes for Query Performance",
                description="Create indexes on columns that are frequently used in WHERE clauses, JOIN conditions, or ORDER BY clauses.",
                category="indexing",
                applicable_schema_types=[SchemaType.SQL_DDL, SchemaType.BIGQUERY, SchemaType.SNOWFLAKE, SchemaType.REDSHIFT],
                examples=[
                    "Good: CREATE INDEX idx_customer_email ON customers(email)",
                    "Missing: No indexes on frequently queried columns"
                ],
                severity_if_missing="medium"
            ),
            BestPractice(
                id="documentation_001",
                title="Add Field Descriptions",
                description="Include meaningful descriptions or comments for fields to make the schema self-documenting.",
                category="documentation",
                applicable_schema_types=[st for st in SchemaType],
                examples=[
                    "Good: 'customer_lifetime_value': {'type': 'number', 'description': 'Total revenue from customer in USD'}",
                    "Bad: 'clv': {'type': 'number'}"
                ],
                severity_if_missing="low"
            ),
            BestPractice(
                id="normalization_001",
                title="Follow Normalization Principles",
                description="Normalize data to reduce redundancy, but consider denormalization for read-heavy workloads.",
                category="normalization",
                applicable_schema_types=[SchemaType.SQL_DDL, SchemaType.BIGQUERY, SchemaType.SNOWFLAKE, SchemaType.REDSHIFT],
                examples=[
                    "Good: Separate customer and order tables with foreign key relationships",
                    "Bad: Storing customer details in every order record"
                ],
                severity_if_missing="medium"
            ),
            BestPractice(
                id="security_001",
                title="Protect Sensitive Data",
                description="Mark sensitive fields appropriately and consider encryption or masking for PII data.",
                category="security",
                applicable_schema_types=[st for st in SchemaType],
                examples=[
                    "Good: Mark SSN, credit card fields as sensitive with encryption",
                    "Bad: Store sensitive data in plain text without protection"
                ],
                severity_if_missing="high"
            ),
            # Venice-specific best practices
            BestPractice(
                id="venice_001",
                title="Use Avro Schema Evolution",
                description="Venice uses Avro for schema evolution. Design schemas to be forward and backward compatible.",
                category="schema_evolution",
                applicable_schema_types=[SchemaType.AVRO],
                applicable_platforms=[Platform.VENICE],
                examples=[
                    "Good: Add new fields with default values, avoid removing required fields",
                    "Bad: Removing fields or changing field types without compatibility"
                ],
                severity_if_missing="high"
            ),
            BestPractice(
                id="venice_002", 
                title="Optimize for Venice Storage",
                description="Venice is optimized for read-heavy workloads. Design schemas with query patterns in mind.",
                category="performance",
                applicable_schema_types=[SchemaType.AVRO],
                applicable_platforms=[Platform.VENICE],
                examples=[
                    "Good: Denormalize data for common query patterns",
                    "Bad: Highly normalized schemas requiring complex joins"
                ],
                severity_if_missing="medium"
            ),
            # BigQuery-specific practices
            BestPractice(
                id="bigquery_001",
                title="Use Nested and Repeated Fields",
                description="BigQuery supports nested and repeated fields efficiently. Use them to denormalize data.",
                category="data_modeling",
                applicable_schema_types=[SchemaType.BIGQUERY],
                applicable_platforms=[Platform.BIGQUERY],
                examples=[
                    "Good: STRUCT<name STRING, email STRING> for user info",
                    "Bad: Separate tables with JOINs for simple relationships"
                ],
                severity_if_missing="medium"
            ),
            # Snowflake-specific practices
            BestPractice(
                id="snowflake_001",
                title="Use Clustering Keys",
                description="Snowflake benefits from clustering keys on large tables for query performance.",
                category="performance",
                applicable_schema_types=[SchemaType.SNOWFLAKE],
                applicable_platforms=[Platform.SNOWFLAKE],
                examples=[
                    "Good: CLUSTER BY (date, region) for time-series data",
                    "Bad: No clustering on large frequently-queried tables"
                ],
                severity_if_missing="medium"
            )
        ]
    
    def add_best_practice(self, practice: BestPractice) -> bool:
        """Add a new best practice to the vector store."""
        try:
            self.collection.add(
                documents=[f"{practice.title}: {practice.description}"],
                metadatas=[{
                    "category": practice.category,
                    "schema_types": json.dumps([st.value for st in practice.applicable_schema_types]),
                    "platforms": json.dumps([p.value for p in practice.applicable_platforms]),
                    "severity": practice.severity_if_missing.value,
                    "examples": json.dumps(practice.examples)
                }],
                ids=[practice.id]
            )
            logger.info(f"Added best practice: {practice.id}")
            return True
        except Exception as e:
            logger.error(f"Error adding best practice {practice.id}: {e}")
            return False
    
    def search_relevant_practices(self, query: str, schema_type: SchemaType, platform: Optional[Platform] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant best practices based on query, schema type, and optionally platform."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit * 2  # Get more results to allow for filtering
            )
            
            practices = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i]
                    
                    # Filter by schema type
                    schema_types_str = metadata.get("schema_types", "[]")
                    platforms_str = metadata.get("platforms", "[]")
                    
                    try:
                        schema_types = json.loads(schema_types_str)
                        platforms = json.loads(platforms_str)
                        
                        # Check schema type match
                        if schema_type.value not in schema_types:
                            continue
                            
                        # Check platform match (if platform is specified)
                        if platform:
                            # If platforms list is empty, it applies to all platforms
                            # Otherwise, check if the specified platform is in the list
                            if platforms and platform.value not in platforms:
                                continue
                        
                        practices.append({
                            "id": results["ids"][0][i],
                            "content": doc,
                            "metadata": metadata,
                            "distance": results["distances"][0][i] if "distances" in results else None
                        })
                        
                        # Stop if we have enough results
                        if len(practices) >= limit:
                            break
                            
                    except json.JSONDecodeError:
                        # Skip if metadata is malformed
                        continue
            
            logger.info(f"Found {len(practices)} relevant practices for query: {query}, schema_type: {schema_type.value}, platform: {platform.value if platform else 'any'}")
            return practices
            
        except Exception as e:
            logger.error(f"Error searching best practices: {e}")
            return []
    
    def get_all_practices_for_schema_type(self, schema_type: SchemaType) -> List[Dict[str, Any]]:
        """Get all best practices applicable to a specific schema type."""
        try:
            # Get all documents first, then filter
            all_results = self.collection.get()
            
            practices = []
            for i, metadata in enumerate(all_results["metadatas"]):
                schema_types_str = metadata.get("schema_types", "[]")
                try:
                    schema_types = json.loads(schema_types_str)
                    if schema_type.value in schema_types:
                        practices.append({
                            "id": all_results["ids"][i],
                            "content": all_results["documents"][i],
                            "metadata": metadata
                        })
                except json.JSONDecodeError:
                    # Skip if schema_types is malformed
                    continue
            
            logger.info(f"Found {len(practices)} practices for schema type: {schema_type.value}")
            return practices
            
        except Exception as e:
            logger.error(f"Error getting practices for schema type {schema_type.value}: {e}")
            return []
    
    def update_practice(self, practice: BestPractice) -> bool:
        """Update an existing best practice."""
        try:
            self.collection.update(
                ids=[practice.id],
                documents=[f"{practice.title}: {practice.description}"],
                metadatas=[{
                    "category": practice.category,
                    "schema_types": json.dumps([st.value for st in practice.applicable_schema_types]),
                    "platforms": json.dumps([p.value for p in practice.applicable_platforms]),
                    "severity": practice.severity_if_missing.value,
                    "examples": json.dumps(practice.examples)
                }]
            )
            logger.info(f"Updated best practice: {practice.id}")
            return True
        except Exception as e:
            logger.error(f"Error updating best practice {practice.id}: {e}")
            return False
    
    def delete_practice(self, practice_id: str) -> bool:
        """Delete a best practice from the vector store."""
        try:
            self.collection.delete(ids=[practice_id])
            logger.info(f"Deleted best practice: {practice_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting best practice {practice_id}: {e}")
            return False 