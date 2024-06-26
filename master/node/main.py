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
DB_HOST = os.getenv('DB_HOST')  # get the database host from the environment variables DO NOT USE LOCALHOST
DB_ADDRESS="http://" + DB_HOST + ":8080" 

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
                print(f"Worker '{ip}' is fine.")
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
                print(f"Worker '{worker_ip}' is already on the list.")
                continue
            else:
                WORKER_LOBBIES[worker_ip]=0
                print(f"Added new worker '{worker_ip}' to the list!")
    except Exception as e:
        print("Error Adding new workers:",e)
    finally:
        return
class MasterServiceServicer(master_pb2_grpc.MasterServiceServicer, sys_master_pb2_grpc.SysMasterServiceServicer): 
    

    def CreateNewLobby(self, request, context):
        print(f"Creating a lobby for '{request.user_id}'")
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
            
            print(f"Parameters: lobby id: '"+str(lobby_id)+"' user_id: '"+request.user_id+"' "+"ip:"+ip) #DEBUG
            request = sys_worker_pb2.LobbyParams(lobby_id=lobby_id, user_id=str(user_id),)
            response = workerStub.NewLobby(request)
            channel.close()
            print("channel closed") #DEBUG
            
            if response.status == "OK":
                print("Worker is ok, finalizing lobby...")
                request = requests.put(url=DB_ADDRESS+"/lobbies/"+str(lobby_id), params={"lobby_id": lobby_id, "ip_address": ip, "status": "available"})
                WORKER_LOBBIES[ip] += 1
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
        print(f"Updating info for lobby '{request.lobby_id}'")
        status = ""
        desc = ""
        try:
            lobby_id = request.lobby_id
            new_status = request.new_status
            oldLobby = requests.get(url=DB_ADDRESS+"/lobbies/"+lobby_id).json()
            worker_id = oldLobby["ip_address"] # Could also be pulled from context?
            
            # take appropriate action with the new status
            if new_status == "closed":
                print("Closing the lobby...")
                response = requests.delete(url=DB_ADDRESS+"/lobbies/"+str(lobby_id))
                WORKER_LOBBIES[worker_id] -= 1
            else:
                print(f"updating lobby with new status '{new_status}'...")
                response = requests.put(url=DB_ADDRESS+"/lobbies/"+str(lobby_id), params={"lobby_id": lobby_id, "ip_address": worker_id, "status": new_status})
            
            if response.status_code == 200:
                status = "OK"
            else:
                status = "ERROR"
                desc = response.text
        except Exception as e:
            print("Error while Updating lobby: ", e)
        finally:
            print(f"returning worker with {status}: {desc}")
            return sys_master_pb2.Status(status=status, desc=desc)

    def DeleteLobby(self, request, context):
        success = False
        message = ""
        lobby_id = int(request.lobby_id)
        user_id = str(request.user_id)
        
        # find worker ip
        lobby = requests.get(url=DB_ADDRESS+"/lobbies/"+str(lobby_id)).json()
        ip = lobby["ip_address"]
        
        # tell worker to kill lobby
        try:
            with grpc.insecure_channel(ip + ":50052") as channel:
                print("channel opened in '" + ip + ":50052'")
                workerStub = sys_worker_pb2_grpc.SysWorkerServiceStub(channel)
                
                print(f"Parameters for KillLobby: lobby id: '{lobby_id}' user_id: '{user_id}' ip: {ip}") #DEBUG
                request = sys_worker_pb2.LobbyParams(lobby_id=lobby_id, user_id=user_id,)
                response = workerStub.workerStub(request)
                channel.close()
            print("channel closed") #DEBUG
        
        # if worker no answer, continue on deleting
        except Exception as e:
            print("Error conneting to worker :",e)
            pass
    
        # if workers says no, then don't remove and pass message along
        if response.status == "Fail":
            message = response.desc
            return master_pb2.StatusForClient(success=success, message=message)
        # If OK, got error or no answer, delete the lobby
        else:  
            try:
                WORKER_LOBBIES[ip] -=1
                dbRequest = requests.delete(url=DB_ADDRESS+"/lobbies/"+str(lobby_id)) # don't care what db says, its deleted
                success = True
                return master_pb2.StatusForClient(success=success, message=message)
            except Exception as e:
                print("Error deleting lobby:",e)
                return master_pb2.StatusForClient(success=success, message=e)
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