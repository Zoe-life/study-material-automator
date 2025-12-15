# Examples

This directory contains examples of how to use the Study Material Automator.

## Example Usage

### 1. Process a sample PDF

```bash
# If you have a PDF file
python main.py --pdf examples/sample_notes.pdf --output examples/output
```

### 2. Process a YouTube video

```bash
# Using a public educational video
python main.py --video "https://www.youtube.com/watch?v=EXAMPLE" --output examples/output
```

### 3. Combine multiple sources

```bash
# Process both PDF and video together for comprehensive materials
python main.py --pdf examples/notes.pdf --video examples/lecture.mp4 --output examples/output
```

## Expected Output

After running the automator, you'll find:

1. **Learning Modules** - Structured content broken into digestible sections
2. **Flashcards** - Question/answer pairs for memorization
3. **Quizzes** - Assessment questions with answers
4. **Diagrams** - Visual concept maps and illustrations
5. **Summary** - JSON file with overview of all generated materials

## Sample Content

To test the system, you can:

1. Use any PDF textbook or class notes
2. Use lecture recordings or educational videos
3. Try YouTube educational content (with a valid URL)

## Tips

- Start with shorter content (5-10 pages) to test the system
- Combine PDF notes with video lectures for best results
- Review the generated modules before studying with flashcards
- Take quizzes after studying each module
