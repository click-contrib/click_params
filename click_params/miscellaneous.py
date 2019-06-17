"""Parameter types that do not fit into other modules"""
import json
from typing import Callable

import click
from validators import mac_address


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


class MacAddressParamType(click.ParamType):
    name = 'mac address'

    def convert(self, value, param, ctx):
        if not mac_address(value):
            self.fail(f'{value} is not a valid mac address', param, ctx)
        return value

    def __repr__(self):
        return self.name.upper()


JSON = JsonParamType()
MAC_ADDRESS = MacAddressParamType()
