# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: monit.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0bmonit.proto\x12\x05monit\x1a\x1bgoogle/protobuf/empty.proto"&\n\x0fGetLastResponse\x12\x13\n\x0bresult_json\x18\x01 \x01(\t"\x1d\n\x0cListResponse\x12\r\n\x05items\x18\x01 \x03(\t""\n\rGetAvgRequest\x12\x11\n\tparameter\x18\x01 \x01(\x05"%\n\x0eGetAvgResponse\x12\x13\n\x0bresult_json\x18\x01 \x01(\t2\xee\x01\n\x0cMonitService\x12\x37\n\x05\x43heck\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\x12\x39\n\x07GetLast\x12\x16.google.protobuf.Empty\x1a\x16.monit.GetLastResponse\x12\x33\n\x04List\x12\x16.google.protobuf.Empty\x1a\x13.monit.ListResponse\x12\x35\n\x06GetAvg\x12\x14.monit.GetAvgRequest\x1a\x15.monit.GetAvgResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "monit_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_GETLASTRESPONSE"]._serialized_start = 51
    _globals["_GETLASTRESPONSE"]._serialized_end = 89
    _globals["_LISTRESPONSE"]._serialized_start = 91
    _globals["_LISTRESPONSE"]._serialized_end = 120
    _globals["_GETAVGREQUEST"]._serialized_start = 122
    _globals["_GETAVGREQUEST"]._serialized_end = 156
    _globals["_GETAVGRESPONSE"]._serialized_start = 158
    _globals["_GETAVGRESPONSE"]._serialized_end = 195
    _globals["_MONITSERVICE"]._serialized_start = 198
    _globals["_MONITSERVICE"]._serialized_end = 436
# @@protoc_insertion_point(module_scope)
