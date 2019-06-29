"""Parameter types to represent list of items."""
from decimal import Decimal
from fractions import Fraction

from .base import ListParamType


class StringListParamType(ListParamType):
    name = 'string list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        return value.split(self._separator)


class IntListParamType(ListParamType):
    name = 'int list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, int_list = self._convert_expression_to_numeric_list(value, int)
        if errors:
            self.fail(f'These items are not integers: {errors}', param, ctx)

        return int_list


class FloatListParamType(ListParamType):
    name = 'float list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, float_list = self._convert_expression_to_numeric_list(value, float)
        if errors:
            self.fail(f'These items are not floating point values: {errors}', param, ctx)

        return float_list


class DecimalListParamType(ListParamType):
    name = 'decimal list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, decimal_list = self._convert_expression_to_numeric_list(value, Decimal)
        if errors:
            self.fail(f'These items are not decimal values: {errors}', param, ctx)

        return decimal_list


class FractionListParamType(ListParamType):
    name = 'fraction list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, fraction_list = self._convert_expression_to_numeric_list(value, Fraction)
        if errors:
            self.fail(f'These items are not fraction values: {errors}', param, ctx)

        return fraction_list


class ComplexListParamType(ListParamType):
    name = 'complex list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, complex_list = self._convert_expression_to_numeric_list(value, complex)
        if errors:
            self.fail(f'These items are not complex values: {errors}', param, ctx)

        return complex_list
