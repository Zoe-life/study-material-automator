"""Flask Web Application for Study Material Automator - Enhanced with Auth & Progress Tracking"""
import os
import json
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import secrets

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.study_material_automator import StudyMaterialAutomator
from src.utils import Config

# Import auth and models
from models.user import db, bcrypt, User
from models.topic import Topic
from models.progress import Progress
from models.study_session import StudySession
from auth import init_jwt, jwt_required, get_current_user, generate_tokens
from auth import init_oauth, google_bp, microsoft_bp, apple_bp

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', tempfile.mkdtemp())

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///study_automator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# OAuth configuration
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID', '')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET', '')
app.config['MICROSOFT_CLIENT_ID'] = os.getenv('MICROSOFT_CLIENT_ID', '')
app.config['MICROSOFT_CLIENT_SECRET'] = os.getenv('MICROSOFT_CLIENT_SECRET', '')
app.config['APPLE_CLIENT_ID'] = os.getenv('APPLE_CLIENT_ID', '')
app.config['APPLE_CLIENT_SECRET'] = os.getenv('APPLE_CLIENT_SECRET', '')

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
init_jwt(app)
init_oauth(app)

# Register OAuth blueprints
app.register_blueprint(google_bp, url_prefix='/auth/google')
app.register_blueprint(microsoft_bp, url_prefix='/auth/microsoft')
app.register_blueprint(apple_bp, url_prefix='/auth/apple')

