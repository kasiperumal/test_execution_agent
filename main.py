import git_handler
import test_executor

def main():
    print("Starting TestExecutionAgent...")
    #git_handler.clone_or_update_repo()
    test_executor.run_karate_tests()
    print("Test execution finished.")

if __name__ == "__main__":
    main()
