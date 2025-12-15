// Study Material Automator - Frontend JavaScript

let currentSessionId = null;
let currentResults = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeFileInput();
    initializeForm();
    initializeTabs();
});

// File input handling
function initializeFileInput() {
    const fileInput = document.getElementById('pdfFile');
    const fileDisplay = document.getElementById('fileDisplay');
    
    fileInput.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            fileDisplay.innerHTML = `
                <i class="fas fa-file-pdf"></i>
                <span>${file.name} (${formatFileSize(file.size)})</span>
            `;
            fileDisplay.classList.add('has-file');
        }
    });
    
    // Drag and drop
    const wrapper = document.querySelector('.file-input-wrapper');
    
    wrapper.addEventListener('dragover', function(e) {
        e.preventDefault();
        fileDisplay.style.borderColor = 'var(--primary-color)';
    });
    
    wrapper.addEventListener('dragleave', function(e) {
        e.preventDefault();
        fileDisplay.style.borderColor = 'var(--border-color)';
    });
    
    wrapper.addEventListener('drop', function(e) {
        e.preventDefault();
        fileDisplay.style.borderColor = 'var(--border-color)';
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            fileInput.files = e.dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });
}

// Form submission
function initializeForm() {
    const form = document.getElementById('uploadForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const pdfFile = document.getElementById('pdfFile').files[0];
        const videoUrl = document.getElementById('videoUrl').value.trim();
        
        if (!pdfFile && !videoUrl) {
            showError('Please provide either a PDF file or a video URL');
            return;
        }
        
        // Show progress
        showProgress();
        
        // Prepare form data
        const formData = new FormData();
        if (pdfFile) {
            formData.append('pdf_file', pdfFile);
        }
        if (videoUrl) {
            formData.append('video_url', videoUrl);
        }
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }
            
            // Store results
            currentSessionId = data.session_id;
            currentResults = data;
            
            // Display results
            displayResults(data);
            
        } catch (error) {
            hideProgress();
            showError(error.message);
        }
    });
}

// Show progress indicator
function showProgress() {
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('progressContainer').style.display = 'block';
}

// Hide progress indicator
function hideProgress() {
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('progressContainer').style.display = 'none';
}

// Display results
function displayResults(data) {
    hideProgress();
    
    // Hide upload section, show results
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Update summary cards
    document.getElementById('moduleCount').textContent = data.files.modules.length;
    document.getElementById('diagramCount').textContent = data.files.diagrams.length;
    document.getElementById('flashcardCount').textContent = data.files.flashcards.length;
    document.getElementById('quizCount').textContent = data.files.quizzes.length;
    
    // Display topics
    if (data.summary.analysis && data.summary.analysis.main_topics) {
        const topicsList = document.getElementById('topicsList');
        topicsList.innerHTML = data.summary.analysis.main_topics
            .map(topic => `<span class="topic-tag">${escapeHtml(topic)}</span>`)
            .join('');
    }
    
    // Populate file lists
    populateModules(data.files.modules);
    populateDiagrams(data.files.diagrams);
    populateFlashcards(data.files.flashcards);
    populateQuizzes(data.files.quizzes);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Populate modules list
function populateModules(modules) {
    const list = document.getElementById('modulesList');
    list.innerHTML = modules.map((path, index) => {
        const filename = escapeHtml(path.split('/').pop());
        return `
            <div class="file-item">
                <div class="file-info">
                    <i class="fas fa-book file-icon"></i>
                    <div class="file-details">
                        <h4>${filename}</h4>
                        <p>Learning Module ${index + 1}</p>
                    </div>
                </div>
                <div class="file-actions">
                    <button class="action-btn view-btn" onclick="viewFile('modules', '${filename}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="action-btn download-btn" onclick="downloadFile('${filename}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Populate diagrams grid
function populateDiagrams(diagrams) {
    const grid = document.getElementById('diagramsList');
    grid.innerHTML = diagrams.map(path => {
        const filename = escapeHtml(path.split('/').pop());
        const name = escapeHtml(filename.replace('.png', '').replace('diagram_', '').replace(/_/g, ' '));
        return `
            <div class="diagram-item">
                <img src="/view/${currentSessionId}/diagrams/${filename}" 
                     alt="${name}" 
                     class="diagram-preview"
                     onclick="viewImage('${filename}', '${name}')">
                <div class="diagram-info">
                    <h4>${name}</h4>
                    <button class="action-btn download-btn" onclick="downloadFile('${filename}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Populate flashcards list
function populateFlashcards(flashcards) {
    const list = document.getElementById('flashcardsList');
    list.innerHTML = flashcards.map(path => {
        const filename = escapeHtml(path.split('/').pop());
        return `
            <div class="file-item">
                <div class="file-info">
                    <i class="fas fa-layer-group file-icon"></i>
                    <div class="file-details">
                        <h4>${filename}</h4>
                        <p>Study Flashcards</p>
                    </div>
                </div>
                <div class="file-actions">
                    <button class="action-btn view-btn" onclick="viewFile('flashcards', '${filename}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="action-btn download-btn" onclick="downloadFile('${filename}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Populate quizzes list
function populateQuizzes(quizzes) {
    const list = document.getElementById('quizzesList');
    list.innerHTML = quizzes.map((path, index) => {
        const filename = escapeHtml(path.split('/').pop());
        const isComprehensive = filename.includes('comprehensive');
        return `
            <div class="file-item">
                <div class="file-info">
                    <i class="fas fa-clipboard-check file-icon"></i>
                    <div class="file-details">
                        <h4>${filename}</h4>
                        <p>${isComprehensive ? 'Comprehensive Assessment' : `Module ${index + 1} Quiz`}</p>
                    </div>
                </div>
                <div class="file-actions">
                    <button class="action-btn view-btn" onclick="viewFile('quizzes', '${filename}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="action-btn download-btn" onclick="downloadFile('${filename}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// View file in modal
async function viewFile(category, filename) {
    try {
        const response = await fetch(`/view/${currentSessionId}/${category}/${filename}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load file');
        }
        
        document.getElementById('modalTitle').textContent = filename;
        document.getElementById('modalBody').innerHTML = `<pre>${escapeHtml(data.content)}</pre>`;
        document.getElementById('fileModal').classList.add('active');
        
    } catch (error) {
        showError(error.message);
    }
}

// View image in modal
function viewImage(filename, title) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = 
        `<img src="/view/${currentSessionId}/diagrams/${escapeHtml(filename)}" alt="${escapeHtml(title)}">`;
    document.getElementById('fileModal').classList.add('active');
}

// Download file
function downloadFile(filename) {
    window.location.href = `/download/${currentSessionId}/${filename}`;
}

// Close modal
function closeModal() {
    document.getElementById('fileModal').classList.remove('active');
}

// Reset form for new upload
function resetForm() {
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('uploadForm').reset();
    document.getElementById('fileDisplay').innerHTML = `
        <i class="fas fa-cloud-upload-alt"></i>
        <span>Choose a PDF file or drag & drop here</span>
    `;
    document.getElementById('fileDisplay').classList.remove('has-file');
    currentSessionId = null;
    currentResults = null;
}

// Initialize tabs
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and panes
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding pane
            this.classList.add('active');
            document.getElementById(`${tabName}-pane`).classList.add('active');
        });
    });
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showError(message) {
    // Create a better error notification
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    errorDiv.innerHTML = `<strong>Error:</strong> ${escapeHtml(message)}`;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('fileModal');
    if (event.target === modal) {
        closeModal();
    }
}
