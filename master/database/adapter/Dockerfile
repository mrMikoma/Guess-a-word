# Using python 3.12 as base image (change according to used Python version)
FROM python:3.12

# Set the working directory in the container
WORKDIR /adapter

# Copy the current directory contents into the container at /adapter
COPY . /adapter/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run main.py when the container launches
CMD ["python3", "./main.py"]