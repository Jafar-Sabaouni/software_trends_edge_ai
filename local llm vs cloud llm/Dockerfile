# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Grant execution permissions
RUN chmod +x entrypoint.sh
RUN chmod +x scripts/benchmark.py
RUN chmod +x scripts/analyse.py

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Set the default command to run the benchmark script
CMD ["python", "-u", "scripts/benchmark.py"]

