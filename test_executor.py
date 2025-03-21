import subprocess
import yaml
import os
import redis
import datetime

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Connect to Redis
redis_client = redis.Redis(
    host=config["redis_host"],
    port=config["redis_port"],
    db=config["redis_db"],
    decode_responses=True
)


def run_karate_tests():
    #test_folder = os.path.join("test_repo", config["test_folder"])
    test_folder = config["test_folder"]

    if not os.path.exists(test_folder):
        print("Test folder not found!")
        return

    karate_cmd = f"mvn test -Dkarate.options='{test_folder}'"

    print(f"Running Karate tests: {karate_cmd}")
    process = subprocess.run(karate_cmd, shell=True, capture_output=True, text=True)

    test_results = process.stdout
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store results in a Redis hash
    redis_key = f"karate_test:{timestamp}"
    redis_client.hset(redis_key, mapping={"timestamp": timestamp, "results": test_results})

    print(f"Karate test results saved in Redis under key: {redis_key}")


if __name__ == "__main__":
    run_karate_tests()
