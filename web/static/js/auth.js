// Authentication Module

class AuthManager {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
    }
    
    isAuthenticated() {
        return !!this.token;
    }
    
    async register(email, password, name) {
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, name })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            
            this.setAuth(data);
            return data;
        } catch (error) {
            throw error;
        }
    }
    
    async login(email, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            
            this.setAuth(data);
            return data;
        } catch (error) {
            throw error;
        }
    }
    
    loginWithGoogle() {
        window.location.href = '/auth/google/login';
    }
    
    loginWithMicrosoft() {
        window.location.href = '/auth/microsoft/login';
    }
    
    loginWithApple() {
        window.location.href = '/auth/apple/login';
    }
    
    async completeOAuth() {
        try {
            const response = await fetch('/api/auth/oauth-complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);
            
            this.setAuth(data);
            return data;
        } catch (error) {
            throw error;
        }
    }
    
    setAuth(data) {
        this.token = data.access_token;
        this.user = data.user;
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        localStorage.setItem('user', JSON.stringify(data.user));
    }
    
    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/';
    }
    
    getAuthHeader() {
        return {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
        };
    }
    
    async fetchWithAuth(url, options = {}) {
        if (!options.headers) {
            options.headers = {};
        }
        options.headers['Authorization'] = `Bearer ${this.token}`;
        
        const response = await fetch(url, options);
        
        // Handle 401 unauthorized
        if (response.status === 401) {
            this.logout();
            throw new Error('Session expired. Please login again.');
        }
        
        return response;
    }
}

// Initialize global auth manager
const authManager = new AuthManager();
