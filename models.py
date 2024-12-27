from enum import Enum
import os
from typing import Any
from langchain_openai import (
    ChatOpenAI,
    OpenAI,
    OpenAIEmbeddings,
    AzureChatOpenAI,
    AzureOpenAIEmbeddings,
    AzureOpenAI,
)
from langchain_community.llms.ollama import Ollama
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_google_genai import (
    GoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
    embeddings as google_embeddings,
)
from langchain_mistralai import ChatMistralAI
from pydantic.v1.types import SecretStr
from python.helpers import dotenv, runtime
from python.helpers.dotenv import load_dotenv
from python.helpers.rate_limiter import RateLimiter

# environment variables
load_dotenv()

# Configuration
DEFAULT_TEMPERATURE = 0.0

class ModelType(Enum):
    CHAT = "Chat"
    EMBEDDING = "Embedding"
    PATTERN = "Pattern"
    LEARNING = "Learning"
    ANALYTICS = "Analytics"
    EVOLUTION = "Evolution"

class ModelProvider(Enum):
    ANTHROPIC = "Anthropic"
    GOOGLE = "Google"
    GROQ = "Groq"
    LMSTUDIO = "LM Studio"
    MISTRALAI = "Mistral AI"
    OLLAMA = "Ollama"
    OPENAI = "OpenAI"
    OPENAI_AZURE = "OpenAI Azure"
    OPENROUTER = "OpenRouter"
    SAMBANOVA = "Sambanova"
    OTHER = "Other"

rate_limiters: dict[str, RateLimiter] = {}

def get_api_key(service):
    return (
        dotenv.get_dotenv_value(f"API_KEY_{service.upper()}")
        or dotenv.get_dotenv_value(f"{service.upper()}_API_KEY")
        or "None"
    )

def get_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    fnc_name = f"get_{provider.name.lower()}_{type.name.lower()}"
    model = globals()[fnc_name](name, **kwargs)
    return model

def get_rate_limiter(
    provider: ModelProvider, name: str, requests: int, input: int, output: int
) -> RateLimiter:
    key = f"{provider.name}\\{name}"
    rate_limiters[key] = limiter = rate_limiters.get(key, RateLimiter(seconds=60))
    limiter.limits["requests"] = requests or 0
    limiter.limits["input"] = input or 0
    limiter.limits["output"] = output or 0
    return limiter

def parse_chunk(chunk: Any):
    if isinstance(chunk, str):
        content = chunk
    elif hasattr(chunk, "content"):
        content = str(chunk.content)
    else:
        content = str(chunk)
    return content

# Model getter functions for each type
def get_pattern_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    """Get pattern recognition model"""
    fnc_name = f"get_{provider.name.lower()}_pattern"
    model = globals()[fnc_name](name, **kwargs)
    return model

def get_learning_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    """Get learning model"""
    fnc_name = f"get_{provider.name.lower()}_learning"
    model = globals()[fnc_name](name, **kwargs)
    return model

def get_analytics_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    """Get analytics model"""
    fnc_name = f"get_{provider.name.lower()}_analytics"
    model = globals()[fnc_name](name, **kwargs)
    return model

def get_evolution_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    """Get evolution model"""
    fnc_name = f"get_{provider.name.lower()}_evolution"
    model = globals()[fnc_name](name, **kwargs)
    return model

# Provider-specific implementations
def get_openai_chat(
    model_name: str,
    api_key=None,
    temperature=DEFAULT_TEMPERATURE,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("openai")
    return ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

def get_openai_embedding(model_name: str, api_key=None, **kwargs):
    if not api_key:
        api_key = get_api_key("openai")
    return OpenAIEmbeddings(model=model_name, api_key=api_key, **kwargs)

def get_openai_pattern(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE, **kwargs):
    if not api_key:
        api_key = get_api_key("openai")
    return ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

def get_openai_learning(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE, **kwargs):
    if not api_key:
        api_key = get_api_key("openai")
    return ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

def get_openai_analytics(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE, **kwargs):
    if not api_key:
        api_key = get_api_key("openai")
    return ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

def get_openai_evolution(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE, **kwargs):
    if not api_key:
        api_key = get_api_key("openai")
    return ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

# Add similar implementations for other providers
def get_anthropic_chat(
    model_name: str,
    api_key=None,
    temperature=DEFAULT_TEMPERATURE,
    **kwargs,
):
    if not api_key:
        api_key = get_api_key("anthropic")
    return ChatAnthropic(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

def get_anthropic_pattern(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE, **kwargs):
    if not api_key:
        api_key = get_api_key("anthropic")
    return ChatAnthropic(model_name=model_name, temperature=temperature, api_key=api_key, **kwargs)

# Continue with other provider implementations...

# Utility functions
def get_ollama_base_url():
    return (
        dotenv.get_dotenv_value("OLLAMA_BASE_URL")
        or f"http://{runtime.get_local_url()}:11434"
    )

def get_lmstudio_base_url():
    return (
        dotenv.get_dotenv_value("LM_STUDIO_BASE_URL")
        or f"http://{runtime.get_local_url()}:1234/v1"
    )