FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    ffmpeg \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/python/systems

# Copy the application code
COPY . .

# Create systems module
RUN touch /app/python/systems/__init__.py && \
    grep -A 1000 "# python/systems/pattern_recognition.py" /app/agent.py | grep -B 1000 "# python/systems/resource_optimization.py" > /app/python/systems/pattern_recognition.py && \
    grep -A 1000 "# python/systems/resource_optimization.py" /app/agent.py | grep -B 1000 "# python/systems/learning_integration.py" > /app/python/systems/resource_optimization.py && \
    grep -A 1000 "# python/systems/learning_integration.py" /app/agent.py | grep -B 1000 "# python/systems/multi_agent_cooperation.py" > /app/python/systems/learning_integration.py && \
    grep -A 1000 "# python/systems/multi_agent_cooperation.py" /app/agent.py | grep -B 1000 "# python/systems/system_evolution.py" > /app/python/systems/multi_agent_cooperation.py && \
    grep -A 1000 "# python/systems/system_evolution.py" /app/agent.py | grep -B 1000 "# python/systems/analytics_system.py" > /app/python/systems/system_evolution.py && \
    grep -A 1000 "# python/systems/analytics_system.py" /app/agent.py | grep -B 1000 "# python/systems/interface_enhancement.py" > /app/python/systems/analytics_system.py && \
    grep -A 1000 "# python/systems/interface_enhancement.py" /app/agent.py | grep -B 1000 "# config/agent_config.py" > /app/python/systems/interface_enhancement.py

# Set permissions
RUN chmod -R 755 /app

# Set environment variables
ENV FLASK_APP=run_ui.py \
    BASIC_AUTH_USERNAME=admin \
    BASIC_AUTH_PASSWORD=admin \
    VISIONSYNC_METRICS_UPDATE_INTERVAL=2 \
    VISIONSYNC_LOG_LEVEL=INFO \
    PYTHONPATH=/app:/app/python

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000", "--debug"]
