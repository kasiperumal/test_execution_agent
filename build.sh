# !/bin/bash

# ✅ Download and install OpenJDK 11 manually
mkdir -p /opt/java
curl -o /opt/java/openjdk.tar.gz https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_linux-x64_bin.tar.gz
tar -xvzf /opt/java/openjdk.tar.gz -C /opt/java
export JAVA_HOME=/opt/java/jdk-11
export PATH=$JAVA_HOME/bin:$PATH

# ✅ Verify Java installation
java -version

# ✅ Run the Python application
exec python3 -m uvicorn api:app --host 0.0.0.0 --port 10000