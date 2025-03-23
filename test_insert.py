import yaml
import redis
import json

# Connect to Redis
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()  # Check if Redis is reachable
except Exception as e:
    print(f"❌ Redis Connection Error: {e}")
    exit(1)

def insert_bdd_tests():
# Define the JSON data
    test_data = {
        "run_id": "run-20250322-001",
        "app_id": "payment-microservice",
        "approved_at": "2025-03-22T09:00:00Z",
        "approved_by": "developer1@example.com",
        "testcases": [
            {
                "id": "TC002",
                "title": "Verify GET endpoint",
                "karate_test": """Feature: Payment Transactions API
      Background:
        * url 'https://payment-microservice-a65j.onrender.com'

      Scenario: Verify GET endpoint
        Given path '/api/transactions'
        When method get
        Then status 200"""
            },
{
                "id": "TC004",
                "title": "Verify GET endpoint",
                "karate_test": """Feature: Payment Transactions API
      Background:
        * url 'https://payment-microservice-a65j.onrender.com'

      Scenario: Verify GET endpoint
        Given path '/api/transactions'
        When method get
        Then status 500"""
            }
        ]
    }

    # Generate Redis key
    redis_key = f"testcases:approved:{test_data['app_id']}:{test_data['run_id']}"

    # Store JSON data in Redis
    redis_client.set(redis_key, json.dumps(test_data))

    print(f"✅ Data successfully inserted into Redis with key: {redis_key}")


if __name__ == "__main__":
    insert_bdd_tests()