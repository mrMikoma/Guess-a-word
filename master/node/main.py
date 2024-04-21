from concurrent import futures
import time
import grpc
import os
import master_pb2_grpc
import master_pb2
import sys_master_pb2_grpc
import sys_master_pb2
import sys_worker_pb2_grpc
import sys_worker_pb2
from dotenv import load_dotenv
import requests

# Global variables
MAX_WORKERS = 10
PORT = 50051
WORKER_LOBBIES = {} # dictionary {worker_ip:lobby_count} to track how many lobbies each worker has
DB_ADDRESS="http://localhost:8080"

load_dotenv()

class MasterServiceServicer(master_pb2_grpc.MasterServiceServicer, sys_master_pb2_grpc.SysMasterServiceServicer): 
    
    def CreateNewLobby(self, request, context):
        ip, lobby_id = -1
        try: 
            lobby_id = requests.post(url=DB_ADDRESS+"/lobbies/").json()["lobby_id"]
            
            # Find the worker with the smallest lobby_count
            ip = min(WORKER_LOBBIES, key=lambda x: WORKER_LOBBIES[x])
            
            workerStub = sys_worker_pb2_grpc.WorkerServiceStub()
            response = workerStub.NewLobby(sys_master_pb2.LobbyInfo(lobby_id=lobby_id, user_id=request.user_id))
            if response.status == "OK":
                request = requests.put(url=DB_ADDRESS+"/lobbies/"+lobby_id, data={"lobby_id": lobby_id, "ip_address": ip, "status": "available"})
                return master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
            else:
                print("Error with worker:", response.status, response.desc)
                return master_pb2.LobbyInfo(ip=-1, lobby_id=-1)
        except Exception as e:
            print("Error: ", e)
            return master_pb2.LobbyInfo(ip=-1, lobby_id=-1)
    
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
        try:
            oldLobby = requests.get(url=DB_ADDRESS+"/lobbies/"+request.lobby_id).json()
            response = requests.put(url=DB_ADDRESS+"/lobbies/"+request.lobby_id, data={"lobby_id": request.lobby_id, "ip_address": oldLobby["ip_address"], "status": request.new_status})
            if response.status_code == 200:
                status = "OK"
            else:
                status = "ERROR"
                desc = response.text
        except Exception as e:
            print("Error: ", e)
        finally:
            return sys_master_pb2.Status(status=status, desc=desc)

def initialize():
    # add every worker to dict and set their lobby count to 0
    try:
        worker_list = list(requests.get(DB_ADDRESS+"/workers/").content)
        for worker in worker_list:
            WORKER_LOBBIES[worker]=0
    except Exception as e:
        print("Error initializing workers:",e)
    finally:
        return
    
def serve():
    initialize()
    
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    master_pb2_grpc.add_MasterServiceServicer_to_server(MasterServiceServicer(), server)
    sys_master_pb2_grpc.add_SysMasterServiceServicer_to_server(MasterServiceServicer(), server)
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