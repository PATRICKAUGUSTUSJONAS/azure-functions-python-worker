import collections.abc
import json
import typing

from azure.functions import _cosmosdb as cdb

from . import meta
from .. import protos


class CosmosDBConverter(meta.InConverter, meta.OutConverter,
                        binding='documentDB'):

    @classmethod
    def check_input_type_annotation(cls, pytype: type) -> bool:
        return issubclass(pytype, cdb.DocumentList)

    @classmethod
    def check_output_type_annotation(cls, pytype: type) -> bool:
        return issubclass(pytype, (cdb.DocumentList, cdb.Document))

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

        return cdb.Document(
            body=body
        )

    @classmethod
    def to_proto(cls, obj: typing.Any, *,
                 pytype: typing.Optional[type]) -> protos.TypedData:
        if isinstance(obj, cdb.Document):
            data = cdb.DocumentList([obj])

        elif isinstance(obj, cdb.DocumentList):
            data = obj

        elif isinstance(obj, collections.abc.Iterable):
            data = cdb.DocumentList()

            for doc in obj:
                if not isinstance(doc, cdb.Document):
                    raise NotImplementedError
                else:
                    data.append(doc)

        else:
            raise NotImplementedError

        return protos.TypedData(
            json=json.dumps([dict(d) for d in data])
        )


class CosmosDBTriggerConverter(CosmosDBConverter,
                               binding='cosmosDBTrigger', trigger=True):
    pass
