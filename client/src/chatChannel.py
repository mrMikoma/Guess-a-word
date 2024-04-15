from src.connectRPC import *
import chat_pb2
import chat_pb2_grpc
from datetime import datetime
import threading 

### References:
# - https://docs.python.org/3/library/threading.html
# - https://grpc.io/docs/languages/python/basics/
# - 
###

### TODO:
# - Improve a way to exit the chat channel
# - Improve error handling
###

# Receive messages from the channel
def receive_messages(stub, channel_id, shutdown_event):
    while not shutdown_event.is_set():
        try: 
            # Get messages from the channel
            request = chat_pb2.ChannelMessageRequest(channel_id=channel_id)
            message_stream = stub.GetChannelMessages(request)
            
            # Print messages as they arrive
            for message in message_stream:
                # Print the message with a timestamp
                timestamp = datetime.fromtimestamp(message.timestamp).strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] {message.sender_id}: {message.content}")
                
                # Check if the user wants to exit the channel
                if shutdown_event.is_set():
                    break
        except grpc._channel._MultiThreadedRendezvous as e:        
            print("\nChannel connection closed")
        except Exception as e:
            print("Error receiving messages:", e)
            return 1
    
    return 0

# Send messages to the channel 
def send_message(stub, channel_id, sender_id, shutdown_event):
    while True:
        content = input() # Get user input
        
        # Check if the user wants to exit the channel
        if content.lower() == 'exit' or shutdown_event.is_set():
            break

        # Send the message to the server
        request = chat_pb2.ChannelMessage(channel_id=channel_id, sender_id=sender_id, content=content)
        response = stub.SendChannelMessage(request)
        if not response.success:
            print("Error sending message:", response.message)
            
    return 0


def connectToChatChannel(user_id):
    # Ask for the channel ID
    channel_id = input("Enter the channel name you want to connect to: ")
    
    # Establish gRPC Connection
    client = getClient()
    stub = chat_pb2_grpc.ChatServiceStub(client)
    
    # Print information about the channel
    print(f"\nConnected to channel {channel_id}")
    print("Type 'exit' to leave the channel\n")
    
    # Create an event to signal the threads to stop
    shutdown_event = threading.Event()
    
    # Start a thread for receiving messages from the channel
    receive_thread = threading.Thread(target=receive_messages, args=(stub, channel_id, shutdown_event))
    receive_thread.start()

    # Start a thread for sending messages to the channel
    sending_thread = threading.Thread(target=send_message, args=(stub, channel_id, user_id, shutdown_event))
    sending_thread.start()
    sending_thread.join() # Wait for the sending thread to finish
    
    # Signal the receiving thread to stop if the sending thread finishes
    shutdown_event.set()

    return 0