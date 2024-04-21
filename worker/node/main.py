import grpc
import time
import redis
from concurrent import futures
import os
import json
from dotenv import load_dotenv
import requests

import worker_pb2
import worker_pb2_grpc
import sys_worker_pb2
import sys_worker_pb2_grpc
from src import gameLogic

###
# References:
# - https://grpc.io/docs/languages/python/basics/
# - https://redis.io/docs/connect/clients/python/
# - 
###

# CONSTANTS
MAX_WORKERS = 10
REDIS_HOST = os.getenv('REDIS_HOST') # In docker-compose.yml, the Redis service is named "redis"
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
CHANNELS = []
DB_ADDRESS="http://database-adapter-1:8080" # if running in docker use address of "database-adapter-1", else use "localhost:8080"

load_dotenv()  # Load environment variables from .env

### TODO:

###

class WorkerServiceServicer(worker_pb2_grpc.WorkerServiceServicer, sys_worker_pb2_grpc.SysWorkerServiceServicer):
        
    def SendChannelMessage(self, request, context):
        print("SendChannelMessage")
        
        try: 
            # Check if the channel exists
            print(CHANNELS)
            if len(CHANNELS) < request.lobby_id:
                return worker_pb2.Status(success=False, message="Channel does not exist")
            
            # Check if the message is empty
            if request.content == "":
                return worker_pb2.Status(success=False, message="Message cannot be empty")
            
            # Connect to Redis
            redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
            #redis_client.flushall() # Debug (Clear all keys in Redis)
            
            # Store the message in Redis
            redis_key = f"channel_messages:{request.lobby_id}"  # Key format: channel_messages:<channel_id>
            redis_object = json.dumps({ # JSON object to store in Redis
                "sender_id": request.sender_id,
                "content": request.content,
                "timestamp": int(time.time())
            })
            # ZADD for Sorted Set to store messages in order of timestamp
            redis_client.zadd(redis_key, {redis_object: int(time.time())}) # Append the message to the Redis sorted set
            
            # Return status
            return worker_pb2.Status(success=True, message="Message sent successfully")
        
        except Exception as e:
            print(e)
            return worker_pb2.Status(success=False, message="Error occurred")
        
    def GetChannelMessages(self, request, context):
            print("GetChannelMessages")  

            try:
                # Declare last timestamp
                last_timestamp = 0
                
                # Connect to Redis
                redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))

                # Construct the Redis key for the channel
                key = f"channel_messages:{request.lobby_id}"  # Key format: channel_messages:<channel_id>
                
                # Initial fetch
                messages = redis_client.zrangebyscore(key, last_timestamp, '+inf', withscores=True)
                
                # Yield initially fetched messages
                for message, timestamp in messages: 
                    # Yield the message
                    message_dict = json.loads(message)

                    if message_dict["sender_id"] != request.user_id:
                        yield worker_pb2.Message(sender_id=message_dict["sender_id"], content=message_dict["content"], timestamp=int(timestamp))
                    
                    # Store the last timestamp
                    last_timestamp = timestamp

                # Continuous streaming loop
                while True:
                    # Fetch messages from Redis using ZRANGEBYSCORE
                    messages = redis_client.zrangebyscore(key, last_timestamp + 1, '+inf', withscores=True)  

                    # Yield messages
                    for message, timestamp in messages:
                        message_dict = json.loads(message)
                        if message_dict["sender_id"] != request.user_id:
                            yield worker_pb2.Message(sender_id=message_dict["sender_id"], content=message_dict["content"], timestamp=int(timestamp))
                        
                        # Store the last timestamp
                        last_timestamp = timestamp

                    time.sleep(0.1)  # Sleep for 1 second before fetching the next message
                    
                # Return status
                return worker_pb2.Status(success=True, message="Channel connection closed")

            except Exception as e:
                print(e) 
                return worker_pb2.Status(success=False, message="Error occurred")
            
    def JoinLobby(self, request, context):
        print("JoinLobby")
        user = request.user_id
        lobby = request.lobby_id
        print(user + " is joining lobby: " + str(lobby))
        
        if len(CHANNELS) >= lobby + 1:
            print("Lobby exists.")

            # Add player to the lobby. 
            user_list = CHANNELS[lobby]
            print("Lobby alreade has these players: ")
            for user_in_list in user_list:
                print(user_in_list, end=", ")
            print()
            # If player is first, let's make them the admin. 
            if len(user_list) == 0:
                player_role = 0
            else:
                player_role = 1
            user_list.append(user)
            print(user + " joined lobby: " + str(lobby))


        return worker_pb2.PlayerInfo(player_role=player_role)
    
    def GetStatus(self, request, context):
        print("Get status.")
        print(request.success)
        print(request.message)
        return worker_pb2.Status(success=True, message="Worker is working.")
    
    def StartGame(self, request, context):
        print("StartGame")

        # Samuel can implement here how the secret word is decided.

        print("A game starts.")
        if request.start:
            return worker_pb2.SecretWords(word=gameLogic.getWord())


# Function for initializing data structures     
def initialize():
    lobby0 = []
    CHANNELS.append(lobby0)
    try:
        response = requests.post(url=DB_ADDRESS+"/workers/") # Send DB info that this worker has been created
    except Exception as e:
        print("Error trying to send worker info to db:", e)
    finally:
        return 0

def serve():
    # Initialize data structures
    initialize()
    
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(WorkerServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            print("Worker is running...")
            time.sleep(60)  # One minute
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
