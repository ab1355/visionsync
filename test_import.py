import sys
print("Python path:", sys.path)
print("\nTrying to import visionsync...")
try:
    import visionsync
    print("visionsync package location:", visionsync.__file__)
    print("visionsync contents:", dir(visionsync))
    
    # Try importing specific classes
    from visionsync import Agent, AgentConfig
    print("\nSuccessfully imported Agent and AgentConfig")
    print("Agent:", Agent)
    print("AgentConfig:", AgentConfig)
except ImportError as e:
    print("Import error:", e)
except Exception as e:
    print("Other error:", e)
