import openai
import anthropic
import json
from typing import Dict, Any, List
from app.core.config import settings, SCHEMA_ANALYSIS_PROMPT
from app.models.schema import SchemaValidationRequest, SchemaValidationResponse, Recommendation, SchemaType, Platform
from app.services.vector_store import VectorStoreService
from loguru import logger
import time


class AIService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        
        # Get decrypted API keys
        openai_key = settings.get_decrypted_openai_key()
        anthropic_key = settings.get_decrypted_anthropic_key()
        
        if settings.ai_provider == "openai" and openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
            self.provider = "openai"
        elif settings.ai_provider == "anthropic" and anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            self.provider = "anthropic"
        else:
            raise ValueError("No valid AI provider configuration found")
    
    async def analyze_schema(self, request: SchemaValidationRequest) -> SchemaValidationResponse:
        """Analyze a schema and provide recommendations."""
        start_time = time.time()
        
        try:
            # Get relevant best practices from vector store
            best_practices_context = ""
            if request.include_best_practices:
                best_practices_context = self._get_best_practices_context(
                    request.schema_content, 
                    request.schema_type,
                    request.platform
                )
            
            # Prepare the prompt
            analysis_prompt = SCHEMA_ANALYSIS_PROMPT.format(
                schema_type=request.schema_type.value,
                schema_content=request.schema_content,
                best_practices_context=best_practices_context
            )
            
            # Get AI analysis
            ai_response = await self._get_ai_analysis(analysis_prompt)
            
            # Parse the response
            analysis_result = self._parse_ai_response(ai_response)
            
            # Create response
            processing_time = time.time() - start_time
            
            response = SchemaValidationResponse(
                overall_score=analysis_result.get("overall_score", 5),
                recommendations=[
                    Recommendation(**rec) for rec in analysis_result.get("recommendations", [])
                ],
                best_practices_applied=analysis_result.get("best_practices_applied", []),
                missing_best_practices=analysis_result.get("missing_best_practices", []),
                summary=analysis_result.get("summary", "Schema analysis completed"),
                processing_time=processing_time
            )
            
            logger.info(f"Schema analysis completed in {processing_time:.2f}s with score {response.overall_score}")
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing schema: {e}")
            # Return a basic response with error info
            return SchemaValidationResponse(
                overall_score=1,
                recommendations=[
                    Recommendation(
                        category="error",
                        severity="high",
                        description=f"Failed to analyze schema: {str(e)}",
                        suggestion="Please check the schema format and try again",
                        impact="Cannot provide recommendations due to analysis failure"
                    )
                ],
                best_practices_applied=[],
                missing_best_practices=[],
                summary="Analysis failed due to error",
                processing_time=time.time() - start_time
            )
    
    def _get_best_practices_context(self, schema_content: str, schema_type: SchemaType, platform=None) -> str:
        """Get relevant best practices context from vector store."""
        try:
            # Search for practices relevant to the schema content
            relevant_practices = self.vector_store.search_relevant_practices(
                query=schema_content[:500],  # Limit query length
                schema_type=schema_type,
                platform=platform,
                limit=5
            )
            
            # Also get all practices for this schema type
            type_practices = self.vector_store.get_all_practices_for_schema_type(schema_type)
            
            # Combine and deduplicate
            all_practices = {p["id"]: p for p in relevant_practices + type_practices}
            
            # Format as context
            context_parts = []
            for practice in all_practices.values():
                metadata = practice["metadata"]
                examples = json.loads(metadata.get("examples", "[]"))
                
                context_part = f"""
**{metadata.get('category', 'general').title()} Best Practice:**
{practice['content']}
Examples: {'; '.join(examples) if examples else 'None'}
Severity if missing: {metadata.get('severity', 'medium')}
"""
                context_parts.append(context_part)
            
            return "\n".join(context_parts)
            
        except Exception as e:
            logger.error(f"Error getting best practices context: {e}")
            return "Best practices context unavailable"
    
    async def _get_ai_analysis(self, prompt: str) -> str:
        """Get analysis from the configured AI provider."""
        try:
            if self.provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model=settings.gpt_model,
                    messages=[
                        {"role": "system", "content": "You are an expert database schema architect."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif self.provider == "anthropic":
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    temperature=0.1,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
                
        except Exception as e:
            logger.error(f"Error getting AI analysis: {e}")
            raise
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response into structured format."""
        try:
            # Try to extract JSON from the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: create a basic structure
                return self._create_fallback_response(response)
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse AI response as JSON, using fallback")
            return self._create_fallback_response(response)
    
    def _create_fallback_response(self, response: str) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails."""
        return {
            "overall_score": 5,
            "recommendations": [
                {
                    "category": "analysis",
                    "severity": "medium",
                    "description": "AI analysis completed but response format was non-standard",
                    "suggestion": response[:500] + "..." if len(response) > 500 else response,
                    "impact": "Manual review recommended"
                }
            ],
            "best_practices_applied": [],
            "missing_best_practices": ["Unable to determine from response"],
            "summary": "Analysis completed with parsing issues"
        }
    
    async def get_schema_recommendations_only(self, schema_content: str, schema_type: SchemaType) -> List[str]:
        """Get a simple list of recommendations without full analysis."""
        try:
            simple_prompt = f"""
Analyze this {schema_type.value} schema and provide 3-5 key improvement recommendations:

{schema_content}

Provide only a numbered list of specific, actionable recommendations.
"""
            
            if self.provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model=settings.gpt_model,
                    messages=[
                        {"role": "system", "content": "You are an expert database schema architect."},
                        {"role": "user", "content": simple_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=1000
                ).choices[0].message.content
            else:
                response = await self._get_ai_analysis(simple_prompt)
            
            # Parse simple recommendations
            recommendations = []
            for line in response.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                    # Clean up the line
                    clean_line = line.lstrip('0123456789.-* ')
                    if clean_line:
                        recommendations.append(clean_line)
            
            return recommendations[:5]  # Limit to 5 recommendations
            
        except Exception as e:
            logger.error(f"Error getting simple recommendations: {e}")
            return [f"Error getting recommendations: {str(e)}"] 