document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeCharts();
    initializeDropzone();
    initializeActivityList();
    initializeQueueList();
});

// Navigation handling
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const view = item.dataset.view;
            switchView(view);
            updateActiveNavItem(item);
        });
    });
}

function switchView(viewId) {
    const views = document.querySelectorAll('.view');
    views.forEach(view => view.classList.remove('active'));
    document.getElementById(`${viewId}-view`).classList.add('active', 'fade-in');
}

function updateActiveNavItem(activeItem) {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    activeItem.classList.add('active');
}

// Charts initialization
function initializeCharts() {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Processing Speed (ms)',
                data: [1200, 1100, 1000, 950, 900, 850],
                borderColor: '#4A90E2',
                tension: 0.4
            }, {
                label: 'Accuracy (%)',
                data: [95, 96, 97, 97, 98, 98],
                borderColor: '#2ECC71',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// File upload handling
function initializeDropzone() {
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = dropzone.querySelector('.file-input');

    dropzone.addEventListener('click', () => fileInput.click());
    
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            addToProcessingQueue(file);
        }
    });
}

// Queue management
function addToProcessingQueue(file) {
    const queueList = document.querySelector('.queue-list');
    const queueItem = document.createElement('div');
    queueItem.classList.add('queue-item');
    queueItem.innerHTML = `
        <div class="file-info">
            <span class="file-name">${file.name}</span>
            <span class="file-size">${formatFileSize(file.size)}</span>
        </div>
        <div class="progress-bar">
            <div class="progress" style="width: 0%"></div>
        </div>
    `;
    queueList.appendChild(queueItem);
    
    // Simulate processing
    simulateProcessing(queueItem);
}

function simulateProcessing(queueItem) {
    const progress = queueItem.querySelector('.progress');
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
            queueItem.classList.add('completed');
            addToActivityList(queueItem.querySelector('.file-name').textContent);
        } else {
            width++;
            progress.style.width = width + '%';
        }
    }, 50);
}

// Activity list management
function initializeActivityList() {
    const activityList = document.querySelector('.activity-list');
    // Add some sample activities
    const activities = [
        'Image batch processing completed',
        'New model version deployed',
        'System optimization performed',
        'Daily backup completed'
    ];
    
    activities.forEach(activity => {
        addToActivityList(activity);
    });
}

function addToActivityList(activity) {
    const activityList = document.querySelector('.activity-list');
    const activityItem = document.createElement('div');
    activityItem.classList.add('activity-item');
    activityItem.innerHTML = `
        <span class="activity-time">${formatTime(new Date())}</span>
        <span class="activity-text">${activity}</span>
    `;
    activityList.insertBefore(activityItem, activityList.firstChild);
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Error handling
window.onerror = function(msg, url, lineNo, columnNo, error) {
    console.error('Error: ', msg, 'URL: ', url, 'Line: ', lineNo, 'Column: ', columnNo, 'Error object: ', error);
    return false;
};

// API communication
class VisionSyncAPI {
    static async processImage(file) {
        try {
            const formData = new FormData();
            formData.append('image', file);
            
            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error processing image:', error);
            throw error;
        }
    }

    static async getAnalytics() {
        try {
            const response = await fetch('/api/analytics');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching analytics:', error);
            throw error;
        }
    }
}
