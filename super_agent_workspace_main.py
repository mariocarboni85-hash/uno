# Entry point per collegare il workspace principale alla struttura super_agent_workspace

def main():
    from super_agent_workspace.ai.ai_integration import start_workspace
    start_workspace()

if __name__ == "__main__":
    main()
