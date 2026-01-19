# Quick Start Guide - Web Interface

## Get Started in 3 Steps

### Step 1: Install & Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 2: Start the Web Server

**Option A: Using the startup script (recommended)**
```bash
./start_web.sh
```

**Option B: Manual start**
```bash
cd web
python app.py
```

### Step 3: Use the Web Interface

1. Open your browser to: **http://localhost:5000**

2. **Upload your materials:**
   - Drag & drop a PDF file, or click to browse
   - Optionally add a video URL (YouTube, etc.)
   - Click "Generate Study Materials"

3. **View your results:**
   - Summary shows count of generated materials
   - Browse main topics covered
   - Click tabs to view different material types
   - Click "View" to preview content
   - Click "Download" to save files

## Web Interface Features

### Upload Section
- **Drag & Drop**: Easy file upload
- **Video URLs**: YouTube and other platforms
- **Progress Bar**: Real-time processing status

### Results Display
- **Summary Cards**: Quick overview of materials
- **Topics Tags**: Main concepts covered
- **Tabbed Interface**: Organized by type
  - Learning Modules
  - Concept Diagrams
  - Study Flashcards
  - Practice Quizzes

### File Actions
- **Preview**: View content in modal
- **Download**: Save files locally
- **New Upload**: Process more materials

## Example Workflow

1. **Upload**: Drop your `lecture_notes.pdf` and add `https://youtube.com/watch?v=xyz`
2. **Process**: Wait 1-3 minutes while AI generates materials
3. **Study**: View modules → Review diagrams → Practice with flashcards → Take quizzes
4. **Download**: Save materials for offline study

## UI Screenshots

### Upload Interface
- Clean, modern design
- Clear instructions
- Visual feedback

### Results Display
- Interactive cards
- Filterable content
- Easy navigation

## Troubleshooting

**Server won't start?**
```bash
# Check Flask is installed
pip install Flask

# Verify .env has OPENAI_API_KEY
cat .env | grep OPENAI_API_KEY
```

**Upload fails?**
- Ensure PDF is not password-protected
- Check file size (max 50MB)
- Verify API key is valid

**Can't see results?**
- Check browser console (F12)
- Refresh the page
- Try a different browser

## Next Steps

- See `web/README.md` for detailed documentation
- Check `USAGE_GUIDE.md` for advanced features
- Visit `examples/` for sample content

## Tips

**Best Results:**
- Use clear, well-formatted PDFs
- Combine notes with video lectures
- Start with shorter content (5-10 pages)

**Performance:**
- Processing time depends on content length
- First upload may take longer
- Results are cached per session

**Studying:**
1. Read modules first
2. Review diagrams for visual understanding
3. Practice with flashcards
4. Test knowledge with quizzes

---

**Need help?** Check the main README.md or open an issue on GitHub.
