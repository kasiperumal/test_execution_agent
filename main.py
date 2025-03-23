from test_reader import get_test_cases
from test_executor import execute_karate_tests

def main():
    print("📥 executing Test Execution Agent...")
    # Define app_id and run_id
    app_id = "payment-microservice"
    run_id = "run-20250322-001"

    retrieve_and_execute_testcases(app_id, run_id)


def retrieve_and_execute_testcases(app_id, run_id):
    print("📥 Fetching test cases from Redis...")
    feature_files = get_test_cases(app_id, run_id)
    if feature_files:
        print("🚀 Executing Karate tests...")
        result = execute_karate_tests(app_id, run_id)
        print("📥 Fetching test cases from Redis...", result)
        #return {"message": "Tests executed", "result": result}
    else:
        print("❌ No feature files found. Skipping execution.")


if __name__ == "__main__":
    main()
