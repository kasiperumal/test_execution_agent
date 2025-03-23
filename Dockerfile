# Use an official Python runtime as a parent image
  FROM python:3.9-slim

  # Install Java
  RUN apt-get update && \
      apt-get install -y openjdk-11-jdk && \
      apt-get clean;

  # Set JAVA_HOME environment variable
  ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

  # Install Python dependencies
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  # Copy the rest of your application code
  COPY . .

  # Command to run your application
  CMD ["python", "app.py"]