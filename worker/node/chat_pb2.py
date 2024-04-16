# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04\x63hat\"H\n\x0e\x43hannelMessage\x12\x12\n\nchannel_id\x18\x01 \x01(\t\x12\x11\n\tsender_id\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"+\n\x15\x43hannelMessageRequest\x12\x12\n\nchannel_id\x18\x01 \x01(\t\"@\n\x07Message\x12\x11\n\tsender_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x03\"*\n\x06Status\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\".\n\tLobbyInfo\x12\x10\n\x08lobby_id\x18\x01 \x01(\x03\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"!\n\nPlayerInfo\x12\x13\n\x0bplayer_role\x18\x01 \x01(\x03\"\x1b\n\x0bSecretWords\x12\x0c\n\x04word\x18\x01 \x01(\t\"\x19\n\x08GameInfo\x12\r\n\x05start\x18\x01 \x01(\x08\x32\xf3\x01\n\x0b\x43hatService\x12:\n\x12SendChannelMessage\x12\x14.chat.ChannelMessage\x1a\x0c.chat.Status\"\x00\x12\x44\n\x12GetChannelMessages\x12\x1b.chat.ChannelMessageRequest\x1a\r.chat.Message\"\x00\x30\x01\x12\x30\n\tJoinLobby\x12\x0f.chat.LobbyInfo\x1a\x10.chat.PlayerInfo\"\x00\x12\x30\n\tStartGame\x12\x0e.chat.GameInfo\x1a\x11.chat.SecretWords\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CHANNELMESSAGE']._serialized_start=20
  _globals['_CHANNELMESSAGE']._serialized_end=92
  _globals['_CHANNELMESSAGEREQUEST']._serialized_start=94
  _globals['_CHANNELMESSAGEREQUEST']._serialized_end=137
  _globals['_MESSAGE']._serialized_start=139
  _globals['_MESSAGE']._serialized_end=203
  _globals['_STATUS']._serialized_start=205
  _globals['_STATUS']._serialized_end=247
  _globals['_LOBBYINFO']._serialized_start=249
  _globals['_LOBBYINFO']._serialized_end=295
  _globals['_PLAYERINFO']._serialized_start=297
  _globals['_PLAYERINFO']._serialized_end=330
  _globals['_SECRETWORDS']._serialized_start=332
  _globals['_SECRETWORDS']._serialized_end=359
  _globals['_GAMEINFO']._serialized_start=361
  _globals['_GAMEINFO']._serialized_end=386
  _globals['_CHATSERVICE']._serialized_start=389
  _globals['_CHATSERVICE']._serialized_end=632
# @@protoc_insertion_point(module_scope)
