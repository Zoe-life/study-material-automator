"""Diagram Generation Module"""
import json
import os
import math
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from openai import OpenAI

# Display formatting constants
MAX_DISPLAY_TEXT_LENGTH = 30


class DiagramGenerator:
    """Generates diagrams and visual illustrations for concepts"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_concept_diagram(self, concept: str, related_concepts: List[str],
                                output_path: str) -> str:
        """
        Generate a concept map diagram
        
        Args:
            concept: Main concept
            related_concepts: Related concepts
            output_path: Path to save the diagram
            
        Returns:
            Path to saved diagram
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Draw main concept in center
        center_x, center_y = 5, 5
        main_box = FancyBboxPatch(
            (center_x - 1, center_y - 0.5), 2, 1,
            boxstyle="round,pad=0.1",
            edgecolor='#2C3E50',
            facecolor='#3498DB',
            linewidth=2
        )
        ax.add_patch(main_box)
        ax.text(center_x, center_y, concept, ha='center', va='center',
                fontsize=12, fontweight='bold', color='white',
                wrap=True)
        
        # Draw related concepts around main concept
        num_related = len(related_concepts)
        if num_related > 0:
            for i, rel_concept in enumerate(related_concepts[:8]):  # Limit to 8
                angle = 2 * math.pi * i / min(num_related, 8)
                x = center_x + 3 * math.cos(angle)
                y = center_y + 3 * math.sin(angle)
                
                # Draw related concept box
                rel_box = FancyBboxPatch(
                    (x - 0.8, y - 0.4), 1.6, 0.8,
                    boxstyle="round,pad=0.05",
                    edgecolor='#34495E',
                    facecolor='#ECF0F1',
                    linewidth=1.5
                )
                ax.add_patch(rel_box)
                
                # Wrap text if too long
                display_text = rel_concept[:MAX_DISPLAY_TEXT_LENGTH] + '...' if len(rel_concept) > MAX_DISPLAY_TEXT_LENGTH else rel_concept
                ax.text(x, y, display_text, ha='center', va='center',
                       fontsize=9, wrap=True)
                
                # Draw arrow from main to related
                arrow = FancyArrowPatch(
                    (center_x, center_y),
                    (x, y),
                    arrowstyle='->,head_width=0.4,head_length=0.4',
                    color='#95A5A6',
                    linewidth=1.5,
                    alpha=0.7
                )
                ax.add_patch(arrow)
        
        plt.title(f'Concept Map: {concept}', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_flow_diagram(self, steps: List[str], title: str,
                            output_path: str) -> str:
        """
        Generate a flow diagram showing process steps
        
        Args:
            steps: List of steps in the process
            title: Diagram title
            output_path: Path to save the diagram
            
        Returns:
            Path to saved diagram
        """
        fig, ax = plt.subplots(figsize=(10, 2 + len(steps) * 1.5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(steps) + 1)
        ax.axis('off')
        
        colors = ['#3498DB', '#2ECC71', '#F39C12', '#E74C3C', '#9B59B6', '#1ABC9C']
        
        for i, step in enumerate(steps):
            y = len(steps) - i
            color = colors[i % len(colors)]
            
            # Draw step box
            box = FancyBboxPatch(
                (1, y - 0.4), 8, 0.8,
                boxstyle="round,pad=0.1",
                edgecolor=color,
                facecolor=color,
                linewidth=2,
                alpha=0.7
            )
            ax.add_patch(box)
            
            # Add step number and text
            step_text = f"{i+1}. {step}"
            if len(step_text) > 60:
                step_text = step_text[:57] + '...'
            ax.text(5, y, step_text, ha='center', va='center',
                   fontsize=10, fontweight='bold', color='white')
            
            # Draw arrow to next step
            if i < len(steps) - 1:
                arrow = FancyArrowPatch(
                    (5, y - 0.5),
                    (5, y - 1.1),
                    arrowstyle='->,head_width=0.4,head_length=0.4',
                    color='#34495E',
                    linewidth=2
                )
                ax.add_patch(arrow)
        
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_hierarchy_diagram(self, hierarchy: Dict, title: str,
                                  output_path: str) -> str:
        """
        Generate a hierarchical diagram
        
        Args:
            hierarchy: Dictionary representing hierarchy
            title: Diagram title
            output_path: Path to save the diagram
            
        Returns:
            Path to saved diagram
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Draw root
        root_name = list(hierarchy.keys())[0] if hierarchy else "Root"
        root_box = FancyBboxPatch(
            (4, 8.5), 2, 0.8,
            boxstyle="round,pad=0.1",
            edgecolor='#2C3E50',
            facecolor='#3498DB',
            linewidth=2
        )
        ax.add_patch(root_box)
        ax.text(5, 8.9, root_name[:20], ha='center', va='center',
               fontsize=11, fontweight='bold', color='white')
        
        # Draw children if present
        children = hierarchy.get(root_name, []) if isinstance(hierarchy.get(root_name), list) else []
        if children:
            num_children = len(children[:5])  # Limit to 5
            spacing = 8 / (num_children + 1)
            
            for i, child in enumerate(children[:5]):
                x = spacing * (i + 1) + 1
                y = 6
                
                child_box = FancyBboxPatch(
                    (x - 0.8, y - 0.4), 1.6, 0.8,
                    boxstyle="round,pad=0.05",
                    edgecolor='#34495E',
                    facecolor='#ECF0F1',
                    linewidth=1.5
                )
                ax.add_patch(child_box)
                
                child_text = child[:15] + '...' if len(child) > 15 else child
                ax.text(x, y, child_text, ha='center', va='center',
                       fontsize=9)
                
                # Draw connecting line
                ax.plot([5, x], [8.5, y + 0.4], 'k-', linewidth=1.5, alpha=0.5)
        
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_diagram_description(self, concept: str, diagram_type: str = "concept_map") -> Dict:
        """
        Use AI to determine what should be in a diagram
        
        Args:
            concept: Concept to diagram
            diagram_type: Type of diagram to create
            
        Returns:
            Dictionary with diagram specifications
        """
        prompt = f"""Create a specification for a {diagram_type} diagram about: {concept}

Provide:
1. Main elements to include
2. Relationships between elements
3. Labels and annotations
4. Suggested layout

Respond in JSON format."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating educational diagrams."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating diagram description: {e}")
            return {}
