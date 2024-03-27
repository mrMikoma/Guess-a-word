# Using python 3.12.2-bookworm as base image (change according to used Python version)
FROM python:3.12.2-bookworm

# Set the working directory in the container
WORKDIR /worker

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /worker/

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/worker/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /worker/

# Create a non-root user
RUN useradd -m nonrootuser
USER nonrootuser

# Run main.py when the container launches
CMD ["python3", "main.py"]