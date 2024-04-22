# Initializing Python 3 and Pip Virtual Environment Project and with Dockerfile

This guide will walk you through the process of initializing a Python 3 project with Pip's virtual environment (venv) and running it using Docker.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Python 3: [Install Python 3](https://www.python.org/downloads/)

## venv Setup

1. **Create a Python Virtual Environment:**
   Run the following command in your terminal to create a Python virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment:**
   Activate the virtual environment using the appropriate command for your operating system:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Dependencies:**
   Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Docker Setup

1. **Build Docker Image:**
   Run the following command to build the Docker image:
   ```bash
   docker build -t master .
   ```

2. **Run Docker Container:**
   Execute the following command to run the Docker container:
   ```bash
   docker run --network database_private-db -p 50051:50051 master
   ```

   The master server uses port 50051. 

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

- Check logs using `docker logs <container_name>` command to troubleshoot any errors or issues with your container.
