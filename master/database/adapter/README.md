# Running the Adapter with venv and Docker

This guide will walk you through the process of initializing a Python 3 server with Pip's virtual environment (venv) and Docker.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3: [Install Python 3](https://www.python.org/downloads/)
- Docker: [Install Docker](https://docs.docker.com/get-docker/)

## PostgreSQL database setup
   This server requires PostgreSQL database in order to work correctly.

   NOTE: This is why using the docker-compose is recommended at the parent directory.

## Setup with Pip Virtual Environment

1. **Create a Python Virtual Environment:**
   Run the following commands in your terminal to create a Python virtual environment:
   ```bash
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

5. **Stop the Server**
   Press `Control + C` and run the following command to deactive the venv:
   ```bash
   deactivate
   ```

## Setup with Docker

1. **Build Docker image:**
   Run the following command to build the Docker image:
   ```
   docker build -t adapter .
   ```

2. **Run the Server with Docker:**
   Run the following command to build the Docker image:
   ```
   docker run -e DB_USERNAME=username \
              -e DB_PASSWORD=password \
              -e DB_NAME=databasename \
              -e DB_HOSTNAME=localhost \
              -p 8080:8080\
              adapter
   ```
   Change the DB_* variables according to your database. 

   The `-d` flag runs the services in detached mode, meaning they run in the background.




   
