# Initializing Python 3 and Pip Virtual Environment Project.

This guide will walk you through the process of initializing a Python 3 project with Pip's virtual environment (venv) and running it.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
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

4. **Run client:**
   Run the client with 
   ```bash
   python3 ./main.py
   ```



## Additional Notes

- Ensure that your Python dependencies are listed in the `requirements.txt` file.
- Don't forget to deactivate the virtual environment once you're done working on your project:
   ```bash
   deactivate
   ```
