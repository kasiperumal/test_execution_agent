import yaml
import redis
import json
import os

# Load configuration from YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialize Redis connection using config
redis_config = config.get("redis", {})
redis_client = redis.StrictRedis(
    host=redis_config.get("host", "localhost"),
    port=redis_config.get("port", 6379),
    db=redis_config.get("db", 0),
    decode_responses=redis_config.get("decode_responses", True)
)

def get_test_cases(app_id, run_id):
    """Fetch test cases JSON from Redis and write Karate feature files."""
    redis_key = f"testcases:approved:{app_id}:{run_id}"
    print(f"🔍 Checking Redis key: {redis_key}")

    # Fetch test data
    test_data_json = redis_client.get(redis_key)

    if not test_data_json:
        print(f"❌ Error: No test data found for key {redis_key}")
        return None

    print(f"✅ Found test data: {test_data_json}")

    # Parse JSON
    try:
        test_data = json.loads(test_data_json)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}")
        return None

    testcases = test_data.get("testcases", [])
    if not testcases:
        print("❌ No test cases found in JSON!")
        return None

    # Directory to store Karate feature files
    FEATURES_DIR = os.path.join(os.getcwd(), "karate-tests")
    os.makedirs(FEATURES_DIR, exist_ok=True)

    # Write each test case to a feature file
    feature_files = []
    for testcase in testcases:
        feature_file = os.path.join(FEATURES_DIR, f"{testcase['id']}.feature")
        with open(feature_file, "w", encoding="utf-8") as f:
            f.write(testcase["karate_test"])
        feature_files.append(feature_file)

    print(f"✅ Created {len(feature_files)} Karate feature files in {FEATURES_DIR}")
    return feature_files  # Return the list of feature files

if __name__ == "__main__":
    # Example usage
    app_id = "payment-microservice"
    run_id = "run-20250322-001"
    feature_files = get_test_cases(app_id, run_id)
    print("Feature files generated:",feature_files)