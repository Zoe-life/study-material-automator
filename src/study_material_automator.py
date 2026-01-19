"""Main Study Material Automator Application"""
import os
import json
from typing import Dict, List, Optional

from .processors import PDFProcessor, VideoProcessor
from .generators import ModuleGenerator, DiagramGenerator, FlashcardGenerator, QuizGenerator
from .utils import ContentAnalyzer, Config


class StudyMaterialAutomator:
    """
    Main application class that orchestrates the conversion of
    educational content into structured study materials
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the automator
        
        Args:
            config: Configuration object (optional)
        """
        self.config = config or Config()
        
        if not self.config.validate():
            raise ValueError("Invalid configuration. Please set OPENAI_API_KEY.")
        
        # Initialize processors
        self.pdf_processor = PDFProcessor()
        self.video_processor = VideoProcessor(temp_dir=self.config.temp_dir)
        
        # Initialize generators
        self.content_analyzer = ContentAnalyzer(
            api_key=self.config.openai_api_key,
            model=self.config.openai_model
        )
        self.module_generator = ModuleGenerator(
            api_key=self.config.openai_api_key,
            model=self.config.openai_model
        )
        self.diagram_generator = DiagramGenerator(
            api_key=self.config.openai_api_key,
            model=self.config.openai_model
        )
        self.flashcard_generator = FlashcardGenerator(
            api_key=self.config.openai_api_key,
            model=self.config.openai_model
        )
        self.quiz_generator = QuizGenerator(
            api_key=self.config.openai_api_key,
            model=self.config.openai_model
        )
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """
        Process a PDF file and extract content
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted content dictionary
        """
        print(f"Processing PDF: {pdf_path}")
        content = self.pdf_processor.extract_text(pdf_path)
        print(f"Extracted {len(content['text'])} characters from {content['metadata']['num_pages']} pages")
        return content
    
    def process_video(self, video_source: str, extract_audio: bool = True) -> Dict:
        """
        Process a video file or URL
        
        Args:
            video_source: Video file path or URL
            extract_audio: Whether to extract and transcribe audio
            
        Returns:
            Video content dictionary
        """
        print(f"Processing video: {video_source}")
        
        # Get video info
        video_info = self.video_processor.get_video_info(video_source)
        
        content = {
            'metadata': video_info,
            'transcript': ''
        }
        
        if extract_audio:
            try:
                # Download if URL
                video_path = video_source
                if video_source.startswith('http'):
                    print("Downloading video...")
                    video_path = self.video_processor.download_video(video_source)
                
                # Extract audio
                print("Extracting audio...")
                audio_path = self.video_processor.extract_audio(video_path)
                
                # Transcribe
                print("Transcribing audio...")
                transcript = self.video_processor.transcribe_audio(
                    audio_path,
                    self.config.openai_api_key
                )
                content['transcript'] = transcript
                print(f"Transcribed {len(transcript)} characters")
            except Exception as e:
                print(f"Warning: Could not process video audio: {e}")
        
        return content
    
    def analyze_content(self, content: str) -> Dict:
        """
        Analyze content to extract structure and concepts
        
        Args:
            content: Text content to analyze
            
        Returns:
            Analysis results
        """
        print("Analyzing content...")
        analysis = self.content_analyzer.analyze_content(content)
        print(f"Found {len(analysis.get('main_topics', []))} main topics")
        return analysis
    
    def generate_study_materials(self, content: str, analysis: Dict,
                                output_dir: Optional[str] = None) -> Dict:
        """
        Generate all study materials from content
        
        Args:
            content: Source content
            analysis: Content analysis results
            output_dir: Directory to save outputs (optional)
            
        Returns:
            Dictionary with paths to generated materials
        """
        if not output_dir:
            output_dir = self.config.output_dir
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {
            'modules': [],
            'diagrams': [],
            'flashcards': [],
            'quizzes': []
        }
        
        # Generate modules
        print("\nGenerating learning modules...")
        modules = self.module_generator.generate_modules(content, analysis)
        
        for i, module in enumerate(modules, 1):
            module_path = os.path.join(output_dir, f"module_{i}.txt")
            self.module_generator.export_module(module, module_path)
            results['modules'].append(module_path)
            print(f"  Created module {i}: {module.get('title', 'Untitled')}")
            
            # Generate quiz for each module
            quiz = self.quiz_generator.generate_module_quiz(module)
            quiz_path = os.path.join(output_dir, f"module_{i}_quiz.txt")
            self.quiz_generator.export_quiz(quiz, quiz_path, format='txt')
            results['quizzes'].append(quiz_path)
            print(f"  Created quiz for module {i}")
        
        # Generate diagrams for main concepts
        print("\nGenerating concept diagrams...")
        concepts = analysis.get('concepts', {})
        diagram_count = 0
        for topic, topic_concepts in list(concepts.items())[:3]:  # Limit to 3 topics
            if topic_concepts:
                diagram_path = os.path.join(output_dir, f"diagram_{topic.replace(' ', '_')}.png")
                try:
                    self.diagram_generator.generate_concept_diagram(
                        topic, topic_concepts[:6], diagram_path
                    )
                    results['diagrams'].append(diagram_path)
                    diagram_count += 1
                    print(f"  Created diagram: {topic}")
                except Exception as e:
                    print(f"  Could not create diagram for {topic}: {e}")
        
        # Generate flashcards
        print("\nGenerating flashcards...")
        flashcards = self.flashcard_generator.generate_flashcards(content, num_cards=20)
        
        if flashcards:
            flashcard_path = os.path.join(output_dir, "flashcards.txt")
            self.flashcard_generator.export_flashcards(flashcards, flashcard_path, format='txt')
            results['flashcards'].append(flashcard_path)
            print(f"  Created {len(flashcards)} flashcards")
        
        # Generate overall quiz
        print("\nGenerating comprehensive quiz...")
        overall_quiz = self.quiz_generator.generate_quiz(content, num_questions=15)
        overall_quiz_path = os.path.join(output_dir, "comprehensive_quiz.txt")
        self.quiz_generator.export_quiz(overall_quiz, overall_quiz_path, format='txt')
        results['quizzes'].append(overall_quiz_path)
        print(f"  Created comprehensive quiz with {len(overall_quiz.get('questions', []))} questions")
        
        # Save summary
        summary = {
            'analysis': analysis,
            'modules': [os.path.basename(p) for p in results['modules']],
            'diagrams': [os.path.basename(p) for p in results['diagrams']],
            'flashcards': [os.path.basename(p) for p in results['flashcards']],
            'quizzes': [os.path.basename(p) for p in results['quizzes']]
        }
        
        summary_path = os.path.join(output_dir, "summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ All materials saved to: {output_dir}")
        print(f"  - {len(results['modules'])} modules")
        print(f"  - {len(results['diagrams'])} diagrams")
        print(f"  - {len(results['flashcards'])} flashcard sets")
        print(f"  - {len(results['quizzes'])} quizzes")
        
        return results
    
    def process_materials(self, pdf_path: Optional[str] = None,
                        video_source: Optional[str] = None,
                        output_dir: Optional[str] = None) -> Dict:
        """
        Process input materials and generate study materials
        
        Args:
            pdf_path: Path to PDF file (optional)
            video_source: Video file path or URL (optional)
            output_dir: Output directory (optional)
            
        Returns:
            Results dictionary
        """
        if not pdf_path and not video_source:
            raise ValueError("Must provide at least one input source (PDF or video)")
        
        # Collect content from all sources
        all_content = ""
        
        if pdf_path:
            pdf_content = self.process_pdf(pdf_path)
            all_content += pdf_content['text'] + "\n\n"
        
        if video_source:
            video_content = self.process_video(video_source)
            all_content += video_content.get('transcript', '') + "\n\n"
        
        if not all_content.strip():
            raise ValueError("No content could be extracted from input sources")
        
        # Analyze content
        analysis = self.analyze_content(all_content)
        
        # Generate study materials
        results = self.generate_study_materials(all_content, analysis, output_dir)
        
        return results
