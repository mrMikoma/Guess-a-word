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
DB_HOST = os.getenv('DB_HOST', "database-adapter-1")
DB_ADDRESS="http://" + DB_HOST + ":8080" # if running in docker use address of "database-adapter-1", else use "localhost:8080"

load_dotenv()
def DeleteWorker(ip):
    response = requests.delete(url=DB_ADDRESS+"/workers/"+str(ip)).json()
    print("status from deleting the worker:",response["status"])
    WORKER_LOBBIES.pop(ip)
    return response["status"]

def CheckWorker(ip):
    try:
        print(f"Checking if worker '{ip}' is alive")
        with grpc.insecure_channel(ip + ":50052") as channel:
            workerStub = sys_worker_pb2_grpc.SysWorkerServiceStub(channel)
            request = sys_worker_pb2.Null()
            response = workerStub.CheckStatus(request)
            if response.status == "OK":
                print(f"Worker '{ip}' is fine")
                return "OK"
            else:
                print(f"Worker '{ip}' is not fine, deleting from list...")
                DeleteWorker(ip=ip)
                return "ERROR"
    except Exception as e:
        print("Error while checking on worker:", e)
        print(f"Deleting worker '{ip}' from list...")
        DeleteWorker(ip=ip)
        return "ERROR"
        

def UpdateWorkers():
    try:
        worker_list = list(requests.get(DB_ADDRESS+"/workers/").json())
        for worker in worker_list:
            worker_ip = worker["ip_address"]
            if CheckWorker(ip=worker_ip) != "OK":
                # Worker was unavailable and was deleted
                continue
            if worker_ip in WORKER_LOBBIES:
                continue
            else:
                WORKER_LOBBIES[worker_ip]=0
                print(f"added new worker '{worker_ip}' to the list!")
    except Exception as e:
        print("Error Adding new workers:",e)
    finally:
        return
class MasterServiceServicer(master_pb2_grpc.MasterServiceServicer, sys_master_pb2_grpc.SysMasterServiceServicer): 
    

    def CreateNewLobby(self, request, context):
        ip = ""
        lobby_id = -1
        try: 
            lobby_id = int(requests.post(url=DB_ADDRESS+"/lobbies/").json()["lobby_id"])
            user_id = str(request.user_id)
            # Update workers before using them
            UpdateWorkers()
            # Find the worker with the smallest lobby_count
            ip = min(WORKER_LOBBIES, key=lambda x: WORKER_LOBBIES[x])
            
            
            channel = grpc.insecure_channel(ip + ":50052")
            print("channel opened in '" + ip + ":50052'")
            workerStub = sys_worker_pb2_grpc.SysWorkerServiceStub(channel)
            
            print(f"lobby id: '"+str(lobby_id)+"' user_id: '"+request.user_id+"'") #DEBUG
            request = sys_worker_pb2.LobbyParams(lobby_id=lobby_id, user_id=str(user_id),)
            
            print("ip:"+ip) #DEBUG
            response = workerStub.NewLobby(request)
            channel.close()
            print("channel closed") #DEBUG
            if response.status == "OK":
                request = requests.put(url=DB_ADDRESS+"/lobbies/"+str(lobby_id), params={"lobby_id": lobby_id, "ip_address": ip, "status": "available"})
                # print("check 2") #DEBUG
                return master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
            else:
                print("Error with worker:", response.status, response.desc)
                master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
        except Exception as e:
            print("Error while creating a lobby: ", e)
            return master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
    
    def JoinLobby(self, request, context):
        try:
            ip = ""
            lobby_id = request.lobby_id
            lobby = requests.get(url=DB_ADDRESS+"/lobbies/"+str(request.lobby_id)).json()
            ip = lobby["ip_address"]
            return master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
        except Exception as e:
            print("Error while Joining a lobby: ", e)
            return master_pb2.LobbyInfo(ip=ip, lobby_id=lobby_id)
    
    def UpdateLobby(self, request, context):
        status = ""
        desc = ""
        try:
            oldLobby = requests.get(url=DB_ADDRESS+"/lobbies/"+request.lobby_id).json()
            response = requests.put(url=DB_ADDRESS+"/lobbies/"+request.lobby_id, params={"lobby_id": request.lobby_id, "ip_address": oldLobby["ip_address"], "status": request.new_status})
            if response.status_code == 200:
                status = "OK"
            else:
                status = "ERROR"
                desc = response.text
        except Exception as e:
            print("Error while Updating lobby: ", e)
        finally:
            return sys_master_pb2.Status(status=status, desc=desc)

def initialize():
    # add every worker to dict and set their lobby count to 0
    UpdateWorkers()
    
def serve():
    initialize()
    
    # Initialize the server
    print("Using database address: " + DB_ADDRESS) # debug
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