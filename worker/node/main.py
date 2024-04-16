import grpc
import time
import redis
from concurrent import futures
import os
import json
from dotenv import load_dotenv

import worker_pb2
import worker_pb2_grpc

###
# References:
# - https://grpc.io/docs/languages/python/basics/
# - https://redis.io/docs/connect/clients/python/
# - 
###

# CONSTANTS
MAX_WORKERS = 10
REDIS_HOST = 'localhost'
CHANNELS = {} 

load_dotenv()  # Load environment variables from .env

### TODO:
# - Add private chat with bidirectional communication
# - Add function to list all channels
# - Improve client connection closing handling
###

class WorkerServiceServicer(worker_pb2_grpc.WorkerServiceServicer):
    def SendPrivateMessage(self, request, context):
        print("SendPrivateMessage") # Debug
        
        try:
            # Check if the sender and recipient are the same
            if request.sender_id == request.recipient_id:
                return worker_pb2.Status(success=False, message="Sender and recipient cannot be the same")
            
            # Check if the message is empty
            if request.content == "":
                return worker_pb2.Status(success=False, message="Message cannot be empty")
            
            # Connect to Redis
            redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
            #redis_client.flushall() # Debug (Clear all keys in Redis)
            
            # Store the message in Redis
            redis_key = f"private_messages:{request.recipient_id}"  # Key format: private_messages:<recipient_id>
            redis_object = json.dumps({ # JSON object to store in Redis
                "sender_id": request.sender_id,
                "content": request.content,
                "timestamp": int(time.time())
            })
            redis_client.rpush(redis_key, redis_object) # Append the message to the Redis list

            # Return status
            return worker_pb2.Status(success=True, message="Message sent successfully")
        except Exception as e:
            print(e)  # Debug
            return worker_pb2.Status(success=False, message="Error occurred")

    def GetPrivateMessages(self, request, context):
        print("GetPrivateMessages")  

        try:
            # Connect to Redis
            redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))

            # Construct the Redis keys for both directions of the conversation
            key1 = f"private_messages:{request.sender_id}"  # Where the user is the recipient
            key2 = f"private_messages:{request.recipient_id}" # Where the user is the sender

            # Fetch messages from Redis using LRANGE
            messages = redis_client.lrange(key1, 0, -1) + redis_client.lrange(key2, 0, -1)
            
            # Parse messages only between the sender and recipient
            #messages = [message for message in messages if json.loads(message)["user_id"] == request.sender_id or json.loads(message)["user_id"] == request.recipient_id]
            messages = [message for message in messages if json.loads(message)["sender_id"] in {request.sender_id, request.recipient_id}]

            # Yield individual messages
            for message_json in messages:
                # Parse the JSON object
                message_dict = json.loads(message_json)
                
                # Yield the message
                yield worker_pb2.Message(sender_id=message_dict["sender_id"], content=message_dict["content"], timestamp=message_dict["timestamp"]) 

        except Exception as e:
            print(e) 
            return worker_pb2.Status(success=False, message="Error occurred")
        
    def SendChannelMessage(self, request, context):
        print("SendChannelMessage")
        
        try: 
            # Check if the channel exists
            if request.channel_id not in CHANNELS:
                return worker_pb2.Status(success=False, message="Channel does not exist")
            
            # Check if the message is empty
            if request.content == "":
                return worker_pb2.Status(success=False, message="Message cannot be empty")
            
            # Connect to Redis
            redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))
            #redis_client.flushall() # Debug (Clear all keys in Redis)
            
            # Store the message in Redis
            redis_key = f"channel_messages:{request.channel_id}"  # Key format: channel_messages:<channel_id>
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
                key = f"channel_messages:{request.channel_id}"  # Key format: channel_messages:<channel_id>
                
                # Initial fetch
                messages = redis_client.zrangebyscore(key, last_timestamp, '+inf', withscores=True)
                
                # Yield initially fetched messages
                for message, timestamp in messages: 
                    # Yield the message
                    message_dict = json.loads(message)
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
                        yield worker_pb2.Message(sender_id=message_dict["sender_id"], content=message_dict["content"], timestamp=int(timestamp))
                        
                        # Store the last timestamp
                        last_timestamp = timestamp

                    time.sleep(1)  # Sleep for 1 second before fetching the next message
                    
                # Return status
                return worker_pb2.Status(success=True, message="Channel connection closed")

            except Exception as e:
                print(e) 
                return worker_pb2.Status(success=False, message="Error occurred")
            
    def JoinLobby(self, request, context):
        user = request.user_id
        lobby = request.lobby_id
        print(user + " is joining lobby: " + str(lobby))


        return worker_pb2.PlayerInfo(player_role=1)
    
    def GetStatus(self, request, context):
        print("Get status.")
        print(request.success)
        print(request.message)
        return worker_pb2.Status(success=True, message="Worker is working.")

# Function for initializing data structures     
def initialize():
    # Initialize CHANNELS
    #CHANNELS["general"] = set()
    #CHANNELS["coding"] = set()
    #CHANNELS["random"] = set()
    CHANNELS["0"] = set()
    return 0

def serve():
    # Initialize data structures
    initialize()
    
    # Initialize the server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(WorkerServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            print("Server is running...")
            time.sleep(86400)  # One day
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
