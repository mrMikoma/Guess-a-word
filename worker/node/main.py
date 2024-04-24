import grpc
import time
import redis
from concurrent import futures
import os
import json
from dotenv import load_dotenv
import requests
import socket

import worker_pb2
import worker_pb2_grpc
import sys_worker_pb2
import sys_worker_pb2_grpc
from src.gameLogic import *

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
#CHANNELS = [[0, [], [], [], ""]] #DEBUG
ADMINS = []
DB_HOST = os.getenv('DB_HOST')
DB_ADDRESS="http://" + DB_HOST + ":8080" # if running in docker use address of "database-adapter-1", else use "localhost:8080"
HOST_IP = os.getenv('HOST_IP')

load_dotenv()  # Load environment variables from .env

### TODO:

###

class WorkerServiceServicer(worker_pb2_grpc.WorkerServiceServicer):
        
    def SendChannelMessage(self, request, context):
        print("SendChannelMessage")
        
        try: 
            # Check if the message is empty
            if request.content == "":
                return worker_pb2.Status(success=False, message="Message cannot be empty")

            # Check if the channel exists
            print(CHANNELS) #DEBUG
            print(request.lobby_id) #DEBUG
            for sublist in CHANNELS:
                print("sublist:", sublist) #DEBUG
                print("sublist[0]:", sublist[0]) #DEBUG
                if sublist[0] == request.lobby_id:
                
                    # Connect to Redis
                    redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
                    #redis_client.flushall() # Debug (Clear all keys in Redis)

                    # Check if message is same as the secret word
                    if request.content == sublist[4]:
                        player_index = sublist[1].index(request.sender_id)
                        # Check if sender is not admin
                        if player_index != 0:
                            # Check if player hasn't guessed right yet
                            if sublist[3][player_index] == 0:
                                playerCount = 0
                                # Count how many players haven't yet guessed right
                                for player in sublist[3]:
                                    if player == 0:
                                        playerCount += 1
                                # Mark player as guessed and add points to them
                                sublist[3][player_index] = 1
                                sublist[2][player_index] += playerCount - 1
                            message = str(request.sender_id) + " has quessed correctly!"
                        else:
                            message = request.content
                    else:
                        message = request.content
                    
                    # Store the message in Redis
                    redis_key = f"channel_messages:{request.lobby_id}"  # Key format: channel_messages:<channel_id>
                    redis_object = json.dumps({ # JSON object to store in Redis
                        "sender_id": request.sender_id,
                        "content": message,
                        "timestamp": int(time.time())
                    })

                    # ZADD for Sorted Set to store messages in order of timestamp
                    redis_client.zadd(redis_key, {redis_object: int(time.time())}) # Append the message to the Redis sorted set
                    
                    # Check if everyone has guessed correctly
                    playerCount = 0
                    for player in sublist[3]:
                        if player == 0:
                            playerCount += 1
                            
                    # Print score if necessary
                    if playerCount == 1:
                        message = "Everyone quessed correctly!\nHere are the results:"
                        for i in range(1, len(sublist[1])):
                            player = sublist[1][i]
                            points = str(sublist[2][i])
                            message += "\n" + player + ": " + points
                        message += "\nTo start a new round, the host must type 'exit' and start again"
                        # Store the message in Redis
                        redis_key = f"channel_messages:{request.lobby_id}"  # Key format: channel_messages:<channel_id>
                        redis_object = json.dumps({ # JSON object to store in Redis
                            "sender_id": sublist[1][0],
                            "content": message,
                            "timestamp": int(time.time())
                        })
                        # ZADD for Sorted Set to store messages in order of timestamp
                        redis_client.zadd(redis_key, {redis_object: int(time.time())}) # Append the message to the Redis sorted set

                    # Return status
                    return worker_pb2.Status(success=True, message="Message sent successfully")
            
            return worker_pb2.Status(success=False, message="Channel does not exist")
            
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

                    #if message_dict["sender_id"] != request.user_id:
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
                        #if message_dict["sender_id"] != request.user_id:
                        yield worker_pb2.Message(sender_id=message_dict["sender_id"], content=message_dict["content"], timestamp=int(timestamp))
                        
                        # Store the last timestamp
                        last_timestamp = timestamp

                    time.sleep(0.1)  # Sleep for 0.1 second before fetching the next message
                    
                # Return status
                return worker_pb2.Status(success=True, message="Channel connection closed")

            except Exception as e:
                print(e) 
                return worker_pb2.Status(success=False, message="Error occurred")
            
    def JoinLobby(self, request, context):
        print("JoinLobby")

        player_role = -1
        user = str(request.user_id)
        lobby = int(request.lobby_id)
        print(user + " is joining lobby: " + str(lobby) + "...")
        
        # this loop currently has no failure handling in case no lobby was found, which breaks the client
        
        for sublist in CHANNELS:
            print("sublist:", sublist) #DEBUG
            print("sublist[0]:", sublist[0]) #DEBUG
            if sublist[0] == lobby:

                # Add player to the lobby. 
                user_list = sublist[1]
                point_list = sublist[2]
                guess_list = sublist[3]

                # If player is first, let's make them the admin. 
                if len(user_list) == 0:
                    player_role = 0
                else: 
                    player_role = 1

                user_list.append(user)
                point_list.append(0)
                guess_list.append(0)

                
                print(user + " joined lobby: " + str(lobby))
                print("Their role is " + str(player_role))
                break
            else:
                print(str(sublist[0]),"is not the same as",str(lobby))
                continue

        return worker_pb2.PlayerInfo(player_role=player_role)
    
    def GetStatus(self, request, context):
        print("GetStatus")
        print(request.success)
        print(request.message)
        return worker_pb2.Status(success=True, message="Worker is working.")
    
    def StartGame(self, request, context):
        print("StartGame")

        # Get new random word from the list
        secretWord = getWord("src/wordlist.txt")
        print(secretWord)

        # Save the secret word in the lobby info
        lobby = int(request.lobby_id) 
        for sublist in CHANNELS:
            print("sublist:", sublist) #DEBUG
            print("sublist[0]:", sublist[0]) #DEBUG
            if sublist[0] == lobby:
                sublist[4] = secretWord
                # Set the guessed list so that no-one has guessed
                for player in range(len(sublist[3])):
                    sublist[3][player] = 0

        print("A game starts.")
        if request.start:
            return worker_pb2.SecretWords(word=secretWord)
        
    

class SysWorkerServiceServicer(sys_worker_pb2_grpc.SysWorkerServiceServicer):
    def NewLobby(self, request, context):
        print("NewLobby")
        lobby_id = int(request.lobby_id)
        user_id = str(request.user_id)
        new_list = [lobby_id, [], [], [], ""]
        CHANNELS.append(new_list)
        print("Created new lobby", lobby_id)

        return sys_worker_pb2.MasterStatus(status = "OK", desc="New lobby added.")
    
    def CheckStatus(self, request, context):
        print("CheckStatus")
        print("Master checked on me, telling it I'm fine")
        return sys_worker_pb2.MasterStatus(status = "OK", desc="I am still running.")

# Function for initializing data structures     
def initialize():
    # Get the worker's IP address
    print("Worker IP address:", HOST_IP) # Print the worker's IP address
    
    try:
        # Send the worker's IP address to the database
        response = requests.post(url=DB_ADDRESS + "/workers/?ip_address=" + HOST_IP)
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
    sys_worker_pb2_grpc.add_SysWorkerServiceServicer_to_server(SysWorkerServiceServicer(), server)
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
