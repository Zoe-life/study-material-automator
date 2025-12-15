#!/usr/bin/env python3
"""
Example usage of the Study Material Automator

This demonstrates how to use the system programmatically.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.study_material_automator import StudyMaterialAutomator
from src.utils import Config


def example_with_pdf():
    """Example: Process a PDF file"""
    print("="*60)
    print("Example 1: Processing PDF Notes")
    print("="*60)
    
    # Initialize with config
    config = Config()
    
    # Validate API key is set
    if not config.openai_api_key:
        print("Error: Please set OPENAI_API_KEY in your .env file")
        return
    
    automator = StudyMaterialAutomator(config)
    
    # Process a PDF file
    pdf_path = "your_notes.pdf"  # Replace with actual PDF
    
    if os.path.exists(pdf_path):
        results = automator.process_materials(
            pdf_path=pdf_path,
            output_dir="example_output"
        )
        
        print("\nGenerated materials:")
        print(f"- {len(results['modules'])} modules")
        print(f"- {len(results['diagrams'])} diagrams")
        print(f"- {len(results['flashcards'])} flashcard sets")
        print(f"- {len(results['quizzes'])} quizzes")
    else:
        print(f"Note: {pdf_path} not found. This is just an example.")


def example_with_components():
    """Example: Using individual components"""
    print("\n" + "="*60)
    print("Example 2: Using Individual Components")
    print("="*60)
    
    from src.processors import PDFProcessor
    from src.utils import ContentAnalyzer
    
    # Initialize components
    pdf_processor = PDFProcessor()
    
    # This would work with a real PDF
    print("\nPDF Processor Features:")
    print("- Extract text from PDF")
    print("- Extract tables")
    print("- Identify headings")
    print("- Chunk content for processing")
    
    print("\nContent Analyzer Features:")
    print("- Analyze content structure")
    print("- Extract key concepts")
    print("- Simplify complex topics")
    print("- Identify concept relationships")


def example_flashcard_generation():
    """Example: Generate flashcards"""
    print("\n" + "="*60)
    print("Example 3: Flashcard Generation")
    print("="*60)
    
    from src.generators import FlashcardGenerator
    from src.utils import Config
    
    config = Config()
    
    if not config.openai_api_key:
        print("Set OPENAI_API_KEY to try this example")
        return
    
    # Sample content
    sample_content = """
    Machine Learning is a subset of artificial intelligence that enables 
    systems to learn and improve from experience without being explicitly 
    programmed. It focuses on developing computer programs that can access 
    data and use it to learn for themselves.
    """
    
    # Generate flashcards
    generator = FlashcardGenerator(api_key=config.openai_api_key)
    
    print("\nFlashcard Generator can create:")
    print("- Concept-based flashcards")
    print("- Definition flashcards")
    print("- Spaced repetition schedules")
    print("- Multiple export formats (JSON, TXT, CSV)")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("Study Material Automator - Usage Examples")
    print("="*60)
    
    example_with_pdf()
    example_with_components()
    example_flashcard_generation()
    
    print("\n" + "="*60)
    print("For real usage, see the main.py CLI:")
    print("  python main.py --pdf your_notes.pdf")
    print("  python main.py --video your_lecture.mp4")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
