# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: ms/audio_grpc/proto/audio_service.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'ms/audio_grpc/proto/audio_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'ms/audio_grpc/proto/audio_service.proto\x12\x08\x61udiogen\" \n\x10TextInputRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\"$\n\rAudioResponse\x12\x13\n\x0b\x61udio_chunk\x18\x01 \x01(\x0c\x32Z\n\x0c\x41udioService\x12J\n\x11GenerateFartAudio\x12\x1a.audiogen.TextInputRequest\x1a\x17.audiogen.AudioResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ms.audio_grpc.proto.audio_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TEXTINPUTREQUEST']._serialized_start=53
  _globals['_TEXTINPUTREQUEST']._serialized_end=85
  _globals['_AUDIORESPONSE']._serialized_start=87
  _globals['_AUDIORESPONSE']._serialized_end=123
  _globals['_AUDIOSERVICE']._serialized_start=125
  _globals['_AUDIOSERVICE']._serialized_end=215
# @@protoc_insertion_point(module_scope)
