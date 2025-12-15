"""Progress tracking model"""
from datetime import datetime
from .user import db


class Progress(db.Model):
    """User progress tracking for each topic"""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    
    # Progress metrics
    modules_completed = db.Column(db.JSON, default=list)  # List of completed module IDs/names
    quizzes_taken = db.Column(db.JSON, default=list)  # List of quiz attempts
    flashcards_reviewed = db.Column(db.Integer, default=0)
    
    # Overall progress percentage (0-100)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Study time tracking (in minutes)
    total_study_time = db.Column(db.Integer, default=0)
    
    # Performance metrics
    quiz_scores = db.Column(db.JSON, default=list)  # List of scores
    average_score = db.Column(db.Float, default=0.0)
    
    # Timestamps
    last_studied = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_completion(self):
        """Calculate overall completion percentage"""
        # Simple calculation based on modules completed
        if not self.topic or self.topic.num_modules == 0:
            self.completion_percentage = 0.0
        else:
            modules_done = len(self.modules_completed) if self.modules_completed else 0
            self.completion_percentage = (modules_done / self.topic.num_modules) * 100
    
    def calculate_average_score(self):
        """Calculate average quiz score"""
        if not self.quiz_scores or len(self.quiz_scores) == 0:
            self.average_score = 0.0
        else:
            self.average_score = sum(self.quiz_scores) / len(self.quiz_scores)
    
    def to_dict(self):
        """Convert progress to dictionary"""
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'modules_completed': self.modules_completed or [],
            'quizzes_taken': self.quizzes_taken or [],
            'flashcards_reviewed': self.flashcards_reviewed,
            'completion_percentage': round(self.completion_percentage, 2),
            'total_study_time': self.total_study_time,
            'quiz_scores': self.quiz_scores or [],
            'average_score': round(self.average_score, 2),
            'last_studied': self.last_studied.isoformat() if self.last_studied else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Progress user_id={self.user_id} topic_id={self.topic_id}>'
