# Proto initialization

0. **Proto init**
   Run the following command in your terminal to change into correct directory. These commands are supposed to be run in the root directory of the application:

   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=worker/node --grpc_python_out=worker/node protos/worker.proto
   ```

   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/master.proto
   ```

   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/worker.proto
   ```
   
   ```bash
   python3 -m grpc_tools.protoc -Iprotos --python_out=master/node --grpc_python_out=master/node protos/master.proto
   ```
