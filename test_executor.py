import yaml
import os
import redis
import json
import datetime
import karate_runner  # Importing the new execution script

# Load configuration from YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize Redis connection using config
redis_config = config.get("redis", {})

redis_client = redis.StrictRedis(
    host=redis_config.get("host", "localhost"),
    port=redis_config.get("port", 6379),
    username=redis_config.get("username"),  # Added username support
    password=redis_config.get("password"),  # Added password support
    db=redis_config.get("db", 0),
    decode_responses=redis_config.get("decode_responses", True)
)


def execute_karate_tests(app_id, run_id):
    """Execute all Karate BDD tests using karate_runner.py and store results in Redis."""

    # Run all Karate feature files using karate_runner.py
    test_status = karate_runner.run_karate_tests()  # Call the new module

    # Generate test execution results
    test_results = {
        "run_id": run_id,
        "app_id": app_id,
        "executed_by": "ExecutionAgent",
        "executed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "success" if test_status["failed"] == 0 else "failed",
        "testcase_count": test_status["scenarios"],
        "passed": test_status["passed"],
        "failed": test_status["failed"],
        "allure_report_url": f"https://s3.example.com/reports/allure/{run_id}/index.html",
        "jacoco_report_url": f"https://s3.example.com/reports/jacoco/{run_id}/index.html"
    }

    # Save results to Redis
    save_results_to_redis(test_results)
    return test_results


def save_results_to_redis(results):
    """Save test execution results to Redis."""
    redis_key = f"reports:execution:{results['app_id']}:{results['run_id']}"
    redis_client.set(redis_key, json.dumps(results, indent=2))
    print(f"✅ Test results saved to Redis under key: {redis_key}")


if __name__ == "__main__":
    # Example execution details
    app_id = "payment-microservice"
    run_id = "run-20250322-001"
    execute_karate_tests(app_id,run_id)