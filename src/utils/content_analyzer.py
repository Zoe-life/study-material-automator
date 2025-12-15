"""Content Analysis Module using AI"""
import json
from typing import Dict, List, Optional
from openai import OpenAI


class ContentAnalyzer:
    """Analyzes content using AI to extract concepts, topics, and structure"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def analyze_content(self, content: str) -> Dict:
        """
        Analyze content to extract main topics and concepts
        
        Args:
            content: Text content to analyze
            
        Returns:
            Dictionary with analysis results
        """
        prompt = f"""Analyze the following educational content and provide:
1. Main topics covered (list of 3-7 topics)
2. Key concepts for each topic
3. Difficulty level (beginner, intermediate, advanced)
4. Suggested module structure

Content:
{content[:3000]}  # Limit to avoid token limits

Respond in JSON format:
{{
    "main_topics": ["topic1", "topic2", ...],
    "concepts": {{"topic1": ["concept1", "concept2"], ...}},
    "difficulty": "beginner/intermediate/advanced",
    "module_structure": ["module1 name", "module2 name", ...]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educator analyzing study materials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return {
                "main_topics": [],
                "concepts": {},
                "difficulty": "intermediate",
                "module_structure": []
            }
    
    def extract_key_concepts(self, content: str, num_concepts: int = 10) -> List[str]:
        """
        Extract key concepts from content
        
        Args:
            content: Text content
            num_concepts: Number of concepts to extract
            
        Returns:
            List of key concepts
        """
        prompt = f"""Extract the {num_concepts} most important concepts from this educational content.
List them in order of importance.

Content:
{content[:3000]}

Respond with a JSON array of concept strings."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at identifying key concepts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('concepts', [])
        except Exception as e:
            print(f"Error extracting concepts: {e}")
            return []
    
    def simplify_concept(self, concept: str, context: str = "") -> Dict[str, str]:
        """
        Break down a complex concept into simple explanation
        
        Args:
            concept: The concept to simplify
            context: Additional context
            
        Returns:
            Dictionary with simplified explanation
        """
        prompt = f"""Explain the following concept in simple terms that a beginner can understand.
Break it down into:
1. Simple definition (1-2 sentences)
2. Why it matters (1-2 sentences)
3. Real-world analogy or example
4. Common misconceptions (if any)

Concept: {concept}
Context: {context[:500] if context else 'General education'}

Respond in JSON format."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert teacher who excels at simplifying complex topics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error simplifying concept: {e}")
            return {
                "definition": concept,
                "importance": "",
                "example": "",
                "misconceptions": ""
            }
    
    def identify_relationships(self, concepts: List[str]) -> Dict[str, List[str]]:
        """
        Identify relationships between concepts
        
        Args:
            concepts: List of concepts
            
        Returns:
            Dictionary mapping concepts to related concepts
        """
        prompt = f"""Given these concepts, identify which ones are related and how:
{json.dumps(concepts)}

For each concept, list the related concepts and the nature of the relationship.
Respond in JSON format with concept names as keys and lists of related concepts as values."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at understanding relationships between concepts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error identifying relationships: {e}")
            return {}
