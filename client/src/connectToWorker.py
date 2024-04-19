import worker_pb2
import worker_pb2_grpc
import src.connectRPC as connectRPC
import src.chatChannel as chatChannel

COLOR_GREEN = "\033[92m"  
COLOR_YELLOW = "\033[93m"  
COLOR_RED = "\033[91m"  
COLOR_BLUE = '\033[34m'
COLOR_RESET = "\033[0m"  # Reset color to default

def sendLobbyInfoToWorker(lobby_id, USER_ID, client):
    # Create a channel stub
    try:
        client = client
        stub = worker_pb2_grpc.WorkerServiceStub(client)
    except Exception as e:
        print(COLOR_RED + "Error: connecting to server" + COLOR_RESET)
        print(e)
        return 1
    
    # Send the message to the server, specifying if creating a new lobby or joining an existing.
    request = worker_pb2.LobbyInfo(
        lobby_id=lobby_id,
        user_id=USER_ID,
    )
    
    # Handle the response
    response = stub.JoinLobby(request)
    if response:
        return response.player_role
    else:
        print(COLOR_RED + "Error: ", response + COLOR_RESET)
        return 1
    
def getStatus():
    try:
        client = connectRPC.getClient()
        stub = worker_pb2_grpc.WorkerServiceStub(client)
    except Exception as e:
        print(COLOR_RED + "Error: connecting to server" + COLOR_RESET)
        print(e)
        return 1
    
    # Send the message to the server, specifying if creating a new lobby or joining an existing.
    request = worker_pb2.Status(
        success=True,
        message="Client works",
    )
    
    # Handle the response
    response = stub.GetStatus(request)
    if response.success:
        #print("Received a response") # Debug

        print(response)
        return response
    else:
        print(COLOR_RED + "Error: " + response.message + COLOR_RESET)
        return 1
    
def startGame(user_id, lobby_id):
    # print("Starting game.") # Debug.
    client = connectRPC.getClient()
    stub = worker_pb2_grpc.WorkerServiceStub(client)
    
    chatChannel.connectToChatChannel(user_id, lobby_id, stub)
    return 0

def startGameAsAdmin(user_id, lobby_id):
    try:
        client = connectRPC.getClient()
        stub = worker_pb2_grpc.WorkerServiceStub(client)
    except Exception as e:
        print(COLOR_RED + "Error: connecting to server" + COLOR_RESET)
        print(e)
        return 1
    
    # Send the message to the server, specifying if creating a new lobby or joining an existing.
    request = worker_pb2.GameInfo(
        start=True,
    )
    
    # Handle the response
    response = stub.StartGame(request)
    if response:
        #print("Received a response") # Debug
        print(COLOR_BLUE + "Your secret word is: " + response.word + COLOR_RESET)
        chatChannel.connectToChatChannel(user_id, lobby_id, stub)
    else:
        print(COLOR_RED + "Error: " + response.message + COLOR_RESET)
        return 1

