# Initializing Python 3 and Pip Virtual Environment Project and with Dockerfile

This guide will walk you through the process of initializing a Python 3 project with Pip's virtual environment (venv).

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3: [Install Python 3](https://www.python.org/downloads/)
- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## Redis database setup
   This server needs Redis dabase in order to work correctly. Please refer to README in Redis directory. 

## Setup

1. **Initialize proto**
   Run the following command in your terminal on root directory:
   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=server/node --grpc_python_out=server/node protos/chat.proto
   ```

2. **Create a Python Virtual Environment:**
   Run the following commands in your terminal to create a Python virtual environment:
   ```bash
   cd worker/node/
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   Activate the virtual environment using the appropriate command for your operating system:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies:**
   Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Server**
   Run the server using Python3:
   ```bash
   python3 ./main.py
   ```

## Docker Setup

1. **Build Docker Image:**
   Run the following command to build the Docker image:
   ```bash
   docker build -t worker .
   ```

2. **Run Docker Container:**
   Execute the following command to run the Docker container:
   ```bash
   docker run -p 50052:50052 worker
   ```

   The master server uses port 50052. 

6. **Access the Application:**
   Once the container is running, you can access your application by typing
   ```bash
   docker ps -a
   ```

7. **Stop the Application:**
   Stop Docker containers by typing:
   ```bash
   docker stop <container_name>
   ```

## Additional Notes

- Don't forget to deactivate the virtual environment once you're done working on your project:
   ```bash
   deactivate
   ```

## Troubleshooting

