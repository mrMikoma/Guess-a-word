# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sys-worker.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10sys-worker.proto\x12\x06worker\".\n\tLobbyInfo\x12\x10\n\x08lobby_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"&\n\x06Status\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\t2x\n\rWorkerService\x12/\n\x08NewLobby\x12\x11.worker.LobbyInfo\x1a\x0e.worker.Status\"\x00\x12\x36\n\x0fMasterJoinLobby\x12\x11.worker.LobbyInfo\x1a\x0e.worker.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sys_worker_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_LOBBYINFO']._serialized_start=28
  _globals['_LOBBYINFO']._serialized_end=74
  _globals['_STATUS']._serialized_start=76
  _globals['_STATUS']._serialized_end=114
  _globals['_WORKERSERVICE']._serialized_start=116
  _globals['_WORKERSERVICE']._serialized_end=236
# @@protoc_insertion_point(module_scope)
