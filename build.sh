# Install Java (OpenJDK 17)
apt-get update && apt-get install -y openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
java -version  # Verify Java installation

# ✅ Run the Python application
exec python3 -m uvicorn api:app --host 0.0.0.0 --port 10000