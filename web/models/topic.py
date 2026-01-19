"""Topic model for study materials"""
from datetime import datetime
from .user import db


class Topic(db.Model):
    """Topic/Subject model - each upload creates a topic"""
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Topic details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Source materials
    pdf_filename = db.Column(db.String(255), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    
    # Generated content paths
    output_directory = db.Column(db.String(500), nullable=False)
    
    # Summary data
    num_modules = db.Column(db.Integer, default=0)
    num_diagrams = db.Column(db.Integer, default=0)
    num_flashcards = db.Column(db.Integer, default=0)
    num_quizzes = db.Column(db.Integer, default=0)
    
    # Topics covered (stored as JSON)
    topics_covered = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('Progress', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    study_sessions = db.relationship('StudySession', backref='topic', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert topic to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'pdf_filename': self.pdf_filename,
            'video_url': self.video_url,
            'num_modules': self.num_modules,
            'num_diagrams': self.num_diagrams,
            'num_flashcards': self.num_flashcards,
            'num_quizzes': self.num_quizzes,
            'topics_covered': self.topics_covered,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Topic {self.name}>'
