#!/bin/bash

# ✅ Install Java (OpenJDK 11)
apt-get update && apt-get install -y openjdk-11-jdk

# ✅ Verify Java installation
java -version

# ✅ Run the Python application
exec python3 -m uvicorn api:app --host 0.0.0.0 --port 10000