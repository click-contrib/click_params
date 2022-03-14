"""Parameter types that do not fit into other modules"""
import json
from typing import Callable, List, Sequence

import click
from validators import mac_address

from .base import ValidatorParamType, ListParamType, CustomParamType


class JsonParamType(click.ParamType):
    name = 'json'

    def __init__(self, cls: Callable = None, object_hook: Callable = None, parse_float: Callable = None,
                 parse_int: Callable = None, parse_constant: Callable = None, object_pairs_hook: Callable = None,
                 **kwargs):
        self._cls = cls
        self._object_hook = object_hook
        self._parse_float = parse_float
        self._parse_int = parse_int
        self._parse_constant = parse_constant
        self._object_pairs_hook = object_pairs_hook
        self._kwargs = kwargs

    def convert(self, value, param, ctx):
        try:
            return json.loads(value, cls=self._cls, object_hook=self._object_hook, parse_float=self._parse_float,
                              parse_int=self._parse_int, parse_constant=self._parse_constant,
                              object_pairs_hook=self._object_pairs_hook, **self._kwargs)
        except json.JSONDecodeError:
            self.fail(f'{value} is not a valid json string', param, ctx)

    def __repr__(self):
        return self.name.upper()


class MacAddressParamType(ValidatorParamType):
    name = 'mac address'

    def __init__(self):
        super().__init__(callback=mac_address)


class MacAddressListParamType(ListParamType):
    name = 'mac address list'

    def __init__(self, separator: str = ','):
        super().__init__(MAC_ADDRESS, separator=separator, name='mac addresses')


class StringListParamType(ListParamType):
    name = 'string list'

    def __init__(self, separator: str = ','):
        super().__init__(click.STRING, separator)


class UUIDListParamType(ListParamType):
    name = 'uuid list'

    def __init__(self, separator: str = ','):
        super().__init__(click.UUID, separator=separator, name='uuid')


class DateTimeListParamType(ListParamType):
    name = 'datetime list'

    def __init__(self, separator: str = ',', formats: List[str] = None):
        super().__init__(click.DateTime(formats=formats), separator=separator, name='datetimes')


class UnionParamType(CustomParamType):

    def __init__(self, param_types: Sequence[click.ParamType], name: str = None):
        self._name = name or self.name
        self._param_types = param_types
        self._error_message = '{value} is not a valid %s' % self._name

    def convert(self, value, param, ctx):
        for param_type in self._param_types:
            try:
                return param_type.convert(value, param, ctx)
            except click.BadParameter:
                continue
        self.fail(self._error_message.format(value=value))

    def __repr__(self):
        return self.name.upper()


JSON = JsonParamType()
MAC_ADDRESS = MacAddressParamType()
