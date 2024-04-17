import worker_pb2
import worker_pb2_grpc
import src.connectRPC as connectRPC
import src.chatChannel as chatChannel

def sendLobbyInfoToWorker(lobby_id, USER_ID, client):
    # Create a channel stub
    try:
        client = client
        stub = worker_pb2_grpc.WorkerServiceStub(client)
    except Exception as e:
        print("Error: connecting to server")
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
        print("Received a response") # Debug

        print(response.player_role)

        return response.player_role
    else:
        print("Error: " + response)
        return 1
    
def getStatus():

    try:
        client = connectRPC.getClient()
        stub = worker_pb2_grpc.WorkerServiceStub(client)
    except Exception as e:
        print("Error: connecting to server")
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
        print("Received a response") # Debug

        print(response)
        # HERE response should be parsed and new IP and lobby ID returned to the connectRPC

        return response
    else:
        print("Error: " + response.message)
        return 1
    
def startGame(user_id, lobby_id):
    client = connectRPC.getClient()
    stub = worker_pb2_grpc.WorkerServiceStub(client)
    
    chatChannel.connectToChatChannel(user_id, lobby_id, stub)
    return 0