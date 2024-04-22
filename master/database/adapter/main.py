import uvicorn 
from fastapi import FastAPI, HTTPException
import psycopg2
import random
import os

# Database Configuration
username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
hostname = "database"                           # "localhost" if running locally, "database" if running in Docker
port = "5432"                                   # by default "5432"
databasename = os.getenv("POSTGRES_DB")

# Construct DATABASE_URL
DATABASE_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{databasename}"
#DATABASE_URL = "postgresql://username:password@localhost:5432/databasename"

app = FastAPI() # Create FastAPI instance

"""
### Postgres Database Adapter ###

This adapter provides the following routes for lobby management:
- POST /lobbies/                - Create a new lobby
- GET /lobbies/{lobby_id}       - Get a lobby by ID
- PUT /lobbies/{lobby_id}       - Update a lobby by ID
- DELETE /lobbies/{lobby_id}    - Delete a lobby by ID

The adapter provides the following routes for worker management:
- POST /workers/                - Create a new worker
- GET /workers/                 - Get all workers
- PUT /workers/{ip_address}     - Update a worker by ip_address
- DELETE /workers/{ip_address}  - Delete a worker by ip_address

Database Schema:
- lobbies
    - lobby_id (SERIAL PRIMARY KEY)             # Unique 5-digit lobby ID
    - ip_address (VARCHAR)                      # IP address of the lobby
    - status (VARCHAR, default 'creating')      # Allowed statuses: creating, available, full, closed
- workers
    - ip_address (PRIMARY KEY, VARCHAR, UNIQUE) # IP address of the worker
    - status (VARCHAR, default 'available')     # Allowed statuses: available, error, offline
"""

########################
### HELPER FUNCTIONS ###
########################

# Helper function for database connections
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        raise HTTPException(status_code=500, detail="Database unavailable")
    
# Helper function to create tables
def create_tables():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Create workers table if it doesn't exist
            cur.execute("""CREATE TABLE IF NOT EXISTS workers (ip_address VARCHAR(48) PRIMARY KEY UNIQUE, 
                        status VARCHAR(48) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'error', 'offline')))""")
            
            # Create lobbies table if it doesn't exist
            cur.execute("""CREATE TABLE IF NOT EXISTS lobbies (lobby_id SERIAL PRIMARY KEY, ip_address VARCHAR(48), 
                        status VARCHAR(48) NOT NULL DEFAULT 'creating' CHECK (status IN ('creating', 'available', 'full', 'closed')))""")
            
            # Commit changes
            conn.commit()
            
# Helper function to generate a random lobby ID
def generate_lobby_id():
    return random.randint(10000, 99999)

####################
### LOBBY ROUTES ###
####################

# Route to create a new lobby
@app.post("/lobbies/")
def create_lobby():
    # Retry parameters
    MAX_RETRIES = 5  
    RETRY_DELAY = 0.1  

    with get_db_connection() as conn:
        with conn.cursor() as cur: 
            for _ in range(MAX_RETRIES):
                lobby_id = generate_lobby_id()  # Generate a random lobby ID

                # Check if lobby ID already exists
                cur.execute("SELECT EXISTS(SELECT 1 FROM lobbies WHERE lobby_id = %s)", (lobby_id,))
                if cur.fetchone()[0]: 
                    continue

                # Insert with ip and status
                try:
                    # Insert lobby with status 'creating'
                    cur.execute(
                        "INSERT INTO lobbies (lobby_id, ip_address, status) VALUES (%s, NULL, %s) RETURNING lobby_id",
                        (lobby_id, "creating") 
                    )
                    conn.commit()
                    return {"lobby_id": lobby_id}
                except psycopg2.errors.UniqueViolation:
                    time.sleep(RETRY_DELAY)
                    continue  # Try again

    raise HTTPException(status_code=500, detail="Failed to create lobby after multiple attempts")  

    # If we get here, all retries failed
    raise HTTPException(status_code=500, detail="Failed to create lobby after multiple attempts")

