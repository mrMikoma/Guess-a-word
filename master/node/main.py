from concurrent import futures
import time
import grpc
import os
from dotenv import load_dotenv
import requests

import master_pb2_grpc
import master_pb2
import sys_master_pb2
import sys_master_pb2_grpc
import sys_worker_pb2
import sys_worker_pb2_grpc

# Global variables
MAX_WORKERS = 10
PORT = 50051
DB_ADDRESS="0.0.0.0:8080"

load_dotenv()

def MakeNewLobby():

    worker_list = requests.get(url=DB_ADDRESS+"/workers/")

    
    return

def JoinExistingLobby():
    # TODO
    print("joined a new lobby!")
    return
class MasterServiceServicer(master_pb2_grpc.MasterServiceServicer, sys_master_pb2_grpc.MasterServiceServicer): 
    
    def SendLobbyInfo(self, request, context):
        ip=-1
        lobby_id=-1
        if (request.lobby_choice == 1):
            ip, lobby_id = self.JoinExistingLobby()
        elif(request.lobby_choise == 2):
            ip, lobby_id = self.MakeNewLobby()
        else:
            # wrong request, return default values 
            pass 
        return master_pb2.NewLobbyInfo(ip=ip, lobby_id=lobby_id)
    
    def UpdateLobby(self, request, context):
        return super().UpdateLobby(request, context)

def initialize():
    # TODO
    # clear up worker
    return
    
def serve():
    initialize()
    
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    master_pb2_grpc.add_MasterServiceServicer_to_server(MasterServiceServicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    try:
        while True:
            print(f"Master
                  is running on port {PORT}...")
            time.sleep(86400)  # One day
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()