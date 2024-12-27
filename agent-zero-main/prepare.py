from python.helpers import dotenv, runtime, settings
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
import string
import random

def prepare_environment():
    PrintStyle.standard("Preparing environment...")

    try:
        # Initialize runtime
        runtime.initialize()

        # Generate random root password if not set (for SSH)
        root_pass = dotenv.get_dotenv_value(dotenv.KEY_ROOT_PASSWORD)
        if not root_pass:
            root_pass = "".join(random.choices(string.ascii_letters + string.digits, k=32))
            PrintStyle.standard("Generating new root password...")
        settings.set_root_password(root_pass)

        # Prepare enhancement systems
        prepare_enhancement_systems()

    except Exception as e:
        PrintStyle.error(f"Error in environment preparation: {e}")
        raise e

def prepare_enhancement_systems():
    try:
        # Pattern Recognition System
        pattern_recognition.prepare()
        PrintStyle.standard("Pattern Recognition system prepared")

        # Resource Optimization System
        resource_optimization.prepare()
        PrintStyle.standard("Resource Optimization system prepared")

        # Learning Integration System
        learning_integration.prepare()
        PrintStyle.standard("Learning Integration system prepared")

        # Multi-Agent Cooperation System
        multi_agent_cooperation.prepare()
        PrintStyle.standard("Multi-Agent Cooperation system prepared")

        # System Evolution
        system_evolution.prepare()
        PrintStyle.standard("System Evolution prepared")

        # Analytics System
        analytics_system.prepare()
        PrintStyle.standard("Analytics System prepared")

        # Interface Enhancement
        interface_enhancement.prepare()
        PrintStyle.standard("Interface Enhancement prepared")

    except Exception as e:
        PrintStyle.error(f"Error in enhancement system preparation: {e}")
        raise e

def verify_environment():
    try:
        # Verify core systems
        runtime.verify()
        settings.verify()

        # Verify enhancement systems
        verify_enhancement_systems()

        PrintStyle.success("Environment verification complete")

    except Exception as e:
        PrintStyle.error(f"Error in environment verification: {e}")
        raise e

def verify_enhancement_systems():
    try:
        # Verify each enhancement system
        pattern_recognition.verify()
        resource_optimization.verify()
        learning_integration.verify()
        multi_agent_cooperation.verify()
        system_evolution.verify()
        analytics_system.verify()
        interface_enhancement.verify()

    except Exception as e:
        PrintStyle.error(f"Error in enhancement system verification: {e}")
        raise e

# Main preparation sequence
try:
    # Prepare environment
    prepare_environment()

    # Verify setup
    verify_environment()

    PrintStyle.success("Environment preparation complete")

except Exception as e:
    PrintStyle.error(f"Critical error in preparation: {e}")
    raise e
