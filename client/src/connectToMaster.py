from src.connectRPC import *
import chat_pb2
import chat_pb2_grpc
from datetime import datetime

def sendInformationToMaster(lobby_choice, USER_ID):
    # Create a channel stub
    try:
        client = getClient()
        stub = chat_pb2_grpc.ChatServiceStub(client)
    except Exception as e:
        print("Error: connecting to server")
        print(e)
        return 1
    
    # Send the message to the server, specifying if creating a new lobby or joining an existing.
    request = chat_pb2.PrivateMessage(
        user_id=USER_ID,
        lobby_choice=lobby_choice,
    )
    
    # Handle the response
    response = stub.SendPrivateMessage(request)
    if response.success:
        print("Received a response") # Debug

        # HERE response should be parsed and new IP and lobby ID returned to the connectRPC

        return response
    else:
        print("Error: " + response.message)
        return 1


# def getPrivateMessages(user_id):
    # Ask for the username of the person to get the messages from
    recipient_id = input("Enter username of the person you want to get messages from: ")
    
    # Cet RPC client
    client = getClient()
    if client == 1:
        return 1
    
    # Create a channel stub
    stub = chat_pb2_grpc.ChatServiceStub(client)
    
    request = chat_pb2.PrivateMessageRequest(
        sender_id=user_id, 
        recipient_id=recipient_id
    )
    messages = stub.GetPrivateMessages(request)

    # Collect messages with timestamps
    message_list = [(message.timestamp, message.sender_id, message.content) for message in messages]
    
    # If no messages are found, print a message and return
    if not message_list:
        print("\nNo messages found")
        return 0

    # Sort by timestamp in ascending order
    message_list.sort(key=lambda item: item[0])

    # Print messages with formatted timestamps
    print("")
    for timestamp, sender_id, content in message_list:
        dt_object = datetime.fromtimestamp(timestamp)
        print(f"[{dt_object.strftime('%Y-%m-%d %H:%M')}] {sender_id}: {content}") 
    
    return 0

