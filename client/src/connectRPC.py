import grpc
from src.connectToMaster import *
from src.connectToWorker import *

COLOR_GREEN = "\033[92m"  
COLOR_YELLOW = "\033[93m"  
COLOR_RED = "\033[91m"  
COLOR_BLUE = '\033[34m'
COLOR_RESET = "\033[0m"  # Reset color to default

# CONSTANTS
CLIENT = None

def connectMasterNode(choice, USER_ID):
    # Asks for the server IP
    master_ip = input(COLOR_YELLOW + "Enter the server IP: " + COLOR_RESET)
    
    # Create a connection to the server if it does not exist
    global CLIENT
    if CLIENT is None:
        try:
            CLIENT = grpc.insecure_channel(master_ip + ':50051')
            print(COLOR_GREEN + "\nConnection established" + COLOR_RESET)

            # Ask for existing lobby or to create a new one:
            if choice == 1:
                response = sendInformationToMaster(1, USER_ID, CLIENT)
            elif choice == 2:
                response = sendInformationToMaster(2, USER_ID, CLIENT)

            disconnectServer()
            return response
        except Exception as e:
            print(COLOR_RED + "\nError: something went wrong when communicating with server. connectRPC.py" + COLOR_RESET)
            print(e)
            return 1
    else:
        print(COLOR_RED + "\nConnection already exists" + COLOR_RESET)
        return 1
    

def connectWorkerNode(lobby_info, USER_ID):
    
    # Create a connection to the server if it does not exist
    global CLIENT
    if CLIENT is None:
        try:
            print("lobby_info:", lobby_info)
            CLIENT = grpc.insecure_channel(lobby_info[0] + ':50052')
            print(COLOR_GREEN + "\nConnection established" + COLOR_RESET)

            response = sendLobbyInfoToWorker(lobby_info[1], USER_ID, CLIENT)

            return response
        except Exception as e:
            print(COLOR_RED + "\nError: something went wrong when communicating with server. connectRPC.py" + COLOR_RESET)
            print(e)
            return 1
    else:
        print(COLOR_RED + "\nConnection already exists" + COLOR_RESET)
        return 1
    

def getClient():
    if CLIENT is not None:
        return CLIENT
    else:
        print(COLOR_RED + "\nNo connection to server" + COLOR_RESET)
        return 1

def disconnectServer():
    # Close the connection to the server

    ## HERE SHOULD BE SOME COMMUNICATION FOR DISCONNECTING FROM THE SERVER.

    global CLIENT
    if CLIENT is not None:
        CLIENT.close()
        CLIENT = None
        print(COLOR_YELLOW + "\nDisconnected from server" + COLOR_RESET)
        return 0
    else:
        print(COLOR_RED + "\nNo connection to close" + COLOR_RESET)
        return 1
   