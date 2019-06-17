"""Numeric parameter types"""
from decimal import Decimal, DecimalException
from fractions import Fraction
from typing import Tuple, Union

import click

from .annotations import Error, NumClass
from .base import RangeParamType


class NumericParamType(click.ParamType):
    def __init__(self, _type: NumClass, str_type: str, errors: Union[Error, Tuple[Error]]):
        self._type = _type
        self._errors = errors
        self._error_message = '{value} is not a valid %s' % str_type

    def convert(self, value, param, ctx):
        try:
            return self._type(value)
        except self._errors:
            self.fail(self._error_message.format(value=value))

    def __repr__(self):
        return self.name.upper()


class DecimalParamType(NumericParamType):
    name = 'decimal'

    def __init__(self):
        super().__init__(_type=Decimal, str_type='decimal', errors=DecimalException)


class DecimalRange(RangeParamType):
    name = 'decimal range'

    def __init__(self, minimum: Decimal = None, maximum: Decimal = None, clamp: bool = False):
        super().__init__(DecimalParamType(), minimum, maximum, clamp)


class FractionParamType(NumericParamType):
    name = 'fraction'

    def __init__(self):
        super().__init__(_type=Fraction, str_type='fraction', errors=(ValueError, ZeroDivisionError))


class FractionRange(RangeParamType):
    name = 'fraction range'

    def __init__(self, minimum: Fraction, maximum: Fraction, clamp: bool = False):
        super().__init__(FractionParamType(), minimum, maximum, clamp)


class ComplexParamType(NumericParamType):
    name = 'complex'

    def __init__(self):
        super().__init__(_type=complex, str_type='complex', errors=ValueError)


DECIMAL = DecimalParamType()
FRACTION = FractionParamType()
COMPLEX = ComplexParamType()
