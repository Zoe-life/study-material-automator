// Progress Tracking Module

class ProgressTracker {
    constructor(authManager) {
        this.authManager = authManager;
    }
    
    async getProgress(topicId) {
        try {
            const response = await this.authManager.fetchWithAuth(`/api/progress/${topicId}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            return data;
        } catch (error) {
            console.error('Error fetching progress:', error);
            throw error;
        }
    }
    
    async markModuleComplete(topicId, moduleId) {
        try {
            const response = await this.authManager.fetchWithAuth(`/api/progress/${topicId}/module`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ module_id: moduleId })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            return data;
        } catch (error) {
            console.error('Error marking module complete:', error);
            throw error;
        }
    }
    
    async recordQuizScore(topicId, quizId, score) {
        try {
            const response = await this.authManager.fetchWithAuth(`/api/progress/${topicId}/quiz`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ quiz_id: quizId, score: score })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            return data;
        } catch (error) {
            console.error('Error recording quiz score:', error);
            throw error;
        }
    }
    
    async updateFlashcardProgress(topicId, count = 1) {
        try {
            const response = await this.authManager.fetchWithAuth(`/api/progress/${topicId}/flashcards`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ count: count })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            return data;
        } catch (error) {
            console.error('Error updating flashcard progress:', error);
            throw error;
        }
    }
    
    async createStudySession(topicId, sessionData) {
        try {
            const response = await this.authManager.fetchWithAuth(`/api/progress/${topicId}/session`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(sessionData)
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            return data;
        } catch (error) {
            console.error('Error creating study session:', error);
            throw error;
        }
    }
    
    renderProgressBar(percentage) {
        return `
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: ${percentage}%"></div>
                <span class="progress-text">${Math.round(percentage)}%</span>
            </div>
        `;
    }
    
    renderProgressCard(progress) {
        return `
            <div class="progress-card">
                <h3>Your Progress</h3>
                <div class="progress-stats">
                    <div class="stat">
                        <span class="stat-label">Completion</span>
                        <span class="stat-value">${Math.round(progress.completion_percentage)}%</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Modules Completed</span>
                        <span class="stat-value">${progress.modules_completed.length}</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Study Time</span>
                        <span class="stat-value">${progress.total_study_time} min</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Average Score</span>
                        <span class="stat-value">${Math.round(progress.average_score)}%</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Flashcards Reviewed</span>
                        <span class="stat-value">${progress.flashcards_reviewed}</span>
                    </div>
                </div>
                ${this.renderProgressBar(progress.completion_percentage)}
            </div>
        `;
    }
}

// Initialize global progress tracker
// Check if authManager is available
if (typeof authManager !== 'undefined') {
    const progressTracker = new ProgressTracker(authManager);
} else {
    console.warn('AuthManager not loaded. Progress tracker initialization delayed.');
}
