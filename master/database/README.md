# PostgreSQL and Python 3 adapter setup

# Setting up Environment Variables and Running Docker Compose

This guide will walk you through the process of setting up environment variables using a `.env` file and running Docker Compose to deploy your database and adapter.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Create a `.env` File:**
   Create a file named `.env` in the database (this root) directory. This file will hold your environment variables. Look for `.env.template` to see example.

   Change the values to not use default variables.

2. **Build and Run Docker Compose:**
   Run the following command to build and run your Docker Compose services:
   ```
   docker-compose up -d
   ```

   The `-d` flag runs the services in detached mode, meaning they run in the background.

3. **Verify Deployment:**
   Once the services are up and running, you can verify the deployment by accessing your application through the specified host and port.

   You can check that the service is running using:
   ```
   docker-compose ps
   ```

## Additional Notes

- Don't use default credentials in .env file.

## Troubleshooting

- Check logs using `docker-compose logs` command to troubleshoot any errors or issues with your containers.
