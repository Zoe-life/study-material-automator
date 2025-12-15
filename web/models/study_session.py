"""Study session tracking model"""
from datetime import datetime
from .user import db


class StudySession(db.Model):
    """Individual study session tracking"""
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    
    # Session details
    session_type = db.Column(db.String(50), nullable=False)  # 'module', 'quiz', 'flashcard'
    content_id = db.Column(db.String(100), nullable=True)  # module_1, quiz_2, etc.
    
    # Time tracking
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, default=0)
    
    # Performance (for quizzes)
    score = db.Column(db.Float, nullable=True)
    items_completed = db.Column(db.Integer, default=0)  # questions answered, cards reviewed, etc.
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'session_type': self.session_type,
            'content_id': self.content_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'score': score if self.score else None,
            'items_completed': self.items_completed,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<StudySession {self.session_type} topic_id={self.topic_id}>'
