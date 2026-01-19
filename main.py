#!/usr/bin/env python3
"""Command-line interface for Study Material Automator"""
import argparse
import sys
import os

from src.study_material_automator import StudyMaterialAutomator
from src.utils import Config


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Study Material Automator - Convert PDFs and videos into structured study materials",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a PDF file
  python main.py --pdf notes.pdf
  
  # Process a video URL
  python main.py --video https://youtube.com/watch?v=example
  
  # Process both PDF and video
  python main.py --pdf notes.pdf --video lecture.mp4
  
  # Specify custom output directory
  python main.py --pdf notes.pdf --output my_study_materials
        """
    )
    
    parser.add_argument(
        '--pdf',
        type=str,
        help='Path to PDF file containing class notes'
    )
    
    parser.add_argument(
        '--video',
        type=str,
        help='Path to video file or video URL (e.g., YouTube)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory for generated materials (default: output)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to .env configuration file'
    )
    
    parser.add_argument(
        '--no-video-audio',
        action='store_true',
        help='Skip audio extraction and transcription for videos'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.pdf and not args.video:
        parser.error("Must provide at least one input source (--pdf or --video)")
    
    if args.pdf and not os.path.exists(args.pdf):
        print(f"Error: PDF file not found: {args.pdf}", file=sys.stderr)
        sys.exit(1)
    
    # Load configuration
    try:
        config = Config(env_file=args.config)
        if not config.validate():
            print("Error: Configuration validation failed.", file=sys.stderr)
            print("Make sure OPENAI_API_KEY is set in your .env file or environment.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Override output directory if specified
    if args.output:
        config.output_dir = args.output
    
    # Initialize automator
    print("="*60)
    print("Study Material Automator")
    print("="*60)
    print()
    
    try:
        automator = StudyMaterialAutomator(config)
        
        # Process materials
        results = automator.process_materials(
            pdf_path=args.pdf,
            video_source=args.video,
            output_dir=config.output_dir
        )
        
        print("\n" + "="*60)
        print("✓ Processing Complete!")
        print("="*60)
        print(f"\nStudy materials have been generated in: {config.output_dir}")
        print("\nGenerated files:")
        for category, files in results.items():
            if files:
                print(f"\n{category.title()}:")
                for file in files:
                    print(f"  • {os.path.basename(file)}")
        
        print("\nYou can now:")
        print("  1. Review the modules to learn the content")
        print("  2. Study the flashcards for memorization")
        print("  3. Take the quizzes to test your understanding")
        print("  4. Refer to the diagrams for visual learning")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
