# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import sys_worker_pb2 as sys__worker__pb2


class WorkerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NewLobby = channel.unary_unary(
                '/worker.WorkerService/NewLobby',
                request_serializer=sys__worker__pb2.LobbyInfo.SerializeToString,
                response_deserializer=sys__worker__pb2.Status.FromString,
                )
        self.JoinLobby = channel.unary_unary(
                '/worker.WorkerService/JoinLobby',
                request_serializer=sys__worker__pb2.LobbyInfo.SerializeToString,
                response_deserializer=sys__worker__pb2.Status.FromString,
                )


class WorkerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NewLobby(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinLobby(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NewLobby': grpc.unary_unary_rpc_method_handler(
                    servicer.NewLobby,
                    request_deserializer=sys__worker__pb2.LobbyInfo.FromString,
                    response_serializer=sys__worker__pb2.Status.SerializeToString,
            ),
            'JoinLobby': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinLobby,
                    request_deserializer=sys__worker__pb2.LobbyInfo.FromString,
                    response_serializer=sys__worker__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'worker.WorkerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NewLobby(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/worker.WorkerService/NewLobby',
            sys__worker__pb2.LobbyInfo.SerializeToString,
            sys__worker__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinLobby(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/worker.WorkerService/JoinLobby',
            sys__worker__pb2.LobbyInfo.SerializeToString,
            sys__worker__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)