import asyncio
import sys
import threading, time, models, os
from ansio import application_keypad, mouse_input, raw_input
from ansio.input import InputEvent, get_input_event
from agent import AgentContext, UserMessage
from python.helpers.print_style import PrintStyle
from python.helpers.files import read_file
from python.helpers import files
import python.helpers.timed_input as timed_input
from initialize import initialize
from python.helpers.dotenv import load_dotenv
from python.systems import (
    pattern_recognition,
    resource_optimization,
    learning_integration,
    multi_agent_cooperation,
    system_evolution,
    analytics_system,
    interface_enhancement
)

context: AgentContext = None # type: ignore
input_lock = threading.Lock()

# Main conversation loop
async def chat(context: AgentContext):
    # Initialize enhancement systems
    await initialize_enhancement_systems(context)
    
    # start the conversation loop
    while True:
        try:
            # Process through interface enhancement
            user_input = await get_user_input(context)
            
            # Exit check
            if user_input.lower() == 'e': 
                break

            # Process through enhancement systems
            enhanced_input = await process_input_through_systems(context, user_input)
            
            # Send message to agent0
            assistant_response = await context.communicate(UserMessage(enhanced_input, [])).result()
            
            # Process response through enhancement systems
            enhanced_response = await process_response_through_systems(context, assistant_response)
            
            # Format and display response
            await display_enhanced_response(context, enhanced_response)
            
            # Update analytics and evolution
            await update_system_metrics(context, user_input, enhanced_response)
            
        except Exception as e:
            PrintStyle.error(f"Error in chat loop: {e}")

async def initialize_enhancement_systems(context):
    """Initialize all enhancement systems"""
    try:
        await pattern_recognition.initialize(context)
        await resource_optimization.initialize(context)
        await learning_integration.initialize(context)
        await multi_agent_cooperation.initialize(context)
        await system_evolution.initialize(context)
        await analytics_system.initialize(context)
        await interface_enhancement.initialize(context)
    except Exception as e:
        PrintStyle.error(f"Error initializing enhancement systems: {e}")

async def get_user_input(context):
    """Get enhanced user input"""
    with input_lock:
        timeout = context.agent0.get_data("timeout")
        
        if not timeout:
            # Standard input
            PrintStyle(background_color="#6C3483", font_color="white", bold=True, padding=True).print(
                f"User message ('e' to leave):"
            )
            if sys.platform != "win32": 
                import readline
            user_input = input("> ")
            PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")
            
        else:
            # Timed input
            PrintStyle(background_color="#6C3483", font_color="white", bold=True, padding=True).print(
                f"User message ({timeout}s timeout, 'w' to wait, 'e' to leave):"
            )
            if sys.platform != "win32": 
                import readline
            user_input = timeout_input("> ", timeout=timeout)
            
            if not user_input:
                user_input = context.agent0.read_prompt("fw.msg_timeout.md")
                PrintStyle(font_color="white", padding=False).stream(f"{user_input}")
            else:
                user_input = user_input.strip()
                if user_input.lower()=="w":
                    user_input = input("> ").strip()
                PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")
                
        return user_input

async def process_input_through_systems(context, user_input):
    """Process input through enhancement systems"""
    try:
        # Pattern recognition
        patterns = await context.pattern_engine.process_input(user_input)
        
        # Resource optimization
        resources = await context.resource_manager.optimize_for_input(user_input)
        
        # Learning integration
        learned = await context.learning_engine.process_input(user_input)
        
        # Combine enhancements
        enhanced_input = await interface_enhancement.enhance_input(
            user_input, patterns, resources, learned
        )
        
        return enhanced_input
        
    except Exception as e:
        PrintStyle.error(f"Error processing input through systems: {e}")
        return user_input

async def process_response_through_systems(context, response):
    """Process response through enhancement systems"""
    try:
        # Analytics processing
        analytics = await context.analytics_engine.analyze_response(response)
        
        # Evolution processing
        evolved = await context.evolution_engine.evolve_response(response)
        
        # Interface enhancement
        enhanced = await context.interface_engine.enhance_response(
            response, analytics, evolved
        )
        
        return enhanced
        
    except Exception as e:
        PrintStyle.error(f"Error processing response through systems: {e}")
        return response

async def display_enhanced_response(context, response):
    """Display enhanced response"""
    PrintStyle(font_color="white",background_color="#1D8348", bold=True, padding=True).print(
        f"{context.agent0.agent_name}: response:"
    )
    PrintStyle(font_color="white").print(f"{response}")

async def update_system_metrics(context, user_input, response):
    """Update analytics and evolution metrics"""
    try:
        # Update analytics
        await context.analytics_engine.update_metrics(user_input, response)
        
        # Update evolution
        await context.evolution_engine.update_metrics(user_input, response)
        
    except Exception as e:
        PrintStyle.error(f"Error updating system metrics: {e}")

# User intervention during agent streaming
def intervention():
    if context.streaming_agent and not context.paused:
        context.paused = True
        PrintStyle(background_color="#6C3483", font_color="white", bold=True, padding=True).print(
            f"User intervention ('e' to leave, empty to continue):"
        )
        
        if sys.platform != "win32": 
            import readline
        user_input = input("> ").strip()
        PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")
        
        if user_input.lower() == 'e': 
            os._exit(0)
        if user_input: 
            context.streaming_agent.intervention = UserMessage(user_input, [])
        context.paused = False

# Capture keyboard input
def capture_keys():
    global input_lock
    intervent=False            
    while True:
        if intervent: 
            intervention()
        intervent = False
        time.sleep(0.1)
        
        if context.streaming_agent:
            with input_lock, raw_input, application_keypad:
                event: InputEvent | None = get_input_event(timeout=0.1)
                if event and (event.shortcut.isalpha() or event.shortcut.isspace()):
                    intervent=True
                    continue

def timeout_input(prompt, timeout=10):
    return timed_input.timeout_input(prompt=prompt, timeout=timeout)

def run():
    global context
    PrintStyle.standard("Initializing framework...")

    # Load env vars
    load_dotenv()

    # Initialize context
    config = initialize()
    context = AgentContext(config)

    # Start key capture thread
    threading.Thread(target=capture_keys, daemon=True).start()

    # Start chat
    asyncio.run(chat(context))

if __name__ == "__main__":
    PrintStyle.standard("\n\n!!! run_cli.py is now discontinued. run_ui.py serves as both UI and API endpoint !!!\n\n")
    run()