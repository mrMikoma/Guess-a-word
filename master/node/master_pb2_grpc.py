# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import master_pb2 as master__pb2


class MasterServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateNewLobby = channel.unary_unary(
                '/master.MasterService/CreateNewLobby',
                request_serializer=master__pb2.NewLobbyParameters.SerializeToString,
                response_deserializer=master__pb2.LobbyInfo.FromString,
                )
        self.JoinLobby = channel.unary_unary(
                '/master.MasterService/JoinLobby',
                request_serializer=master__pb2.LobbyParameters.SerializeToString,
                response_deserializer=master__pb2.LobbyInfo.FromString,
                )
        self.DeleteLobby = channel.unary_unary(
                '/master.MasterService/DeleteLobby',
                request_serializer=master__pb2.LobbyParameters.SerializeToString,
                response_deserializer=master__pb2.StatusForClient.FromString,
                )


class MasterServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateNewLobby(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinLobby(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteLobby(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateNewLobby': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateNewLobby,
                    request_deserializer=master__pb2.NewLobbyParameters.FromString,
                    response_serializer=master__pb2.LobbyInfo.SerializeToString,
            ),
            'JoinLobby': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinLobby,
                    request_deserializer=master__pb2.LobbyParameters.FromString,
                    response_serializer=master__pb2.LobbyInfo.SerializeToString,
            ),
            'DeleteLobby': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteLobby,
                    request_deserializer=master__pb2.LobbyParameters.FromString,
                    response_serializer=master__pb2.StatusForClient.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'master.MasterService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MasterService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateNewLobby(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master.MasterService/CreateNewLobby',
            master__pb2.NewLobbyParameters.SerializeToString,
            master__pb2.LobbyInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/master.MasterService/JoinLobby',
            master__pb2.LobbyParameters.SerializeToString,
            master__pb2.LobbyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteLobby(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master.MasterService/DeleteLobby',
            master__pb2.LobbyParameters.SerializeToString,
            master__pb2.StatusForClient.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
