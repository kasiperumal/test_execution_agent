import redis
import yaml

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

def fetch_latest_results():
    keys = redis_client.keys("karate_test:*")
    if not keys:
        print("No test results found.")
        return
    
    latest_key = sorted(keys)[-1]  # Get the most recent test result
    test_results = redis_client.hgetall(latest_key)
    
    print(f"Latest test results ({latest_key}):\n{test_results['results']}")

if __name__ == "__main__":
    fetch_latest_results()
