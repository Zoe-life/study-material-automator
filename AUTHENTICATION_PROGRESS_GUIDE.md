# Authentication & Progress Tracking Guide

## New Features Overview

This guide covers the authentication system and progress tracking features added to the Study Material Automator.

## Authentication System

### Features
- **Email/Password Authentication**: Traditional login and registration
- **JWT-Based Sessions**: Secure token-based authentication
- **OAuth 2.0 Integration**: 
  - Sign in with Google
  - Sign in with Microsoft
  - Sign in with Apple

### Setup

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Edit `.env` file:
```env
# Database
DATABASE_URL=sqlite:///study_automator.db

# Security
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# OAuth 2.0 Providers
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

MICROSOFT_CLIENT_ID=your-microsoft-client-id
MICROSOFT_CLIENT_SECRET=your-microsoft-client-secret

APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret
```

#### 3. Initialize Database
```bash
cd web
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### API Endpoints

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  },
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### OAuth Login
Navigate to:
- Google: `/auth/google/login`
- Microsoft: `/auth/microsoft/login`
- Apple: `/auth/apple/login`

## 📊 Progress Tracking

### Features
- Module completion tracking
- Quiz score recording
- Flashcard review counting
- Study time tracking
- Study session logging
- Performance analytics

### API Endpoints

#### Get Progress
```http
GET /api/progress/<topic_id>
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "topic_id": 1,
  "modules_completed": ["module_1", "module_2"],
  "quizzes_taken": [
    {
      "quiz_id": "quiz_1",
      "score": 85,
      "timestamp": "2025-12-15T10:00:00"
    }
  ],
  "flashcards_reviewed": 50,
  "completion_percentage": 66.67,
  "total_study_time": 120,
  "quiz_scores": [85, 90, 78],
  "average_score": 84.33,
  "last_studied": "2025-12-15T10:00:00"
}
```

#### Mark Module Complete
```http
POST /api/progress/<topic_id>/module
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "module_id": "module_1"
}
```

#### Record Quiz Score
```http
POST /api/progress/<topic_id>/quiz
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quiz_id": "quiz_1",
  "score": 85
}
```

#### Update Flashcard Progress
```http
POST /api/progress/<topic_id>/flashcards
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "count": 10
}
```

#### Create Study Session
```http
POST /api/progress/<topic_id>/session
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "session_type": "module",
  "content_id": "module_1",
  "duration_minutes": 30,
  "score": 90,
  "items_completed": 1,
  "notes": "Completed module 1"
}
```

## 📚 Multiple Topic Management

### Features
- Upload materials for different subjects/topics
- Organize study materials by topic
- Track progress separately for each topic
- View all topics in a dashboard

### API Endpoints

#### Get All Topics
```http
GET /api/topics
Authorization: Bearer <access_token>
```

#### Create New Topic
```http
POST /api/topics
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

topic_name: "Machine Learning Fundamentals"
topic_description: "Introduction to ML concepts"
pdf_file: <file>
video_url: "https://youtube.com/watch?v=..."
```

**Response:**
```json
{
  "topic": {
    "id": 1,
    "name": "Machine Learning Fundamentals",
    "description": "Introduction to ML concepts",
    "num_modules": 3,
    "num_diagrams": 2,
    "num_flashcards": 1,
    "num_quizzes": 4,
    "topics_covered": ["Neural Networks", "Deep Learning"],
    "created_at": "2025-12-15T10:00:00"
  },
  "summary": { ... },
  "files": { ... }
}
```

#### Get Specific Topic
```http
GET /api/topics/<topic_id>
Authorization: Bearer <access_token>
```

## 🎯 Dashboard

### Get Dashboard Data
```http
GET /api/dashboard
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "total_topics": 5,
  "total_study_time": 600,
  "average_completion": 45.5,
  "topics": [
    {
      "topic": { ... },
      "progress": { ... }
    }
  ]
}
```

## 🔒 Protected File Access

All generated files are now protected and require authentication:

```http
GET /api/files/<topic_id>/<filename>
Authorization: Bearer <access_token>
```

```http
GET /api/files/<topic_id>/<filename>/download
Authorization: Bearer <access_token>
```

## 🎨 Frontend Integration

### Using Auth Manager
```javascript
// Initialize
const authManager = new AuthManager();

