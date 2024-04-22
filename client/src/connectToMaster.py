import master_pb2
import master_pb2_grpc
from datetime import datetime

def sendInformationToMaster(lobby_choice, USER_ID, client):
    # Create a channel stub
    try:
        client = client
        stub = master_pb2_grpc.MasterServiceStub(client)
    except Exception as e:
        print("Error: connecting to server")
        print(e)
        return 1
    
    if lobby_choice == 1:
        # Send the message to the server, specifying if creating a new lobby or joining an existing.
        request = master_pb2.NewLobbyParameters(
            lobby_choice=1,
            user_id=USER_ID,
        )
        
        # Handle the response
        response = stub.CreateNewLobby(request)
        if response:
            print("Received a response") # Debug

            lobby_info = [response.ip, response.lobby_id]
            return lobby_info
    elif lobby_choice == 2:
        # Send the message to the server, specifying if creating a new lobby or joining an existing.
        lobby_choice = input("Give lobby's id: ")
        request = master_pb2.LobbyParameters(
            lobby_id=int(lobby_choice),
            user_id=USER_ID,
        )
        
        # Handle the response
        response = stub.JoinLobby(request)
        if response:
            print("Received a response") # Debug

            lobby_info = [response.ip, response.lobby_id]
            return lobby_info
        
    else:
        print("Error: " + response.message)
        return 1


