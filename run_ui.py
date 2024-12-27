import asyncio
from functools import wraps
import os
import threading
from flask import Flask, request, Response, jsonify
from flask_basicauth import BasicAuth
from flask_socketio import SocketIO, emit
from datetime import datetime
import random
import time
from python.helpers import errors, files, git
from python.helpers.files import get_abs_path
from python.helpers import persist_chat, runtime, dotenv, process
from python.helpers.api import ApiHandler
from python.helpers.print_style import PrintStyle
from python.systems import (
    pattern_recognition,
    resource_optimization, 
    learning_integration,
    multi_agent_cooperation,
    system_evolution,
    analytics_system,
    interface_enhancement
)
from python.helpers.error_handler import error_handler, ErrorContext
from python.helpers.resource_manager import resource_manager

# initialize the internal Flask server
app = Flask("app", static_folder=get_abs_path("./webui"), static_url_path="/")
app.config["JSON_SORT_KEYS"] = False

lock = threading.Lock()
enhancement_systems = []

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

class DashboardMetrics:
    def __init__(self):
        self.metrics = {
            "discover": {
                "processingRate": 0,
                "accuracy": 0,
                "activeTasks": 0
            },
            "space": {
                "scope": {"data": [], "labels": []},
                "plan": {"data": [], "labels": []},
                "analyze": {"data": [], "labels": []}
            }
        }

# Initialize dashboard metrics
dashboard_metrics = DashboardMetrics()

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

