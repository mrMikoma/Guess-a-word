# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sys-master.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10sys-master.proto\x12\x06master\"4\n\x0cNewLobbyInfo\x12\x10\n\x08lobby_id\x18\x01 \x01(\t\x12\x12\n\nnew_status\x18\x02 \x01(\t\"&\n\x06Status\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\t2I\n\x10SysMasterService\x12\x35\n\x0bUpdateLobby\x12\x14.master.NewLobbyInfo\x1a\x0e.master.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sys_master_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_NEWLOBBYINFO']._serialized_start=28
  _globals['_NEWLOBBYINFO']._serialized_end=80
  _globals['_STATUS']._serialized_start=82
  _globals['_STATUS']._serialized_end=120
  _globals['_SYSMASTERSERVICE']._serialized_start=122
  _globals['_SYSMASTERSERVICE']._serialized_end=195
# @@protoc_insertion_point(module_scope)
