import grpc
from src.connectToMaster import *
from src.connectToWorker import *

# CONSTANTS
CLIENT = None

def connectMasterNode(choice, USER_ID):
    # Asks for the server IP
    master_ip = input("Enter the server IP: ")
    
    # Create a connection to the server if it does not exist
    global CLIENT
    if CLIENT is None:
        try:
            CLIENT = grpc.insecure_channel(master_ip + ':50051')
            print("\nConnection established")

            # Ask for existing lobby or to create a new one:
            if choice == 1:
                response = sendInformationToMaster(1, USER_ID, CLIENT)
            elif choice == 2:
                response = sendInformationToMaster(2, USER_ID, CLIENT)

            disconnectServer()
            return response
        except Exception as e:
            print("\nError: Could not connect to server")
            print(e)
            return 1
    else:
        print("\nConnection already exists")
        return 1
    

def connectWorkerNode(lobby_info, USER_ID):
    
    # Create a connection to the server if it does not exist
    global CLIENT
    if CLIENT is None:
        try:
            CLIENT = grpc.insecure_channel(lobby_info[0] + lobby_info[1])
            print("\nConnection established")

            response = sendLobbyInfoToWorker(lobby_info[1], USER_ID, CLIENT)
            # HERE should be something to join the lobby.

            return 0
        except Exception as e:
            print("\nError: Could not connect to server")
            print(e)
            return 1
    else:
        print("\nConnection already exists")
        return 1
    

def getClient():
    if CLIENT is not None:
        return CLIENT
    else:
        print("\nNo connection to server")
        return 1

def disconnectServer():
    # Close the connection to the server
    global CLIENT
    if CLIENT is not None:
        CLIENT.close()
        CLIENT = None
        print("\nDisconnected from server")
        return 0
    else:
        print("\nNo connection to close")
        return 1
   