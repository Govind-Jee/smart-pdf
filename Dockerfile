# # Use a specific linux/amd64 Python image as required [cite: 56]
# FROM --platform=linux/amd64 python:3.9-slim

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the file listing our dependencies
# COPY requirements.txt .

# # Install those dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all your code into the container
# COPY . .

# # The command that runs when the container starts
# CMD ["python", "main.py"]
# Dockerfile for Round 1B
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# IMPORTANT: Copy the downloaded model into the container
COPY sbert-model/ ./sbert-model/

COPY . .

# Change the command to run the Round 1B script
CMD ["python", "main_1b.py"]