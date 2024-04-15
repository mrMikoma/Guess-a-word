# Initializing Python 3 and Pip Virtual Environment Project with Dockerfile

This guide will walk you through the process of initializing a Python 3 project with Pip's virtual environment (venv) and running it using Docker.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Python 3: [Install Python 3](https://www.python.org/downloads/)

## Setup

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

4. **Build Docker Image:**
   Run the following command to build the Docker image:
   ```bash
   docker build -t client .
   ```

5. **Run Docker Container:**
   Execute the following command to run the Docker container:
   ```bash
   docker run -p 4000:80 client
   ```

   This command maps port 4000 of the host to port 80 of the Docker container. Adjust the port mapping as needed.

6. **Access the Application:**
   Once the container is running, you can access your application by ...docker

7. **Stop the Application:**
   You can see the Docker containers by typing:
   ```bash
   docker ps -a
   ```

   and stop Docker containers by typing:
   ```bash
   docker stop <container_name>
   ```

## Additional Notes

- Ensure that your Python dependencies are listed in the `requirements.txt` file.
- Customize the `Dockerfile` as needed for your project requirements.
- Don't forget to deactivate the virtual environment once you're done working on your project:
   ```bash
   deactivate
   ```

## Troubleshooting

- Check logs using `docker logs <container_name>` command to troubleshoot any errors or issues with your container.
