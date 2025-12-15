"""Flask Web Application for Study Material Automator"""
import os
import json
import tempfile
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import secrets

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.study_material_automator import StudyMaterialAutomator
from src.utils import Config

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and processing"""
    try:
        # Get form data
        pdf_file = request.files.get('pdf_file')
        video_url = request.form.get('video_url', '').strip()
        
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
        
        # Validate PDF file
        pdf_path = None
        if pdf_file and pdf_file.filename:
            if not allowed_file(pdf_file.filename):
                return jsonify({'error': 'Only PDF files are allowed'}), 400
            
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pdf_file.save(pdf_path)
        
        # Create output directory for this session
        session_id = secrets.token_hex(8)
        session['session_id'] = session_id
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{session_id}')
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize and run automator
        config = Config()
        if not config.validate():
            return jsonify({'error': 'Server configuration error. Please contact administrator.'}), 500
        
        automator = StudyMaterialAutomator(config)
        
        # Process materials
        results = automator.process_materials(
            pdf_path=pdf_path,
            video_source=video_url if video_url else None,
            output_dir=output_dir
        )
        
        # Load summary
        summary_path = os.path.join(output_dir, 'summary.json')
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        # Prepare response with file paths
        response_data = {
            'session_id': session_id,
            'summary': summary,
            'files': {
                'modules': results['modules'],
                'diagrams': results['diagrams'],
                'flashcards': results['flashcards'],
                'quizzes': results['quizzes']
            }
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/view/<session_id>/<category>/<filename>')
def view_file(session_id, category, filename):
    """View generated file"""
    try:
        # Validate filename to prevent path traversal
        filename = secure_filename(filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{session_id}')
        file_path = os.path.join(output_dir, filename)
        
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

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Download generated file"""
    try:
        # Validate filename to prevent path traversal
        filename = secure_filename(filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'output_{session_id}')
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
