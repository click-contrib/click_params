"""Numeric parameter types"""
from decimal import Decimal, DecimalException
from fractions import Fraction

from .base import RangeParamType, BaseParamType


class DecimalParamType(BaseParamType):
    name = 'decimal'

    def __init__(self):
        super().__init__(_type=Decimal, errors=DecimalException)


class DecimalRange(RangeParamType):
    name = 'decimal range'

    def __init__(self, minimum: Decimal = None, maximum: Decimal = None, clamp: bool = False):
        super().__init__(DecimalParamType(), minimum, maximum, clamp)


class FractionParamType(BaseParamType):
    name = 'fraction'

    def __init__(self):
        super().__init__(_type=Fraction, errors=(ValueError, ZeroDivisionError))


class FractionRange(RangeParamType):
    name = 'fraction range'

    def __init__(self, minimum: Fraction = None, maximum: Fraction = None, clamp: bool = False):
        super().__init__(FractionParamType(), minimum, maximum, clamp)


class ComplexParamType(BaseParamType):
    name = 'complex'

    def __init__(self):
        super().__init__(_type=complex, errors=ValueError)


DECIMAL = DecimalParamType()
FRACTION = FractionParamType()
COMPLEX = ComplexParamType()