@app.route("/api/settings", methods=['GET'])
def get_settings():
    settings = {
        "models": {
            "providers": [
                {"id": "openai", "name": "OpenAI"},
                {"id": "anthropic", "name": "Anthropic"},
                {"id": "ollama", "name": "Ollama"},
                {"id": "google", "name": "Google"},
                {"id": "groq", "name": "Groq"},
                {"id": "mistral", "name": "Mistral"}
            ],
            "models": {
                "openai": [
                    {"id": "gpt-4", "name": "GPT-4"},
                    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
                ],
                "anthropic": [
                    {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
                    {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
                    {"id": "claude-2.1", "name": "Claude 2.1"}
                ],
                "ollama": [
                    {"id": "mistral", "name": "Mistral"},
                    {"id": "llama2", "name": "Llama 2"},
                    {"id": "codellama", "name": "Code Llama"}
                ],
                "google": [
                    {"id": "gemini-pro", "name": "Gemini Pro"}
                ],
                "groq": [
                    {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"},
                    {"id": "llama2-70b-4096", "name": "Llama 2 70B"}
                ],
                "mistral": [
                    {"id": "mistral-medium", "name": "Mistral Medium"},
                    {"id": "mistral-small", "name": "Mistral Small"},
                    {"id": "mistral-tiny", "name": "Mistral Tiny"}
                ]
            }
        },
        "api_keys": {
            "openai": dotenv.get_dotenv_value("OPENAI_API_KEY", ""),
            "anthropic": dotenv.get_dotenv_value("ANTHROPIC_API_KEY", ""),
            "google": dotenv.get_dotenv_value("GOOGLE_API_KEY", ""),
            "groq": dotenv.get_dotenv_value("GROQ_API_KEY", ""),
            "mistral": dotenv.get_dotenv_value("MISTRAL_API_KEY", "")
        },
        "selected": {
            "provider": dotenv.get_dotenv_value("PROVIDER", "ollama"),
            "model": dotenv.get_dotenv_value("MODEL", "mistral")
        }
    }
    return jsonify(settings)

@app.route("/api/settings", methods=['POST'])
def update_settings():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update .env file with new settings
    if "provider" in data:
        dotenv.set_dotenv_value("PROVIDER", data["provider"])
    if "model" in data:
        dotenv.set_dotenv_value("MODEL", data["model"])
    if "api_keys" in data:
        for provider, key in data["api_keys"].items():
            if key:  # Only update if key is not empty
                dotenv.set_dotenv_value(f"{provider.upper()}_API_KEY", key)
    
    return jsonify({"status": "success"})

@app.route("/settings_get", methods=['POST'])
def settings_get():
    settings = {
        "settings": {
            "sections": [
                {
                    "title": "Model Settings",
                    "fields": [
                        {
                            "id": "provider",
                            "title": "Provider",
                            "type": "select",
                            "options": [
                                {"id": "openai", "title": "OpenAI"},
                                {"id": "anthropic", "title": "Anthropic"},
                                {"id": "ollama", "title": "Ollama"},
                                {"id": "google", "title": "Google"},
                                {"id": "groq", "title": "Groq"},
                                {"id": "mistral", "title": "Mistral"}
                            ],
                            "value": dotenv.get_dotenv_value("PROVIDER", "ollama")
                        },
                        {
                            "id": "model",
                            "title": "Model",
                            "type": "select",
                            "options": [],  # Will be populated by frontend based on provider
                            "value": dotenv.get_dotenv_value("MODEL", "mistral")
                        }
                    ]
                },
                {
                    "title": "API Keys",
                    "fields": [
                        {
                            "id": "openai_api_key",
                            "title": "OpenAI API Key",
                            "type": "password",
                            "value": dotenv.get_dotenv_value("OPENAI_API_KEY", "")
                        },
                        {
                            "id": "anthropic_api_key",
                            "title": "Anthropic API Key",
                            "type": "password",
                            "value": dotenv.get_dotenv_value("ANTHROPIC_API_KEY", "")
                        },
                        {
                            "id": "google_api_key",
                            "title": "Google API Key",
                            "type": "password",
                            "value": dotenv.get_dotenv_value("GOOGLE_API_KEY", "")
                        },
                        {
                            "id": "groq_api_key",
                            "title": "Groq API Key",
                            "type": "password",
                            "value": dotenv.get_dotenv_value("GROQ_API_KEY", "")
                        },
                        {
                            "id": "mistral_api_key",
                            "title": "Mistral API Key",
                            "type": "password",
                            "value": dotenv.get_dotenv_value("MISTRAL_API_KEY", "")
                        }
                    ]
                }
            ]
        }
    }
    return jsonify(settings)

@app.route("/settings_set", methods=['POST'])
def settings_set():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    for section in data.get("sections", []):
        for field in section.get("fields", []):
            field_id = field.get("id")
            value = field.get("value", "")
            
            if field_id == "provider":
                dotenv.set_dotenv_value("PROVIDER", value)
            elif field_id == "model":
                dotenv.set_dotenv_value("MODEL", value)
            elif field_id.endswith("_api_key"):
                provider = field_id.replace("_api_key", "").upper()
                if value:  # Only update if value is not empty
                    dotenv.set_dotenv_value(f"{provider}_API_KEY", value)
    
    return jsonify({"status": "success"})

def initialize_enhancement_systems():
    global enhancement_systems
    enhancement_systems = [
        pattern_recognition.PatternRecognitionSystem(),
        resource_optimization.ResourceOptimizationSystem(),
        learning_integration.LearningIntegrationSystem(),
        multi_agent_cooperation.MultiAgentCooperationSystem(),
        system_evolution.SystemEvolutionSystem(),
        analytics_system.AnalyticsSystem(),
        interface_enhancement.InterfaceEnhancementSystem()
    ]

def cleanup_systems():
    global enhancement_systems
    for system in enhancement_systems:
        if hasattr(system, 'cleanup'):
            system.cleanup()
    enhancement_systems = []

def run():
    runtime.initialize()
    dotenv.load_dotenv()
    
    # Initialize systems
    initialize_enhancement_systems()
    
    try:
        # Start the Flask app
        socketio.run(app, host="127.0.0.1", port=8000, debug=True)
    finally:
        cleanup_systems()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on_error_default
def handle_error(error):
    print(f'An error occurred: {error}')

@app.route('/api/metrics/history', methods=['GET'])
def get_metrics_history():
    return jsonify(dashboard_metrics.metrics)

@app.route('/api/cognitive/state', methods=['GET'])
def get_cognitive_state():
    state = {
        'systemHealth': random.uniform(0.7, 1.0),
        'resourceUtilization': random.uniform(0.3, 0.8),
        'learningProgress': random.uniform(0.4, 0.9)
    }
    return jsonify(state)

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    history = persist_chat.load_chat_history()
    return jsonify(history)

@app.route('/api/chat/history', methods=['POST'])
def save_chat_history():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    persist_chat.save_chat_history(data)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    run()