# Route to get existing lobby by ID
@app.get("/lobbies/{lobby_id}")
def get_lobby(lobby_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Get lobby by ID
            cur.execute("SELECT * FROM lobbies WHERE lobby_id = %s", (lobby_id,))
            lobby = cur.fetchone()
            
            # If lobby exists, return it
            if lobby:
                return {"lobby_id": lobby_id, "ip_address": lobby[1], "status": lobby[2]}
            else:
                raise HTTPException(status_code=404, detail="Lobby not found")

# Route to update a lobby by ID
@app.put("/lobbies/{lobby_id}")
def update_lobby(lobby_id: int, ip_address: str, status: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if lobby exists
            cur.execute("SELECT EXISTS(SELECT 1 FROM lobbies WHERE lobby_id = %s)", (lobby_id,))
            if not cur.fetchone()[0]:
                raise HTTPException(status_code=404, detail="Lobby not found")
            
            # Update lobby with new IP and status
            cur.execute("UPDATE lobbies SET ip_address = %s, status = %s WHERE lobby_id = %s", (ip_address, status, lobby_id))
            conn.commit()
            return {"status": "success"}

# Route to delete a lobby by ID
@app.delete("/lobbies/{lobby_id}")
def delete_lobby(lobby_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if lobby exists
            cur.execute("SELECT EXISTS(SELECT 1 FROM lobbies WHERE lobby_id = %s)", (lobby_id,))
            if not cur.fetchone()[0]:
                raise HTTPException(status_code=404, detail="Lobby not found")
            
            # Delete lobby by ID
            cur.execute("DELETE FROM lobbies WHERE lobby_id = %s", (lobby_id,))
            conn.commit()
            return {"status": "success"}

#####################
### WORKER ROUTES ###
#####################

# Route to create a new worker
@app.post("/workers/")
def create_worker(ip_address: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if worker already exists
            cur.execute("SELECT EXISTS(SELECT 1 FROM workers WHERE ip_address = %s)", (ip_address,))
            if cur.fetchone()[0]:
                raise HTTPException(status_code=400, detail="Worker already exists")
            
            # Insert worker with status 'available'
            cur.execute("INSERT INTO workers (ip_address, status) VALUES (%s, 'available')", (ip_address,))
            conn.commit()
            return {"status": "success"}
        
# Route to get all workers
@app.get("/workers/")
def get_workers():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Get all workers
            cur.execute("SELECT * FROM workers")
            workers = cur.fetchall()
            return [{"ip_address": worker[0], "status": worker[1]} for worker in workers]
        
# Route to update a worker by ip_address
@app.put("/workers/{ip_address}")
def update_worker(ip_address: str, status: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if worker exists
            cur.execute("SELECT EXISTS(SELECT 1 FROM workers WHERE ip_address = %s)", (ip_address,))
            if not cur.fetchone()[0]:
                raise HTTPException(status_code=404, detail="Worker not found")
            
            # Update worker with new status
            cur.execute("UPDATE workers SET status = %s WHERE ip_address = %s", (status, ip_address))
            conn.commit()
            return {"status": "success"}
        
# Route to delete a worker by ip_address
@app.delete("/workers/{ip_address}")
def delete_worker(ip_address: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if worker exists
            cur.execute("SELECT EXISTS(SELECT 1 FROM workers WHERE ip_address = %s)", (ip_address,))
            if not cur.fetchone()[0]:
                raise HTTPException(status_code=404, detail="Worker not found")
            
            # Delete worker by ip_address
            cur.execute("DELETE FROM workers WHERE ip_address = %s", (ip_address,))
            conn.commit()
            return {"status": "success"}

### MAIN FUNCTION ###
# Start the server
if __name__ == "__main__":
    create_tables() # Create tables if they don't exist
    uvicorn.run(app, host="0.0.0.0", port=8080) # Start the server
