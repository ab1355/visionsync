class CognitiveEnhancement {
    constructor() {
        this.currentState = 'neutral';
        this.focusLevel = 0;
        this.interactionCount = 0;
        this.thoughtPatterns = [];
        this.initialize();
    }

    initialize() {
        this.setupInteractionTracking();
        this.setupCognitivePatterns();
        this.setupMindMapping();
        this.startBrainwaveSimulation();
    }

    setupInteractionTracking() {
        document.addEventListener('mousemove', (e) => {
            this.updateFocusZone(e);
            this.updateBrainwavePattern(e);
        });

        document.addEventListener('click', (e) => {
            this.createRippleEffect(e);
            this.incrementInteraction();
            this.generateThoughtBubble(e);
        });
    }

    updateFocusZone(e) {
        const focusZone = document.querySelector('.focus-zone');
        if (!focusZone) return;
        
        const x = e.clientX;
        const y = e.clientY;
        
        focusZone.style.opacity = '0.2';
        focusZone.style.transform = `translate(${x - 100}px, ${y - 100}px)`;
        
        setTimeout(() => {
            focusZone.style.opacity = '0';
        }, 1000);
    }

    createRippleEffect(e) {
        const ripple = document.createElement('div');
        ripple.className = 'interaction-ripple';
        ripple.style.left = e.clientX + 'px';
        ripple.style.top = e.clientY + 'px';
        document.body.appendChild(ripple);
        
        ripple.addEventListener('animationend', () => {
            ripple.remove();
        });
    }

    generateThoughtBubble(e) {
        const thoughts = [
            'Connecting patterns...',
            'Analyzing structure...',
            'Exploring possibilities...',
            'Synthesizing ideas...',
            'Building connections...'
        ];

        const bubble = document.createElement('div');
        bubble.className = 'thought-bubble';
        bubble.textContent = thoughts[Math.floor(Math.random() * thoughts.length)];
        bubble.style.left = (e.clientX + 10) + 'px';
        bubble.style.top = (e.clientY - 40) + 'px';
        document.body.appendChild(bubble);

        requestAnimationFrame(() => {
            bubble.style.opacity = '1';
            bubble.style.transform = 'translateY(0)';
        });

        setTimeout(() => {
            bubble.style.opacity = '0';
            setTimeout(() => bubble.remove(), 300);
        }, 1500);
    }

    setupCognitivePatterns() {
        const cards = document.querySelectorAll('.space-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.currentState = 'focused';
                this.updateCognitiveState('Focused: Deep Analysis');
            });

            card.addEventListener('mouseleave', () => {
                this.currentState = 'exploring';
                this.updateCognitiveState('Exploring: Pattern Recognition');
            });
        });
    }

    updateCognitiveState(state) {
        const stateElement = document.querySelector('.cognitive-state');
        if (!stateElement) return;
        
        stateElement.textContent = state;
        stateElement.style.borderColor = getComputedStyle(document.documentElement)
            .getPropertyValue('--theme-primary');
    }

    startBrainwaveSimulation() {
        const indicator = document.querySelector('.brain-wave-indicator');
        if (!indicator) return;
        
        let phase = 0;
        setInterval(() => {
            const amplitude = 20 * Math.sin(phase);
            indicator.style.transform = `translateX(-50%) translateY(${amplitude}px)`;
            phase += 0.1;
        }, 50);
    }

    setupMindMapping() {
        const cards = document.querySelectorAll('.space-card');
        cards.forEach((card, index) => {
            if (index < cards.length - 1) {
                const connector = document.createElement('div');
                connector.className = 'mind-map-connector';
                card.appendChild(connector);
            }
        });
    }
}

class VisionSyncDashboard {
    constructor() {
        this.cognitiveEnhancement = new CognitiveEnhancement();
        this.websocket = null;
        this.initialize();
    }

    initialize() {
        this.setupWebSocket();
        this.setupThemeSwitching();
        this.setupInteractions();
    }

    setupWebSocket() {
        this.websocket = new WebSocket(`ws://${window.location.host}/ws`);
        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateMetrics(data);
        };
    }

    setupThemeSwitching() {
        const themes = {
            discover: {
                primary: '#6e00ff',
                secondary: '#00e5ff',
                accent: '#ff00e5'
            },
            space: {
                primary: '#00ff9d',
                secondary: '#4d908e',
                accent: '#277da1'
            },
            flow: {
                primary: '#ff6b6b',
                secondary: '#ffd93d',
                accent: '#ff8600'
            }
        };

        document.querySelectorAll('.theme-button').forEach(button => {
            button.addEventListener('click', () => {
                const theme = button.textContent.toLowerCase().split(' ')[0];
                this.switchTheme(theme, themes[theme]);
            });
        });
    }

    switchTheme(themeName, colors) {
        document.documentElement.style.setProperty('--theme-primary', colors.primary);
        document.documentElement.style.setProperty('--theme-secondary', colors.secondary);
        document.documentElement.style.setProperty('--theme-accent', colors.accent);
        
        const pulse = document.createElement('div');
        pulse.className = 'cognitive-pulse';
        pulse.style.background = `radial-gradient(circle, ${colors.primary}22, transparent)`;
        document.body.appendChild(pulse);
        
        setTimeout(() => pulse.remove(), 4000);
    }

    updateMetrics(data) {
        ['discover', 'space', 'flow'].forEach(section => {
            if (data[section]) {
                Object.entries(data[section]).forEach(([key, value]) => {
                    const container = document.getElementById(`${key}-metrics`);
                    if (container) {
                        container.innerHTML = this.createMetricCard(key, value, section);
                    }
                });
            }
        });
    }

    createMetricCard(title, value, section) {
        return `
<div class="metric-card">
<div class="metric-title">${title}</div>
<div class="cognitive-indicator ${section}"></div>
<div class="metric-value">${value}</div>
</div>
`;
    }

    setupInteractions() {
        document.querySelectorAll('.space-card').forEach(card => {
            card.addEventListener('click', () => {
                this.trackInteraction(card.dataset.section, 'click');
            });
        });
    }

    trackInteraction(section, action) {
        fetch('/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                section,
                action,
                timestamp: new Date().toISOString()
            })
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.visionSync = new VisionSyncDashboard();
});