# Study Material Automator - Complete Usage Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Command Line Usage](#command-line-usage)
5. [Python API Usage](#python-api-usage)
6. [Output Formats](#output-formats)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Process your materials
python main.py --pdf your_notes.pdf

# 4. Check the output directory
ls output/
```

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video processing)
- OpenAI API key

### Install FFmpeg

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install as a package:
```bash
pip install -e .
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional (with defaults)
OPENAI_MODEL=gpt-4                 # or gpt-3.5-turbo for faster/cheaper
OPENAI_TEMPERATURE=0.7             # 0.0-1.0, higher = more creative
OUTPUT_DIR=output                  # where to save materials
TEMP_DIR=temp                      # temporary files
```

### Getting an OpenAI API Key

1. Visit https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new key
5. Copy and paste into your `.env` file

## Command Line Usage

### Basic Commands

**Process a PDF:**
```bash
python main.py --pdf path/to/notes.pdf
```

**Process a video:**
```bash
python main.py --video path/to/lecture.mp4
```

**Process a YouTube video:**
```bash
python main.py --video "https://youtube.com/watch?v=VIDEO_ID"
```

**Process both PDF and video:**
```bash
python main.py --pdf notes.pdf --video lecture.mp4
```

### Advanced Options

**Custom output directory:**
```bash
python main.py --pdf notes.pdf --output my_study_materials
```

**Custom config file:**
```bash
python main.py --pdf notes.pdf --config custom.env
```

**Skip video transcription (faster):**
```bash
python main.py --video lecture.mp4 --no-video-audio
```

### Full Command Reference

```
python main.py [OPTIONS]

Options:
  --pdf PATH              Path to PDF file
  --video PATH            Path to video file or URL
  --output, -o DIR        Output directory (default: output)
  --config PATH           Path to .env config file
  --no-video-audio        Skip audio extraction/transcription
  --help                  Show help message
```

## Python API Usage

### Basic Usage

```python
from src.study_material_automator import StudyMaterialAutomator
from src.utils import Config

# Initialize
config = Config()
automator = StudyMaterialAutomator(config)

# Process materials
results = automator.process_materials(
    pdf_path="notes.pdf",
    video_source="lecture.mp4",
    output_dir="output"
)

# Access results
print(f"Modules: {results['modules']}")
print(f"Quizzes: {results['quizzes']}")
```

### Using Individual Components

**PDF Processing:**
```python
from src.processors import PDFProcessor

processor = PDFProcessor()
content = processor.extract_text("notes.pdf")

print(f"Extracted {len(content['text'])} characters")
print(f"Found {len(content['tables'])} tables")
```

**Content Analysis:**
```python
from src.utils import ContentAnalyzer, Config

config = Config()
analyzer = ContentAnalyzer(api_key=config.openai_api_key)

analysis = analyzer.analyze_content(text_content)
print(f"Topics: {analysis['main_topics']}")
```

**Flashcard Generation:**
```python
from src.generators import FlashcardGenerator
from src.utils import Config

config = Config()
generator = FlashcardGenerator(api_key=config.openai_api_key)

flashcards = generator.generate_flashcards(content, num_cards=20)
generator.export_flashcards(flashcards, "flashcards.txt", format='txt')
```

**Quiz Generation:**
```python
from src.generators import QuizGenerator
from src.utils import Config

config = Config()
generator = QuizGenerator(api_key=config.openai_api_key)

quiz = generator.generate_quiz(content, num_questions=10)
generator.export_quiz(quiz, "quiz.txt", format='txt')
```

**Diagram Generation:**
```python
from src.generators import DiagramGenerator
from src.utils import Config

config = Config()
generator = DiagramGenerator(api_key=config.openai_api_key)

# Create concept map
generator.generate_concept_diagram(
    concept="Machine Learning",
    related_concepts=["Neural Networks", "Deep Learning", "Supervised Learning"],
    output_path="concept_map.png"
)
```

## Output Formats

### Directory Structure

```
output/
├── module_1.txt              # Module 1 content
├── module_1_quiz.txt         # Quiz for module 1
├── module_2.txt              # Module 2 content
├── module_2_quiz.txt         # Quiz for module 2
├── diagram_Topic1.png        # Visual diagram
├── flashcards.txt            # Study flashcards
├── comprehensive_quiz.txt    # Overall quiz
└── summary.json              # Summary metadata
```

### Module Format

Each module includes:
- Learning objectives
- Introduction
- Main content sections
- Key takeaways
- Estimated study time

### Quiz Format

Quizzes include:
- Multiple choice questions
- True/False questions
- Short answer questions
- Correct answers
- Explanations

### Flashcard Format

Flashcards include:
- Question (front)
- Answer (back)
- Hints
- Difficulty level
- Spaced repetition schedule

## Advanced Features

### Custom Module Generation

```python
from src.generators import ModuleGenerator
from src.utils import Config

config = Config()
generator = ModuleGenerator(api_key=config.openai_api_key)

# Generate modules with custom structure
analysis = {
    'main_topics': ['Topic A', 'Topic B'],
    'module_structure': ['Introduction', 'Core Concepts', 'Advanced Topics']
}

modules = generator.generate_modules(content, analysis)
```

### Spaced Repetition Schedule

```python
from src.generators import FlashcardGenerator

generator = FlashcardGenerator(api_key=api_key)
flashcards = generator.generate_flashcards(content)

# Get study schedule
schedule = generator.create_spaced_repetition_schedule(flashcards)

print("Day 1:", len(schedule['day_1']), "cards")
print("Day 7:", len(schedule['day_7']), "cards")
```

### Quiz Grading

```python
from src.generators import QuizGenerator

generator = QuizGenerator(api_key=api_key)
quiz = generator.generate_quiz(content)

# User answers
answers = {
    1: "A",
    2: "True",
    3: "The answer is..."
}

# Grade the quiz
results = generator.grade_quiz(quiz, answers)
print(f"Score: {results['score']}/{results['max_score']}")
print(f"Percentage: {results['percentage']}%")
```

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```
Solution: Install dependencies with: pip install -r requirements.txt
```

**2. OpenAI API Error**
```
Solution: Check that OPENAI_API_KEY is set correctly in .env
Verify your API key at https://platform.openai.com/api-keys
```

**3. FFmpeg not found (video processing)**
```
Solution: Install FFmpeg:
  - Ubuntu: sudo apt-get install ffmpeg
  - macOS: brew install ffmpeg
  - Windows: Download from ffmpeg.org
```

**4. PDF extraction fails**
```
Solution: Ensure PDF is not encrypted or password-protected
Try with a different PDF to verify system works
```

**5. Video download fails**
```
Solution: Check internet connection
Verify video URL is accessible
Some videos may have download restrictions
```

### Performance Tips

1. **Use GPT-3.5-turbo for faster processing:**
   ```env
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. **Process shorter content first** to test the system

3. **For large videos**, consider using `--no-video-audio` for metadata only

4. **Batch processing**: Process multiple files in sequence

### Getting Help

- Check the [README.md](README.md) for overview
- See [examples/](examples/) for sample usage
- Read [CONTRIBUTING.md](CONTRIBUTING.md) for development
- Open an issue on GitHub for bugs

## Best Practices

1. **Start small**: Test with a few pages before processing large documents
2. **Combine sources**: Use both PDF notes and video lectures for comprehensive materials
3. **Review modules first**: Understand the structure before using flashcards
4. **Take quizzes after studying**: Test your understanding of each module
5. **Use diagrams**: Visual learning aids comprehension
6. **Follow spaced repetition**: Use the generated schedule for flashcards

## Example Workflow

```bash
# 1. Process your materials
python main.py --pdf lecture_notes.pdf --video lecture_video.mp4 -o course_materials

# 2. Study the modules in order
cat course_materials/module_1.txt

# 3. Review the diagrams
open course_materials/diagram_*.png

# 4. Practice with flashcards
cat course_materials/flashcards.txt

# 5. Test your knowledge
cat course_materials/module_1_quiz.txt

# 6. Take the comprehensive quiz
cat course_materials/comprehensive_quiz.txt
```

## Additional Resources

- OpenAI API Documentation: https://platform.openai.com/docs
- Python Documentation: https://docs.python.org/3/
- FFmpeg Documentation: https://ffmpeg.org/documentation.html

---

For more information, visit the [GitHub repository](https://github.com/Zoe-life/study-material-automator).
