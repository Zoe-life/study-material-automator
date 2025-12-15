# Study Material Automator

A fully automated system that processes PDF class notes and lecture videos into structured study materials, complete with diagrams, flashcards, quizzes, and simplified explanations.

## Features

🎯 **Comprehensive Content Processing**
- Extract and analyze text from PDF class notes
- Process and transcribe lecture videos (local files or URLs)
- Intelligent content analysis using AI

📚 **Structured Learning Modules**
- Automatically organize content into digestible modules
- Break down complex concepts into simple explanations
- Create learning objectives for each module
- Estimate study time requirements

🎨 **Visual Learning Materials**
- Generate concept map diagrams
- Create flow diagrams for processes
- Build hierarchical relationship diagrams
- Export high-quality PNG images

🃏 **Interactive Study Tools**
- Generate flashcards with spaced repetition schedules
- Create comprehensive quizzes for each module
- Multiple question types (multiple choice, true/false, short answer)
- Automatic quiz grading functionality

🤖 **AI-Powered Intelligence**
- Uses GPT-4 for content analysis and generation
- Simplifies complex concepts with analogies
- Identifies relationships between concepts
- Creates context-aware study materials

🌐 **Intuitive Web Interface**
- Modern, responsive UI for easy access
- Drag & drop file upload
- Real-time progress tracking
- Interactive preview of generated materials
- Download materials with one click

🔐 **User Authentication & Accounts**
- Email/password registration and login
- OAuth 2.0 (Google, Microsoft, Apple Sign-In)
- JWT-based secure sessions
- Personal user accounts with data privacy

📊 **Progress Tracking & Analytics**
- Module completion tracking
- Quiz score recording with performance analytics
- Flashcard review counting
- Study time tracking
- Overall completion percentage
- Personalized study dashboard

📚 **Multiple Topic Management**
- Upload materials for different subjects
- Organize study content by topic
- Track progress separately for each topic
- Dashboard view of all your topics
- Topic-specific file management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Zoe-life/study-material-automator.git
cd study-material-automator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
```bash
cp .env.example .env
# Edit .env and add your configuration:
# - OPENAI_API_KEY (required)
# - DATABASE_URL (defaults to SQLite)
# - OAuth credentials (optional, for social login)
```

4. Initialize the database (for web interface with auth):
```bash
cd web
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## Usage

### Web Interface (Recommended)

The easiest way to use the Study Material Automator is through the web interface:

```bash
cd web
python app.py
```

Then open your browser to `http://localhost:5000`

**Features:**
- 📤 Drag & drop PDF upload
- 🎥 Video URL input
- 📊 Interactive results display
- 👁️ Preview materials in-browser
- ⬇️ Download individual files

### Command Line Interface

Process a PDF file:
```bash
python main.py --pdf path/to/notes.pdf
```

Process a video URL:
```bash
python main.py --video https://youtube.com/watch?v=example
```

Process both PDF and video together:
```bash
python main.py --pdf notes.pdf --video lecture.mp4
```

### Advanced Options

Specify custom output directory:
```bash
python main.py --pdf notes.pdf --output my_study_materials
```

Use a custom configuration file:
```bash
python main.py --pdf notes.pdf --config custom.env
```

### Python API

You can also use the library programmatically:

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

# Access generated materials
print(f"Modules: {results['modules']}")
print(f"Flashcards: {results['flashcards']}")
print(f"Quizzes: {results['quizzes']}")
```

## Output Structure

The system generates the following materials in the output directory:

```
output/
├── module_1.txt              # Learning module 1
├── module_1_quiz.txt         # Quiz for module 1
├── module_2.txt              # Learning module 2
├── module_2_quiz.txt         # Quiz for module 2
├── diagram_Topic1.png        # Concept diagram
├── diagram_Topic2.png        # Concept diagram
├── flashcards.txt            # Study flashcards
├── comprehensive_quiz.txt    # Overall assessment
└── summary.json              # Summary of all materials
```

## Configuration

Create a `.env` file with the following variables:

```env
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
OPENAI_MODEL=gpt-4                 # AI model to use
OPENAI_TEMPERATURE=0.7             # Creativity level (0-1)
OUTPUT_DIR=output                  # Output directory
TEMP_DIR=temp                      # Temporary files directory
```

## Requirements

- Python 3.8+
- OpenAI API key
- FFmpeg (for video processing)

## Architecture

The system is organized into modular components:

- **Processors**: Extract content from PDFs and videos
- **Analyzers**: Use AI to analyze and structure content
- **Generators**: Create study materials (modules, diagrams, flashcards, quizzes)
- **CLI**: Command-line interface for easy usage

## Examples

See the `examples/` directory for sample inputs and outputs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with OpenAI's GPT-4 for intelligent content analysis
- Uses Whisper API for video transcription
- Matplotlib for diagram generation
