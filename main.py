from workflows.app_workflow import build_workflow

def main():
    workflow = build_workflow()
    initial_state = {}  # Populate with initial state data as required
    final_state = workflow.invoke(initial_state)
    print("Workflow execution completed.")
    print("Final State:", final_state)

if __name__ == "__main__":
    main()