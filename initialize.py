import asyncio
import models
from agent import AgentConfig, ModelConfig
from python.helpers import dotenv, files, rfc_exchange, runtime, settings, docker, log
from python.systems import pattern_recognition, resource_optimization, learning_integration
from python.systems import multi_agent_cooperation, system_evolution, analytics_system, interface_enhancement

def initialize():
    current_settings = settings.get_settings()

    # chat model from user settings
    chat_llm = ModelConfig(
        provider=models.ModelProvider[current_settings["chat_model_provider"]],
        name=current_settings["chat_model_name"],
        ctx_length=current_settings["chat_model_ctx_length"],
        limit_requests=current_settings["chat_model_rl_requests"],
        limit_input=current_settings["chat_model_rl_input"],
        limit_output=current_settings["chat_model_rl_output"],
        kwargs={
            "temperature": current_settings["chat_model_temperature"],
            **current_settings["chat_model_kwargs"],
        },
    )

    # utility model from user settings
    utility_llm = ModelConfig(
        provider=models.ModelProvider[current_settings["util_model_provider"]],
        name=current_settings["util_model_name"],
        ctx_length=current_settings["util_model_ctx_length"],
        limit_requests=current_settings["util_model_rl_requests"],
        limit_input=current_settings["util_model_rl_input"],
        limit_output=current_settings["util_model_rl_output"],
        kwargs={
            "temperature": current_settings["util_model_temperature"],
            **current_settings["util_model_kwargs"],
        },
    )

    # embedding model from user settings
    embedding_llm = ModelConfig(
        provider=models.ModelProvider[current_settings["embed_model_provider"]],
        name=current_settings["embed_model_name"],
        ctx_length=0,
        limit_requests=current_settings["embed_model_rl_requests"],
        limit_input=0,
        limit_output=0,
        kwargs={
            **current_settings["embed_model_kwargs"],
        },
    )

    # Enhancement configurations
    pattern_recognition_config = {
        "similarity_threshold": current_settings.get("pattern_similarity_threshold", 0.75),
        "learning_rate": current_settings.get("pattern_learning_rate", 0.1),
        "min_examples": current_settings.get("pattern_min_examples", 5)
    }

    resource_optimization_config = {
        "optimization_threshold": current_settings.get("resource_optimization_threshold", 0.8),
        "allocation_strategy": current_settings.get("resource_allocation_strategy", "dynamic")
    }

    learning_integration_config = {
        "learning_rate": current_settings.get("learning_rate", 0.1),
        "experience_threshold": current_settings.get("experience_threshold", 0.7)
    }

    multi_agent_config = {
        "team_size": current_settings.get("team_size", 5),
        "coordination_threshold": current_settings.get("coordination_threshold", 0.8)
    }

    evolution_config = {
        "evolution_rate": current_settings.get("evolution_rate", 0.2),
        "adaptation_threshold": current_settings.get("adaptation_threshold", 0.7)
    }

    analytics_config = {
        "data_window": current_settings.get("analytics_data_window", 1000),
        "confidence_threshold": current_settings.get("analytics_confidence_threshold", 0.8)
    }

    interface_config = {
        "interaction_memory": current_settings.get("interface_memory", 1000),
        "adaptation_rate": current_settings.get("interface_adaptation_rate", 0.15)
    }

    # agent configuration
    config = AgentConfig(
        chat_model=chat_llm,
        utility_model=utility_llm,
        embeddings_model=embedding_llm,
        prompts_subdir=current_settings["agent_prompts_subdir"],
        memory_subdir=current_settings["agent_memory_subdir"],
        knowledge_subdirs=["default", current_settings["agent_knowledge_subdir"]],
        
        # Enhancement configurations
        pattern_recognition=pattern_recognition_config,
        resource_optimization=resource_optimization_config,
        learning_integration=learning_integration_config,
        multi_agent_cooperation=multi_agent_config,
        system_evolution=evolution_config,
        analytics_system=analytics_config,
        interface_system=interface_config,
        
        code_exec_docker_enabled=False,
    )

    # update SSH and docker settings
    set_runtime_config(config, current_settings)

    # update config with runtime args
    args_override(config)

    # return config object
    return config

def args_override(config):
    # update config with runtime args
    for key, value in runtime.args.items():
        if hasattr(config, key):
            # conversion based on type of config[key]
            if isinstance(getattr(config, key), bool):
                value = value.lower().strip() == "true"
            elif isinstance(getattr(config, key), int):
                value = int(value)
            elif isinstance(getattr(config, key), float):
                value = float(value)
            elif isinstance(getattr(config, key), str):
                value = str(value)
            elif isinstance(getattr(config, key), dict):
                # Handle dictionary configurations
                current_dict = getattr(config, key)
                try:
                    value = eval(value)
                    if isinstance(value, dict):
                        current_dict.update(value)
                        value = current_dict
                except:
                    pass
            else:
                raise Exception(
                    f"Unsupported argument type of '{key}': {type(getattr(config, key))}"
                )

            setattr(config, key, value)

def set_runtime_config(config: AgentConfig, set: settings.Settings):
    ssh_conf = settings.get_runtime_config(set)
    for key, value in ssh_conf.items():
        if hasattr(config, key):
            setattr(config, key, value)