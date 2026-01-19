"""Module Generation for organizing content into digestible units"""
import json
from typing import Dict, List
from openai import OpenAI

# Maximum content length for module generation
MAX_MODULE_CONTENT_LENGTH = 2000


class ModuleGenerator:
    """Generates structured learning modules from content"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_modules(self, content: str, analysis: Dict) -> List[Dict]:
        """
        Generate learning modules from content
        
        Args:
            content: Source content
            analysis: Content analysis results
            
        Returns:
            List of module dictionaries
        """
        modules = []
        module_structure = analysis.get('module_structure', [])
        
        if not module_structure:
            # Create default structure based on topics
            module_structure = analysis.get('main_topics', ['Module 1'])
        
        for idx, module_name in enumerate(module_structure, 1):
            module = self._create_module(
                module_name=module_name,
                module_number=idx,
                content=content,
                concepts=analysis.get('concepts', {})
            )
            modules.append(module)
        
        return modules
    
    def _create_module(self, module_name: str, module_number: int, 
                      content: str, concepts: Dict) -> Dict:
        """
        Create a single module with structured content
        
        Args:
            module_name: Name of the module
            module_number: Module number
            content: Source content
            concepts: Concepts to cover
            
        Returns:
            Module dictionary
        """
        prompt = f"""Create a structured learning module for: {module_name}

Based on the source content, create a module that includes:
1. Module title and learning objectives (3-5 objectives)
2. Introduction (2-3 paragraphs)
3. Main content sections (3-5 sections with subsections)
4. Key takeaways (5-7 bullet points)
5. Prerequisites (if any)
6. Estimated study time

Source content:
{content[:MAX_MODULE_CONTENT_LENGTH]}

Respond in JSON format with the module structure."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert curriculum designer creating engaging learning modules."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            module = json.loads(response.choices[0].message.content)
            module['module_number'] = module_number
            module['module_name'] = module_name
            return module
        except Exception as e:
            print(f"Error creating module: {e}")
            return {
                'module_number': module_number,
                'module_name': module_name,
                'title': module_name,
                'learning_objectives': [],
                'introduction': '',
                'sections': [],
                'key_takeaways': []
            }
    
    def create_module_summary(self, module: Dict) -> str:
        """
        Create a text summary of a module
        
        Args:
            module: Module dictionary
            
        Returns:
            Formatted text summary
        """
        summary = f"""
{'='*60}
MODULE {module.get('module_number', 1)}: {module.get('title', module.get('module_name', 'Untitled'))}
{'='*60}

LEARNING OBJECTIVES:
"""
        for obj in module.get('learning_objectives', []):
            summary += f"  • {obj}\n"
        
        summary += f"\nINTRODUCTION:\n{module.get('introduction', '')}\n"
        
        summary += "\nMAIN CONTENT:\n"
        for section in module.get('sections', []):
            if isinstance(section, dict):
                summary += f"\n{section.get('title', 'Section')}:\n"
                summary += f"{section.get('content', '')}\n"
            else:
                summary += f"\n{section}\n"
        
        summary += "\nKEY TAKEAWAYS:\n"
        for takeaway in module.get('key_takeaways', []):
            summary += f"  ✓ {takeaway}\n"
        
        if module.get('estimated_time'):
            summary += f"\nEstimated Study Time: {module.get('estimated_time')}\n"
        
        return summary
    
    def export_module(self, module: Dict, output_path: str):
        """
        Export module to a file
        
        Args:
            module: Module dictionary
            output_path: Path to save the module
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if output_path.endswith('.json'):
                json.dump(module, f, indent=2, ensure_ascii=False)
            else:
                f.write(self.create_module_summary(module))
