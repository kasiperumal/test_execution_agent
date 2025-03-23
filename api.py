import os
from flask import Flask, jsonify
from fastapi import FastAPI
from test_reader import get_test_cases
from test_executor import execute_karate_tests

# Create FastAPI app
app = FastAPI()


@app.get("/run-tests/{app_id}/{run_id}")
def run_tests(app_id: str, run_id: str):
    """
    API endpoint to retrieve test cases from Redis and execute them.
    Example URL: http://localhost:8000/run-tests/payment-microservice/run-20250322-001
    """
    print(f"📥 Fetching test cases for app_id={app_id}, run_id={run_id}...")

    # Fetch test cases from Redis
    feature_files = get_test_cases(app_id, run_id)

    if feature_files:
        print(f"🚀 Executing Karate tests for {app_id}...")
        result = execute_karate_tests(app_id, run_id)
        return {"message": "Tests executed", "result": result}
    else:
        return {"error": "No test cases found for the given app_id and run_id."}

pp = Flask(__name__)

@app.route('/list-files', methods=['GET'])
def list_files():
    path = "/opt/render/project/src/karate-tests"
    files = os.listdir(path) if os.path.exists(path) else []
    return jsonify(files)