# Create tables
with app.app_context():
    db.create_all()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user with email/password"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        if not email or not password or not name:
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        tokens = generate_tokens(user.id)
        
        return jsonify({
            'user': user.to_dict(),
            **tokens
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with email/password"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate tokens
        tokens = generate_tokens(user.id)
        
        return jsonify({
            'user': user.to_dict(),
            **tokens
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/oauth-complete', methods=['POST'])
def oauth_complete():
    """Complete OAuth authentication"""
    try:
        oauth_user = session.get('oauth_user')
        if not oauth_user:
            return jsonify({'error': 'No OAuth session found'}), 400
        
        # Find or create user
        user = User.query.filter_by(
            oauth_provider=oauth_user['provider'],
            oauth_id=oauth_user['id']
        ).first()
        
        if not user:
            # Create new user from OAuth
            user = User(
                email=oauth_user['email'],
                name=oauth_user['name'],
                oauth_provider=oauth_user['provider'],
                oauth_id=oauth_user['id'],
                is_verified=True
            )
            db.session.add(user)
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Clear OAuth session
        session.pop('oauth_user', None)
        
        # Generate tokens
        tokens = generate_tokens(user.id)
        
        return jsonify({
            'user': user.to_dict(),
            **tokens
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@jwt_required
def get_me():
    """Get current user info"""
    try:
        user_id = get_current_user()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Topic/Upload Routes
# ============================================================================

@app.route('/api/topics', methods=['GET'])
@jwt_required
def get_topics():
    """Get all topics for current user"""
    try:
        user_id = get_current_user()
        topics = Topic.query.filter_by(user_id=user_id).order_by(Topic.created_at.desc()).all()
        return jsonify([topic.to_dict() for topic in topics])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/topics', methods=['POST'])
@jwt_required
def create_topic():
    """Create new topic and process materials"""
    try:
        user_id = get_current_user()
        
        # Get form data
        topic_name = request.form.get('topic_name', '').strip()
        topic_description = request.form.get('topic_description', '').strip()
        pdf_file = request.files.get('pdf_file')
        video_url = request.form.get('video_url', '').strip()
        
        if not topic_name:
            return jsonify({'error': 'Topic name is required'}), 400
        
        if not pdf_file and not video_url:
            return jsonify({'error': 'Please provide either a PDF file or a video URL'}), 400
        
        # Validate video URL if provided
        if video_url:
            from urllib.parse import urlparse
            try:
                parsed = urlparse(video_url)
                if not parsed.scheme in ['http', 'https']:
                    return jsonify({'error': 'Invalid video URL. Only HTTP/HTTPS URLs are allowed.'}), 400
            except Exception:
                return jsonify({'error': 'Invalid video URL format'}), 400
        
        # Validate and save PDF file
        pdf_path = None
        pdf_filename = None
        if pdf_file and pdf_file.filename:
            if not allowed_file(pdf_file.filename):
                return jsonify({'error': 'Only PDF files are allowed'}), 400
            
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_{pdf_filename}")
            pdf_file.save(pdf_path)
        
        # Create output directory
        session_id = secrets.token_hex(8)
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'user_{user_id}_topic_{session_id}')
        os.makedirs(output_dir, exist_ok=True)
        
        # Process materials
        config = Config()
        if not config.validate():
            return jsonify({'error': 'Server configuration error. Please contact administrator.'}), 500
        
        automator = StudyMaterialAutomator(config)
        results = automator.process_materials(
            pdf_path=pdf_path,
            video_source=video_url if video_url else None,
            output_dir=output_dir
        )
        
        # Load summary
        summary_path = os.path.join(output_dir, 'summary.json')
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        # Create topic record
        topic = Topic(
            user_id=user_id,
            name=topic_name,
            description=topic_description,
            pdf_filename=pdf_filename,
            video_url=video_url,
            output_directory=output_dir,
            num_modules=len(results['modules']),
            num_diagrams=len(results['diagrams']),
            num_flashcards=len(results['flashcards']),
            num_quizzes=len(results['quizzes']),
            topics_covered=summary.get('analysis', {}).get('main_topics', [])
        )
        db.session.add(topic)
        
        # Create initial progress record
        progress = Progress(user_id=user_id, topic_id=topic.id)
        db.session.add(progress)
        
        db.session.commit()
        
        return jsonify({
            'topic': topic.to_dict(),
            'summary': summary,
            'files': {
                'modules': [os.path.basename(p) for p in results['modules']],
                'diagrams': [os.path.basename(p) for p in results['diagrams']],
                'flashcards': [os.path.basename(p) for p in results['flashcards']],
                'quizzes': [os.path.basename(p) for p in results['quizzes']]
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/topics/<int:topic_id>', methods=['GET'])
@jwt_required
def get_topic(topic_id):
    """Get specific topic"""
    try:
        user_id = get_current_user()
        topic = Topic.query.filter_by(id=topic_id, user_id=user_id).first()
        if not topic:
            return jsonify({'error': 'Topic not found'}), 404
        return jsonify(topic.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Progress Tracking Routes
# ============================================================================

@app.route('/api/progress/<int:topic_id>', methods=['GET'])
@jwt_required
def get_progress(topic_id):
    """Get progress for a topic"""
    try:
        user_id = get_current_user()
        progress = Progress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
        if not progress:
            return jsonify({'error': 'Progress not found'}), 404
        return jsonify(progress.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/<int:topic_id>/module', methods=['POST'])
@jwt_required
def mark_module_complete(topic_id):
    """Mark a module as completed"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        module_id = data.get('module_id')
        
        if not module_id:
            return jsonify({'error': 'Module ID is required'}), 400
        
        progress = Progress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
        if not progress:
            return jsonify({'error': 'Progress not found'}), 404
        
        # Add module to completed list
        if not progress.modules_completed:
            progress.modules_completed = []
        if module_id not in progress.modules_completed:
            progress.modules_completed.append(module_id)
            progress.modules_completed = progress.modules_completed  # Trigger update
        
        progress.last_studied = datetime.utcnow()
        progress.calculate_completion()
        db.session.commit()
        
        return jsonify(progress.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/<int:topic_id>/quiz', methods=['POST'])
@jwt_required
def record_quiz_score(topic_id):
    """Record a quiz score"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        quiz_id = data.get('quiz_id')
        score = data.get('score')
        
        if quiz_id is None or score is None:
            return jsonify({'error': 'Quiz ID and score are required'}), 400
        
        progress = Progress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
        if not progress:
            return jsonify({'error': 'Progress not found'}), 404
        
        # Add quiz attempt
        if not progress.quizzes_taken:
            progress.quizzes_taken = []
        progress.quizzes_taken.append({'quiz_id': quiz_id, 'score': score, 'timestamp': datetime.utcnow().isoformat()})
        progress.quizzes_taken = progress.quizzes_taken  # Trigger update
        
        # Add score
        if not progress.quiz_scores:
            progress.quiz_scores = []
        progress.quiz_scores.append(score)
        progress.quiz_scores = progress.quiz_scores  # Trigger update
        
        progress.last_studied = datetime.utcnow()
        progress.calculate_average_score()
        db.session.commit()
        
        return jsonify(progress.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/<int:topic_id>/flashcards', methods=['POST'])
@jwt_required
def update_flashcard_progress(topic_id):
    """Update flashcard review count"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        count = data.get('count', 1)
        
        progress = Progress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
        if not progress:
            return jsonify({'error': 'Progress not found'}), 404
        
        progress.flashcards_reviewed += count
        progress.last_studied = datetime.utcnow()
        db.session.commit()
        
        return jsonify(progress.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/<int:topic_id>/session', methods=['POST'])
@jwt_required
def create_study_session(topic_id):
    """Create a new study session"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        
        session_obj = StudySession(
            user_id=user_id,
            topic_id=topic_id,
            session_type=data.get('session_type', 'module'),
            content_id=data.get('content_id'),
            duration_minutes=data.get('duration_minutes', 0),
            score=data.get('score'),
            items_completed=data.get('items_completed', 0),
            notes=data.get('notes')
        )
        db.session.add(session_obj)
        
        # Update progress study time
        progress = Progress.query.filter_by(user_id=user_id, topic_id=topic_id).first()
        if progress:
            progress.total_study_time += data.get('duration_minutes', 0)
            progress.last_studied = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(session_obj.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard', methods=['GET'])
@jwt_required
def get_dashboard():
    """Get user dashboard data"""
    try:
        user_id = get_current_user()
        
        # Get all topics
        topics = Topic.query.filter_by(user_id=user_id).all()
        
        # Get overall progress
        total_topics = len(topics)
        progress_data = []
        total_study_time = 0
        total_completion = 0
        
        for topic in topics:
            progress = Progress.query.filter_by(user_id=user_id, topic_id=topic.id).first()
            if progress:
                progress_data.append({
                    'topic': topic.to_dict(),
                    'progress': progress.to_dict()
                })
                total_study_time += progress.total_study_time
                total_completion += progress.completion_percentage
        
        avg_completion = total_completion / total_topics if total_topics > 0 else 0
        
        return jsonify({
            'total_topics': total_topics,
            'total_study_time': total_study_time,
            'average_completion': round(avg_completion, 2),
            'topics': progress_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# File Access Routes (protected)
# ============================================================================

@app.route('/api/files/<int:topic_id>/<filename>')
@jwt_required
def view_file(topic_id, filename):
    """View generated file for a topic"""
    try:
        user_id = get_current_user()
        topic = Topic.query.filter_by(id=topic_id, user_id=user_id).first()
        if not topic:
            return jsonify({'error': 'Topic not found'}), 404
        
        # Validate filename
        filename = secure_filename(filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(topic.output_directory, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Read file content
        if filename.endswith('.png'):
            return send_file(file_path, mimetype='image/png')
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'content': content, 'filename': filename})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files/<int:topic_id>/<filename>/download')
@jwt_required
def download_topic_file(topic_id, filename):
    """Download generated file"""
    try:
        user_id = get_current_user()
        topic = Topic.query.filter_by(id=topic_id, user_id=user_id).first()
        if not topic:
            return jsonify({'error': 'Topic not found'}), 404
        
        filename = secure_filename(filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(topic.output_directory, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Public Routes
# ============================================================================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Debug mode should only be enabled in development
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