// Register
await authManager.register(email, password, name);

// Login
await authManager.login(email, password);

// OAuth
authManager.loginWithGoogle();
authManager.loginWithMicrosoft();
authManager.loginWithApple();

// Complete OAuth (after redirect)
await authManager.completeOAuth();

// Logout
authManager.logout();

// Check if authenticated
if (authManager.isAuthenticated()) {
  // User is logged in
}

// Make authenticated requests
const response = await authManager.fetchWithAuth('/api/topics');
```

### Using Progress Tracker
```javascript
// Initialize
const progressTracker = new ProgressTracker(authManager);

// Get progress
const progress = await progressTracker.getProgress(topicId);

// Mark module complete
await progressTracker.markModuleComplete(topicId, 'module_1');

// Record quiz score
await progressTracker.recordQuizScore(topicId, 'quiz_1', 85);

// Update flashcard count
await progressTracker.updateFlashcardProgress(topicId, 10);

// Create study session
await progressTracker.createStudySession(topicId, {
  session_type: 'module',
  content_id: 'module_1',
  duration_minutes: 30,
  score: 90,
  items_completed: 1
});

// Render progress card
document.getElementById('progress-container').innerHTML = 
  progressTracker.renderProgressCard(progress);
```

## 🗄️ Database Schema

### Users Table
- id (PK)
- email (unique)
- password_hash
- name
- oauth_provider
- oauth_id
- is_active
- is_verified
- created_at
- last_login

### Topics Table
- id (PK)
- user_id (FK)
- name
- description
- pdf_filename
- video_url
- output_directory
- num_modules
- num_diagrams
- num_flashcards
- num_quizzes
- topics_covered (JSON)
- created_at
- updated_at

### Progress Table
- id (PK)
- user_id (FK)
- topic_id (FK)
- modules_completed (JSON)
- quizzes_taken (JSON)
- flashcards_reviewed
- completion_percentage
- total_study_time
- quiz_scores (JSON)
- average_score
- last_studied
- created_at
- updated_at

### Study Sessions Table
- id (PK)
- user_id (FK)
- topic_id (FK)
- session_type
- content_id
- start_time
- end_time
- duration_minutes
- score
- items_completed
- notes

## 🔧 Configuration for OAuth Providers

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:5000/auth/google/callback`
6. Copy Client ID and Secret to `.env`

### Microsoft OAuth
1. Go to [Azure Portal](https://portal.azure.com/)
2. Register a new application
3. Add platform: Web
4. Add redirect URI: `http://localhost:5000/auth/microsoft/callback`
5. Create client secret
6. Copy Application ID and Secret to `.env`

### Apple OAuth
1. Go to [Apple Developer](https://developer.apple.com/)
2. Create a new Service ID
3. Configure Sign in with Apple
4. Add return URL: `http://localhost:5000/auth/apple/callback`
5. Generate private key
6. Configure `.env` with credentials

## 🚀 Running the Enhanced App

```bash
# Start the server
cd web
python app.py

# The app will be available at http://localhost:5000
```

## 📱 Example User Flow

1. User visits the app
2. Clicks "Sign Up" or "Login"
3. Creates account with email/password or OAuth
4. Gets redirected to dashboard
5. Clicks "Add New Topic"
6. Uploads PDF and/or video URL
7. System generates study materials
8. User studies module → marks complete
9. Progress is tracked automatically
10. Takes quiz → score is recorded
11. Reviews flashcards → count increases
12. Can view progress anytime
13. Can upload materials for other topics
14. Dashboard shows all topics and overall progress

## 🛡️ Security Best Practices

- All passwords are hashed with bcrypt
- JWT tokens expire after 1 hour
- Refresh tokens valid for 30 days
- OAuth tokens are validated
- File access is user-scoped
- SQL injection protection with SQLAlchemy ORM
- XSS protection in frontend
- CORS configured appropriately

## 📊 Analytics & Insights

The system tracks:
- Time spent studying
- Module completion rate
- Quiz performance over time
- Flashcard review frequency
- Study patterns and habits
- Per-topic and overall progress

## 🔮 Future Enhancements

Potential additions:
- Email verification
- Password reset functionality
- Profile picture uploads
- Social features (study groups)
- Gamification (badges, streaks)
- Mobile app
- Study reminders
- Export progress reports
