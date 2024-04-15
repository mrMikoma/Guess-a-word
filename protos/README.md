# Proto initialization

0. **Proto init (might be broken)**
   Run the following command in your terminal to change into correct directory:
   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=server/node --grpc_python_out=server/node protos/chat.proto
   ```
   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/chat.proto
   ```
