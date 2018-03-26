import datetime
import json
import typing

from azure.functions import _abc as azf_abc

from . import meta
from .. import protos


class GridEvent(azf_abc.GridEvent):
    """An EventGrid event message."""

    def __init__(self, *,
                 id=None, body=None,
                 topic=None,
                 subject=None,
                 event_type=None,
                 event_time=None,
                 data_version=None):
        self.__id = id
        self.__body = body
        self.__subject = subject
        self.__event_type = event_type
        self.__event_time = event_time
        self.__data_version = data_version

    @property
    def id(self) -> typing.Optional[str]:
        return self.__id

    def get_json(self) -> typing.Any:
        pass

    @property
    def topic(self) -> typing.Optional[str]:
        return self.__topic

    @property
    def subject(self) -> typing.Optional[str]:
        return self.__subject

    @property
    def event_type(self) -> typing.Optional[str]:
        return self.__event_type

    @property
    def event_time(self) -> datetime.datetime:
        return self.__event_time

    @property
    def data_version(self) -> typing.Optional[str]:
        return self.__data_version

    def __repr__(self) -> str:
        return (
            f'<azure.GridEvent id={self.id} '
            f'topic={self.topic} '
            f'subject={self.subject} '
            f'at 0x{id(self):0x}>'
        )


class GridEventInConverter(meta.InConverter,
                           binding='eventGridTrigger', trigger=True):

    @classmethod
    def check_python_type(cls, pytype: type) -> bool:
        return issubclass(pytype, azf_abc.GridEvent)

    @classmethod
    def from_proto(cls, data: protos.TypedData, *,
                   pytype: typing.Optional[type],
                   trigger_metadata) -> typing.Any:
        data_type = data.WhichOneof('data')

        if data_type == 'string':
            body = data.string

        elif data_type == 'bytes':
            body = data.bytes

        else:
            raise NotImplementedError(
                f'unsupported queue payload type: {data_type}')

        if trigger_metadata is None:
            raise NotImplementedError(
                f'missing trigger metadata for queue input')

        return GridEvent(
            id=cls._decode_trigger_metadata_field(
                trigger_metadata, 'Id', python_type=str),
            body=body,
            dequeue_count=cls._decode_trigger_metadata_field(
                trigger_metadata, 'DequeueCount', python_type=int),
            expiration_time=cls._parse_datetime_metadata(
                trigger_metadata, 'ExpirationTime'),
            insertion_time=cls._parse_datetime_metadata(
                trigger_metadata, 'InsertionTime'),
            next_visible_time=cls._parse_datetime_metadata(
                trigger_metadata, 'NextVisibleTime'),
            pop_receipt=cls._decode_trigger_metadata_field(
                trigger_metadata, 'PopReceipt', python_type=str)
        )
