import worker_pb2
import worker_pb2_grpc
from datetime import datetime
import threading 
import grpc

COLOR_GREEN = "\033[92m"  
COLOR_YELLOW = "\033[93m"  
COLOR_RED = "\033[91m"  
COLOR_BLUE = '\033[34m'
COLOR_RESET = "\033[0m"  # Reset color to default

### References:
# - https://docs.python.org/3/library/threading.html
# - https://grpc.io/docs/languages/python/basics/
# - 
###

# Receive messages from the channel
def receive_messages(stub, lobby_id, user_id, shutdown_event):
    while not shutdown_event.is_set():
        try: 
            # Get messages from the channel
            lobby_id = str(lobby_id)
            request = worker_pb2.ChannelMessageRequest(lobby_id=lobby_id, user_id=user_id)
            message_stream = stub.GetChannelMessages(request)
            
            # Print messages as they arrive
            for message in message_stream:
                # Print the message with a timestamp
                timestamp = datetime.fromtimestamp(message.timestamp).strftime('%Y-%m-%d %H:%M:%S')
                print(COLOR_GREEN + f"[{timestamp}] {message.sender_id}: {message.content}" + COLOR_RESET)
                
                # Check if the user wants to exit the channel
                if shutdown_event.is_set():
                    break
        except grpc._channel._MultiThreadedRendezvous as e:        
            print(COLOR_RED + "\nChannel connection closed" + COLOR_RESET)
        except Exception as e:
            print(COLOR_RED + "Error receiving messages:", e + COLOR_RESET)
            return 1
    
    return 0

# Send messages to the channel 
def send_message(stub, lobby_id, user_id, shutdown_event):
    while True:
        content = input() # Get user input
        
        # Check if the user wants to exit the channel
        if content.lower() == 'exit' or shutdown_event.is_set():
            break

        # Send the message to the server
        request = worker_pb2.LobbyMessage(lobby_id=lobby_id, sender_id=user_id, content=content)
        response = stub.SendChannelMessage(request)
        if not response.success:
            print(COLOR_RED + "Error sending message: " + response.message + COLOR_RESET)
            
    return 0


def connectToChatChannel(user_id, lobby_id, stub):
    # Print information about the lobby
    print(COLOR_GREEN + f"\nConnected to lobby {lobby_id}" + COLOR_RESET)
    print(COLOR_YELLOW + "Type 'exit' to leave the lobby\n" + COLOR_RESET)
    
    # Create an event to signal the threads to stop
    shutdown_event = threading.Event()
    
    # Start a thread for receiving messages from the lobby
    receive_thread = threading.Thread(target=receive_messages, args=(stub, lobby_id, user_id, shutdown_event))
    receive_thread.start()

    # Start a thread for sending messages to the lobby
    sending_thread = threading.Thread(target=send_message, args=(stub, lobby_id, user_id, shutdown_event))
    sending_thread.start()
    sending_thread.join() # Wait for the sending thread to finish
    
    # Signal the receiving thread to stop if the sending thread finishes
    shutdown_event.set()

    return 0