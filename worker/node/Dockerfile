# Using python 3.12 as base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /node

# Copy the current directory contents into the container at /node
COPY . /node/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the worker gRPC server
EXPOSE 50052 

# Run main.py when the container launches
CMD ["python3", "./main.py"]