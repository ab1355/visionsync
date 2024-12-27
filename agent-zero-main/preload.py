import asyncio
from python.helpers import runtime, whisper, settings
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

PrintStyle().print("Running preload...")
runtime.initialize()

async def preload():
    try:
        set = settings.get_default_settings()

        # async tasks to preload
        tasks = [
            # Core systems
            whisper.preload(set["stt_model_size"]),
            
            # Enhancement systems
            pattern_recognition.preload(),
            resource_optimization.preload(),
            learning_integration.preload(),
            multi_agent_cooperation.preload(),
            system_evolution.preload(),
            analytics_system.preload(),
            interface_enhancement.preload()
        ]

        return asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        PrintStyle().print(f"Error in preload: {e}")

async def preload_enhancement_systems():
    """Preload all enhancement systems"""
    try:
        # Pattern Recognition
        await pattern_recognition.preload()
        PrintStyle().print("Pattern Recognition system loaded")

        # Resource Optimization
        await resource_optimization.preload()
        PrintStyle().print("Resource Optimization system loaded")

        # Learning Integration
        await learning_integration.preload()
        PrintStyle().print("Learning Integration system loaded")

        # Multi-Agent Cooperation
        await multi_agent_cooperation.preload()
        PrintStyle().print("Multi-Agent Cooperation system loaded")

        # System Evolution
        await system_evolution.preload()
        PrintStyle().print("System Evolution loaded")

        # Analytics System
        await analytics_system.preload()
        PrintStyle().print("Analytics System loaded")

        # Interface Enhancement
        await interface_enhancement.preload()
        PrintStyle().print("Interface Enhancement loaded")

    except Exception as e:
        PrintStyle().print(f"Error in enhancement system preload: {e}")
        raise e

# preload transcription model and enhancement systems
asyncio.run(preload())
