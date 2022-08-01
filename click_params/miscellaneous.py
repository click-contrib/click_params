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

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(MAC_ADDRESS, separator=separator, name='mac addresses', ignore_empty=ignore_empty)


class StringListParamType(ListParamType):
    name = 'string list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(click.STRING, separator, ignore_empty=ignore_empty)


class ChoiceListParamType(ListParamType):
    name = 'choice list'

    def __init__(self, choices: Sequence[str], separator: str = ',', case_sensitive: bool = True):
        super().__init__(click.Choice(choices, case_sensitive=case_sensitive), separator)


class UUIDListParamType(ListParamType):
    name = 'uuid list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(click.UUID, separator=separator, name='uuid', ignore_empty=ignore_empty)


class DateTimeListParamType(ListParamType):
    name = 'datetime list'

    def __init__(self, separator: str = ',', formats: List[str] = None, ignore_empty: bool = False):
        super().__init__(
            click.DateTime(formats=formats), separator=separator, name='datetimes', ignore_empty=ignore_empty
        )


class FirstOf(click.ParamType):
    def __init__(self, *args: click.ParamType):
        self.params = args
        # Set name to union representation of individual params if not already set (by subclassing).
        if not getattr(self, "name", None):
            self.name = "(" + " | ".join(p.name for p in self.params) + ")"

    def convert(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Any:
        # Collect failure messages to emit later.
        fails: List[Tuple[click.ParamType, str]] = []
        for par in self.params:
            try:
                return (par, par.convert(value, param, ctx))
            except click.BadParameter as e:
                fails.append((par, str(e)))

        self.fail(
            "All possible parameters exhausted without any successful conversion:\n - "
            + "\n - ".join(
                [
                    f"{getattr(f[0], 'name', f[0].__class__.__name__).upper()}: {f[1]}"
                    for f in fails
                ]
            )
        )

    def __repr__(self):
        return self.name.upper()


JSON = JsonParamType()
MAC_ADDRESS = MacAddressParamType()
