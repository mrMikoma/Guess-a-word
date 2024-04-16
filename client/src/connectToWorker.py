import worker_pb2
import worker_pb2_grpc

def sendLobbyInfoToWorker(lobby_choice, USER_ID, client):
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
        lobby_choice=lobby_choice,
        user_id=USER_ID,
    )
    
    # Handle the response
    response = stub.JoinLobby(request)
    if response.success:
        print("Received a response") # Debug

        print(response)
        # HERE response should be parsed and new IP and lobby ID returned to the connectRPC

        return response
    else:
        print("Error: " + response.message)
        return 1