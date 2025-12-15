# System Architecture

## Overview

The Study Material Automator is a full-stack web application with authentication, progress tracking, and AI-powered study material generation.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          FRONTEND (Browser)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   index.html │  │   auth.js    │  │  progress.js │             │
│  │              │  │              │  │              │             │
│  │  • Upload UI │  │  • Login     │  │  • Track     │             │
│  │  • Results   │  │  • Register  │  │  • Analytics │             │
│  │  • Dashboard │  │  • OAuth     │  │  • Sessions  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────────────────────────────────────────────┐          │
│  │              CSS Styles (style.css +                  │          │
│  │              auth-progress.css)                       │          │
│  └──────────────────────────────────────────────────────┘          │
│                                                                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                │ HTTPS / API Calls
                                │ (JWT Bearer Tokens)
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                      BACKEND (Flask Application)                      │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Flask Routes (app.py)                    │   │
│  │                                                               │   │
│  │  • /api/auth/*        - Authentication endpoints             │   │
│  │  • /api/topics/*      - Topic management                     │   │
│  │  • /api/progress/*    - Progress tracking                    │   │
│  │  • /api/dashboard     - User statistics                      │   │
│  │  • /api/files/*       - Protected file access                │   │
│  │                                                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │     Auth     │  │   Database   │  │   Content    │             │
│  │   Modules    │  │    Models    │  │  Processors  │             │
│  │              │  │              │  │              │             │
│  │  • jwt_auth  │  │  • User      │  │  • PDF       │             │
│  │  • oauth     │  │  • Topic     │  │  • Video     │             │
│  │  • Google    │  │  • Progress  │  │  • Analyzer  │             │
│  │  • Microsoft │  │  • Session   │  │  • Automator │             │
│  │  • Apple     │  │              │  │              │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                       │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                │
┌───────────────────────────────▼───────────────────────────────────────┐
│                        DATA LAYER                                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────────┐         ┌──────────────────┐                   │
│  │   SQLite/DB      │         │   File Storage   │                   │
│  │                  │         │                  │                   │
│  │  • users         │         │  • uploads/      │                   │
│  │  • topics        │         │  • user_X/       │                   │
│  │  • progress      │         │    - topic_Y/    │                   │
│  │  • study_sessions│         │      - modules   │                   │
│  │                  │         │      - diagrams  │                   │
│  └──────────────────┘         │      - quizzes   │                   │
│                                │      - flashcards│                   │
│                                └──────────────────┘                   │
│                                                                        │
└────────────────────────────────┬───────────────────────────────────────┘
                                 │
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                      EXTERNAL SERVICES                                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │   OpenAI     │  │   OAuth      │  │   Video      │                 │
│  │   API        │  │   Providers  │  │   Sources    │                 │
│  │              │  │              │  │              │                 │
│  │  • GPT-4     │  │  • Google    │  │  • YouTube   │                 │
│  │  • Whisper   │  │  • Microsoft │  │  • Direct    │                 │
│  │              │  │  • Apple     │  │    URLs      │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Request Flow Examples

### 1. User Registration

```
User → Frontend (auth.js) → POST /api/auth/register
                           ↓
                      Backend validates
                           ↓
                      Hash password (bcrypt)
                           ↓
                      Save to database (User model)
                           ↓
                      Generate JWT tokens
                           ↓
                      Return user + tokens → Frontend
                           ↓
                      Store in localStorage
                           ↓
                      Redirect to Dashboard
```

### 2. OAuth Login (Google)

```
User clicks "Sign in with Google"
     ↓
Frontend → /auth/google/login
     ↓
Redirect to Google OAuth
     ↓
User authorizes
     ↓
Google → /auth/google/callback
     ↓
Backend receives token
     ↓
Fetch user info from Google
     ↓
Find or create User in database
     ↓
Store OAuth data in session
     ↓
Redirect to frontend with success
     ↓
Frontend → POST /api/auth/oauth-complete
     ↓
Backend creates JWT tokens
     ↓
Return user + tokens
     ↓
Frontend stores and redirects to dashboard
```

### 3. Create New Topic

```
User uploads PDF + Video URL
     ↓
Frontend → POST /api/topics (with JWT)
     ↓
Backend verifies JWT
     ↓
Extract user_id from token
     ↓
Save uploaded files
     ↓
Call StudyMaterialAutomator:
  - Extract PDF text
  - Download/transcribe video
  - Analyze content with GPT-4
  - Generate modules
  - Create diagrams
  - Generate flashcards
  - Create quizzes
     ↓
Save to output directory
     ↓
Create Topic record in database
     ↓
Create Progress record (initial)
     ↓
Return topic + files info
     ↓
Frontend displays results
```

### 4. Track Progress (Mark Module Complete)

```
User clicks "Mark Complete" on Module 1
     ↓
Frontend → POST /api/progress/<topic_id>/module (with JWT)
     ↓
Backend verifies JWT
     ↓
Get Progress record (user_id + topic_id)
     ↓
Add module_id to modules_completed array
     ↓
Update last_studied timestamp
     ↓
Calculate new completion_percentage
     ↓
Save to database
     ↓
Return updated progress
     ↓
Frontend updates UI with new percentage
```

### 5. Dashboard View

```
User navigates to dashboard
     ↓
Frontend → GET /api/dashboard (with JWT)
     ↓
Backend verifies JWT
     ↓
Query all Topics for user
     ↓
For each topic, get Progress record
     ↓
Calculate aggregate statistics:
  - Total topics
  - Total study time
  - Average completion
     ↓
Return dashboard data
     ↓
Frontend displays:
  - Topic cards with progress bars
  - Overall statistics
  - Quick actions
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

### Topics Table
```sql
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    pdf_filename VARCHAR(255),
    video_url VARCHAR(500),
    output_directory VARCHAR(500) NOT NULL,
    num_modules INTEGER DEFAULT 0,
    num_diagrams INTEGER DEFAULT 0,
    num_flashcards INTEGER DEFAULT 0,
    num_quizzes INTEGER DEFAULT 0,
    topics_covered JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Progress Table
```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    modules_completed JSON DEFAULT '[]',
    quizzes_taken JSON DEFAULT '[]',
    flashcards_reviewed INTEGER DEFAULT 0,
    completion_percentage FLOAT DEFAULT 0.0,
    total_study_time INTEGER DEFAULT 0,
    quiz_scores JSON DEFAULT '[]',
    average_score FLOAT DEFAULT 0.0,
    last_studied DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);
```

### Study Sessions Table
```sql
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    session_type VARCHAR(50) NOT NULL,
    content_id VARCHAR(100),
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    duration_minutes INTEGER DEFAULT 0,
    score FLOAT,
    items_completed INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (topic_id) REFERENCES topics (id)
);
```

## Security Model

### Authentication Flow
1. **JWT Tokens**: Access token (1 hour) + Refresh token (30 days)
2. **Password**: Bcrypt hashing with salt
3. **OAuth**: Server-to-server token exchange

### Authorization
- All API endpoints check JWT in Authorization header
- User ID extracted from verified JWT
- Database queries filtered by user_id
- File access validated against topic ownership

### Data Isolation
```python
# Example: User can only access their own topics
topic = Topic.query.filter_by(
    id=topic_id,
    user_id=current_user_id  # from JWT
).first()
```

## File Organization

```
study-material-automator/
├── web/
│   ├── app.py                  # Main Flask application
│   ├── auth/                   # Authentication modules
│   │   ├── jwt_auth.py         # JWT management
│   │   └── oauth.py            # OAuth providers
│   ├── models/                 # Database models
│   │   ├── user.py             # User model
│   │   ├── topic.py            # Topic model
│   │   ├── progress.py         # Progress model
│   │   └── study_session.py    # Session model
│   ├── templates/              # HTML templates
│   │   └── index.html          # Main page
│   └── static/                 # Static assets
│       ├── css/
│       │   ├── style.css       # Main styles
│       │   └── auth-progress.css  # Auth/Progress styles
│       └── js/
│           ├── script.js       # Main JavaScript
│           ├── auth.js         # Auth manager
│           └── progress.js     # Progress tracker
├── src/                        # Core processing
│   ├── processors/             # Input processors
│   ├── generators/             # Output generators
│   └── utils/                  # Utilities
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
└── README.md                   # Documentation
```

## Technology Stack

### Backend
- **Framework**: Flask 3.0+
- **Database**: SQLAlchemy ORM (SQLite default, PostgreSQL ready)
- **Authentication**: 
  - Flask-JWT-Extended (JWT)
  - Authlib (OAuth 2.0)
  - Flask-Bcrypt (Password hashing)
- **CORS**: Flask-CORS

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: Vanilla JS (no framework dependencies)
- **Icons**: Font Awesome

### AI/ML
- **OpenAI GPT-4**: Content analysis and generation
- **OpenAI Whisper**: Audio transcription
- **Tiktoken**: Token counting

### Processing
- **PDF**: PyPDF2, pdfplumber
- **Video**: opencv-python, moviepy, yt-dlp
- **Diagrams**: matplotlib, Pillow

## Deployment Considerations

### Environment Variables
```env
# Required
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...  # or sqlite:///...
SECRET_KEY=...
JWT_SECRET_KEY=...

# Optional (OAuth)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
MICROSOFT_CLIENT_ID=...
MICROSOFT_CLIENT_SECRET=...
APPLE_CLIENT_ID=...
APPLE_CLIENT_SECRET=...

# Optional (Config)
FLASK_DEBUG=false
UPLOAD_FOLDER=/var/app/uploads
```

### Production Setup
1. Use PostgreSQL instead of SQLite
2. Set secure SECRET_KEY and JWT_SECRET_KEY
3. Configure OAuth with production redirect URIs
4. Use gunicorn or uwsgi for WSGI
5. Set up HTTPS with valid SSL certificate
6. Configure file storage (S3, etc.)
7. Set up database backups
8. Monitor with logging/APM

### Scaling Options
- **Horizontal**: Multiple app servers behind load balancer
- **Database**: Read replicas, connection pooling
- **Files**: Object storage (S3, GCS)
- **Cache**: Redis for sessions/API responses
- **Background Jobs**: Celery for material generation

## Performance Optimizations

1. **Database Indexes**: On user_id, topic_id, email
2. **File Caching**: Cache generated materials
3. **API Rate Limiting**: Prevent abuse
4. **Async Processing**: Generate materials in background
5. **CDN**: Serve static assets via CDN

---

This architecture provides a solid foundation for a production-ready study material automation system with modern authentication and comprehensive progress tracking!
