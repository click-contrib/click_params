"""Numeric parameter types"""
from decimal import Decimal, DecimalException
from fractions import Fraction

import click

from .base import BaseParamType, RangeParamType, ListParamType


class DecimalParamType(BaseParamType):
    name = 'decimal'

    def __init__(self):
        super().__init__(_type=Decimal, errors=DecimalException)


class DecimalRange(RangeParamType):
    name = 'decimal range'

    def __init__(self, minimum: Decimal = None, maximum: Decimal = None, clamp: bool = False):
        super().__init__(DECIMAL, minimum, maximum, clamp)


class DecimalListParamType(ListParamType):
    name = 'decimal list'

    def __init__(self, separator: str = ','):
        super().__init__(DECIMAL, separator=separator, name='decimal values')


class FractionParamType(BaseParamType):
    name = 'fraction'

    def __init__(self):
        super().__init__(_type=Fraction, errors=(ValueError, ZeroDivisionError))


class FractionRange(RangeParamType):
    name = 'fraction range'

    def __init__(self, minimum: Fraction = None, maximum: Fraction = None, clamp: bool = False):
        super().__init__(FRACTION, minimum, maximum, clamp)


class FractionListParamType(ListParamType):
    name = 'fraction list'

    def __init__(self, separator: str = ','):
        super().__init__(FRACTION, separator=separator, name='fraction values')


class ComplexParamType(BaseParamType):
    name = 'complex'

    def __init__(self):
        super().__init__(_type=complex, errors=ValueError)


class ComplexListParamType(ListParamType):
    name = 'complex list'

    def __init__(self, separator: str = ','):
        super().__init__(COMPLEX, separator=separator, name='complex values')


class IntListParamType(ListParamType):
    name = 'int list'

    def __init__(self, separator: str = ','):
        super().__init__(click.INT, separator=separator, name='integers')


class FloatListParamType(ListParamType):
    name = 'float list'

    def __init__(self, separator: str = ','):
        super().__init__(click.FLOAT, separator=separator, name='floating point values')


DECIMAL = DecimalParamType()
FRACTION = FractionParamType()
COMPLEX = ComplexParamType()
