# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: master.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmaster.proto\x12\x06master\";\n\x12NewLobbyParameters\x12\x14\n\x0clobby_choice\x18\x01 \x01(\x03\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"4\n\x0fLobbyParameters\x12\x10\n\x08lobby_id\x18\x01 \x01(\x03\x12\x0f\n\x07user_id\x18\x02 \x01(\t\")\n\tLobbyInfo\x12\n\n\x02IP\x18\x01 \x01(\t\x12\x10\n\x08lobby_id\x18\x02 \x01(\x03\x32\x8d\x01\n\rMasterService\x12\x41\n\x0e\x43reateNewLobby\x12\x1a.master.NewLobbyParameters\x1a\x11.master.LobbyInfo\"\x00\x12\x39\n\tJoinLobby\x12\x17.master.LobbyParameters\x1a\x11.master.LobbyInfo\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'master_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_NEWLOBBYPARAMETERS']._serialized_start=24
  _globals['_NEWLOBBYPARAMETERS']._serialized_end=83
  _globals['_LOBBYPARAMETERS']._serialized_start=85
  _globals['_LOBBYPARAMETERS']._serialized_end=137
  _globals['_LOBBYINFO']._serialized_start=139
  _globals['_LOBBYINFO']._serialized_end=180
  _globals['_MASTERSERVICE']._serialized_start=183
  _globals['_MASTERSERVICE']._serialized_end=324
# @@protoc_insertion_point(module_scope)
