# Study Material Automator - Web Interface

An intuitive web UI for the Study Material Automator that allows users to easily upload PDFs and video URLs to generate comprehensive study materials.

## Features

- **Drag & Drop File Upload**: Easy PDF upload with drag-and-drop support
- **Video URL Processing**: Support for YouTube and other video platforms
- **Real-time Progress**: Visual feedback during processing
- **Interactive Results Display**: 
  - Summary cards showing generated materials count
  - Main topics overview
  - Tabbed interface for different material types
  - File preview in modal
  - Direct download buttons
- **Modern UI/UX**: Responsive design with smooth animations and transitions

## Running the Web Interface

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration

Make sure your `.env` file is configured with your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Start the Web Server

```bash
cd web
python app.py
```

The application will start on `http://localhost:5000`

### 4. Access the Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Upload Content**:
   - Drag and drop a PDF file, or click to browse
   - Optionally, add a video URL (YouTube, etc.)
   - Click "Generate Study Materials"

2. **View Results**:
   - See summary statistics of generated materials
   - Browse main topics covered
   - Switch between tabs to view:
     - Learning Modules
     - Concept Diagrams
     - Study Flashcards
     - Practice Quizzes

3. **Interact with Materials**:
   - Click "View" to preview content in a modal
   - Click "Download" to save files locally
   - Click "New Upload" to process more materials

## Architecture

```
web/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Main UI template
├── static/
│   ├── css/
│   │   └── style.css   # Modern styling
│   └── js/
│       └── script.js   # Frontend interactions
└── README.md           # This file
```

## UI Components

### Upload Section
- File input with drag & drop
- URL input for videos
- Visual feedback for selected files
- Submit button with progress indicator

### Results Section
- Summary cards (modules, diagrams, flashcards, quizzes)
- Topics overview with tags
- Tabbed navigation
- File lists with actions (view, download)
- Modal viewer for content

## Design Features

- **Gradient Headers**: Eye-catching gradient backgrounds
- **Card-based Layout**: Clean, organized content display
- **Hover Effects**: Interactive feedback on all clickable elements
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Icons**: Font Awesome icons throughout
- **Smooth Animations**: Transitions and loading indicators

## API Endpoints

- `GET /` - Main page
- `POST /upload` - Process uploaded content
- `GET /view/<session_id>/<category>/<filename>` - View file content
- `GET /download/<session_id>/<filename>` - Download file
- `GET /health` - Health check

## Configuration

The web app uses the same configuration as the CLI:
- OpenAI API key from `.env` file
- Model settings (GPT-4 by default)
- Output directory management

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Development

To modify the UI:
1. Edit HTML in `templates/index.html`
2. Update styles in `static/css/style.css`
3. Modify interactions in `static/js/script.js`
4. Backend logic in `app.py`

The Flask app runs in debug mode by default, so changes are reflected immediately.

## Security Notes

- File uploads are limited to 50MB
- Only PDF files are accepted
- Session-based file isolation
- Files are stored in temporary directories

## Troubleshooting

**App won't start:**
- Check that Flask is installed: `pip install Flask`
- Verify your `.env` file has `OPENAI_API_KEY`

**Upload fails:**
- Ensure PDF is not encrypted
- Check file size (max 50MB)
- Verify API key is valid

**Content not displaying:**
- Check browser console for errors
- Ensure backend is running
- Try refreshing the page

## Future Enhancements

- Real-time progress updates via WebSockets
- User authentication and saved sessions
- Share links for generated materials
- Export to different formats
- Collaborative features
- Mobile app integration
