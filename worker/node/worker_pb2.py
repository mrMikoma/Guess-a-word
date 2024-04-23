# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: worker.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cworker.proto\x12\x06worker\"D\n\x0cLobbyMessage\x12\x10\n\x08lobby_id\x18\x01 \x01(\x03\x12\x11\n\tsender_id\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\":\n\x15\x43hannelMessageRequest\x12\x10\n\x08lobby_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"@\n\x07Message\x12\x11\n\tsender_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\"*\n\x06Status\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\".\n\tLobbyInfo\x12\x10\n\x08lobby_id\x18\x01 \x01(\x03\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"!\n\nPlayerInfo\x12\x13\n\x0bplayer_role\x18\x01 \x01(\x03\"\x1b\n\x0bSecretWords\x12\x0c\n\x04word\x18\x01 \x01(\t\"+\n\x08GameInfo\x12\r\n\x05start\x18\x01 \x01(\x08\x12\x10\n\x08lobby_id\x18\x02 \x01(\x03\x32\xa0\x03\n\rWorkerService\x12<\n\x12SendChannelMessage\x12\x14.worker.LobbyMessage\x1a\x0e.worker.Status\"\x00\x12H\n\x12GetChannelMessages\x12\x1d.worker.ChannelMessageRequest\x1a\x0f.worker.Message\"\x00\x30\x01\x12\x34\n\tJoinLobby\x12\x11.worker.LobbyInfo\x1a\x12.worker.PlayerInfo\"\x00\x12\x35\n\x0bGetMessages\x12\x11.worker.LobbyInfo\x1a\x0f.worker.Message\"\x00\x30\x01\x12\x35\n\x0bSendMessage\x12\x14.worker.LobbyMessage\x1a\x0e.worker.Status\"\x00\x12\x34\n\tStartGame\x12\x10.worker.GameInfo\x1a\x13.worker.SecretWords\"\x00\x12-\n\tGetStatus\x12\x0e.worker.Status\x1a\x0e.worker.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'worker_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_LOBBYMESSAGE']._serialized_start=24
  _globals['_LOBBYMESSAGE']._serialized_end=92
  _globals['_CHANNELMESSAGEREQUEST']._serialized_start=94
  _globals['_CHANNELMESSAGEREQUEST']._serialized_end=152
  _globals['_MESSAGE']._serialized_start=154
  _globals['_MESSAGE']._serialized_end=218
  _globals['_STATUS']._serialized_start=220
  _globals['_STATUS']._serialized_end=262
  _globals['_LOBBYINFO']._serialized_start=264
  _globals['_LOBBYINFO']._serialized_end=310
  _globals['_PLAYERINFO']._serialized_start=312
  _globals['_PLAYERINFO']._serialized_end=345
  _globals['_SECRETWORDS']._serialized_start=347
  _globals['_SECRETWORDS']._serialized_end=374
  _globals['_GAMEINFO']._serialized_start=376
  _globals['_GAMEINFO']._serialized_end=419
  _globals['_WORKERSERVICE']._serialized_start=422
  _globals['_WORKERSERVICE']._serialized_end=838
# @@protoc_insertion_point(module_scope)
