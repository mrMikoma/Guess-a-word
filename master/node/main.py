from concurrent import futures
import time
import grpc
import os
import master_pb2_grpc
import master_pb2
import sys_master_pb2_grpc
import sys_master_pb2
from dotenv import load_dotenv
import requests

# Global variables
MAX_WORKERS = 10
PORT = 50051
WORKER_LOBBIES = {} # dictionary {worker:[lobby_id]} to track how many lobbies each worker has
DB_ADDRESS="http://0.0.0.0:8080"

load_dotenv()

def MakeNewLobby(user_id: str):
    
    worker_list = requests.get(url=DB_ADDRESS+"/workers/")
    
    return

class MasterServiceServicer(master_pb2_grpc.MasterServiceServicer, sys_master_pb2_grpc.MasterServiceServicer): 
    
    def CreateNewLobby(self, request, context):
        ip, lobby_id = -1
        
        return master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
    
    def JoinLobby(self, request, context):
        try:
            ip, lobby_id = -1
            lobby = requests.get(url=DB_ADDRESS+"/lobbies/"+request.lobby_id).json()
            ip = lobby["ip_address"]
            return master_pb2.LobbyInfo(ip=ip, lobby_id=request.lobby_id)
        except Exception as e:
            print("Error: ", e)
            return master_pb2.LobbyInfo(ip=-1, lobby_id=-1)
    
    def UpdateLobby(self, request, context):
        status, desc = ""
        lobby = requests.get(url=DB_ADDRESS+"/lobbies/"+request.lobby_id).json()
        return sys_master_pb2.Status(status=status, desc=desc)

def initialize():
    # add every worker to dict and set their lobby count to 0
    worker_list = list(requests.get(DB_ADDRESS+"/workers/").content)
    for worker in worker_list:
        WORKER_LOBBIES[worker]=0
        
    return
    
def serve():
    initialize()
    
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    master_pb2_grpc.add_MasterServiceServicer_to_server(MasterServiceServicer(), server)
    sys_master_pb2_grpc.add_MasterServiceServicer_to_server(MasterServiceServicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    try:
        while True:
            print(f"Master is running on port {PORT}...")
            time.sleep(86400)  # One day
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()