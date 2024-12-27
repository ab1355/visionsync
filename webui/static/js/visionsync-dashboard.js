// Initialize Socket.IO connection
const socket = io();

// Dashboard state
let dashboardState = {
    theme: 'discover',
    metrics: {},
    charts: {}
};

// Initialize dashboard when document is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeThemeSwitcher();
    initializeWebSocket();
    initializeMetricsDisplay();
});

// Theme switching functionality
function initializeThemeSwitcher() {
    document.querySelectorAll('.theme-button').forEach(button => {
        button.addEventListener('click', () => {
            const theme = button.textContent.toLowerCase().split(' ')[0];
            switchTheme(theme);
        });
    });
}

function switchTheme(theme) {
    document.body.className = theme;
    dashboardState.theme = theme;
    updateCognitiveState(`Switched to ${theme} mode`);
}

// WebSocket initialization and handlers
function initializeWebSocket() {
    socket.on('connect', () => {
        console.log('Connected to server');
        updateCognitiveState('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        updateCognitiveState('Disconnected from server');
    });

    socket.on('metrics_update', (data) => {
        dashboardState.metrics = data;
        updateDashboard(data);
    });

    socket.on('error', (error) => {
        console.error('WebSocket error:', error);
        showNotification(error.message, 'error');
    });
}

// Metrics display initialization
function initializeMetricsDisplay() {
    // Initialize charts for each space section
    const sections = ['scope', 'plan', 'analyze', 'create', 'execute'];
    sections.forEach(section => {
        const container = document.getElementById(`${section}-metrics`);
        if (container) {
            const canvas = document.createElement('canvas');
            container.appendChild(canvas);
            dashboardState.charts[section] = createChart(canvas, section);
        }
    });
}

// Chart creation
function createChart(canvas, section) {
    return new Chart(canvas, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: `${section.charAt(0).toUpperCase() + section.slice(1)} Metrics`,
                data: [],
                borderColor: getChartColor(section),
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Update dashboard with new metrics
function updateDashboard(data) {
    // Update discover metrics
    if (data.discover) {
        updateDiscoverMetrics(data.discover);
    }

    // Update space metrics
    if (data.space) {
        Object.entries(data.space).forEach(([section, metrics]) => {
            updateSpaceMetrics(section, metrics);
        });
    }

    // Update cognitive indicators
    if (data.cognitive) {
        updateCognitiveIndicators(data.cognitive);
    }
}

// Update discover section metrics
function updateDiscoverMetrics(metrics) {
    const container = document.getElementById('discover-metrics');
    if (!container) return;

    container.innerHTML = `
        <div class="metric-item">
            <span class="metric-label">Processing Rate</span>
            <span class="metric-value">${metrics.processingRate}/s</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Accuracy</span>
            <span class="metric-value">${metrics.accuracy}%</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Active Tasks</span>
            <span class="metric-value">${metrics.activeTasks}</span>
        </div>
    `;
}

// Update space section metrics
function updateSpaceMetrics(section, metrics) {
    const chart = dashboardState.charts[section];
    if (!chart) return;

    chart.data.labels = metrics.labels;
    chart.data.datasets[0].data = metrics.data;
    chart.update();
}

// Update cognitive indicators
function updateCognitiveIndicators(data) {
    document.querySelectorAll('.cognitive-indicator').forEach(indicator => {
        const type = indicator.classList.contains('discover') ? 'discover' : 'space';
        const level = data[type] || 0;
        indicator.style.setProperty('--cognitive-level', `${level}%`);
    });
}

// Update cognitive state display
function updateCognitiveState(state) {
    const stateElement = document.querySelector('.cognitive-state');
    if (stateElement) {
        stateElement.textContent = `Current State: ${state}`;
    }
}

// Utility functions
function getChartColor(section) {
    const colors = {
        scope: '#4A90E2',
        plan: '#2ECC71',
        analyze: '#F1C40F',
        create: '#E74C3C',
        execute: '#9B59B6'
    };
    return colors[section] || '#4A90E2';
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    notification.querySelector('.notification-close').onclick = () => {
        notification.remove();
    };
    
    setTimeout(() => notification.remove(), 5000);
}
