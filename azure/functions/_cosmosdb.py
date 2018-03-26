import collections
import json

from . import _abc


class Document(_abc.Document, collections.UserDict):
    """An Azure Document."""

    @classmethod
    def from_json(cls, json_data: str) -> 'Document':
        return cls(json.loads(json_data))

    def __repr__(self) -> str:
        return (
            f'<azure.Document at 0x{id(self):0x}>'
        )


class DocumentList(_abc.DocumentList, collections.UserList):
    pass
