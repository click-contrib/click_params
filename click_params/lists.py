"""Parameter types to represent list of items."""

import click

from .base import ListParamType
from .numeric import DECIMAL, FRACTION, COMPLEX


class StringListParamType(ListParamType):
    name = 'string list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        return value.split(self._separator)


class IntListParamType(ListParamType):
    name = 'int list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, int_list = self._convert_expression_to_list(value, click.INT)
        if errors:
            self.fail(self._error_message.format(type='integers', errors=errors), param, ctx)

        return int_list


class FloatListParamType(ListParamType):
    name = 'float list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, float_list = self._convert_expression_to_list(value, click.FLOAT)
        if errors:
            self.fail(self._error_message.format(type='floating point values', errors=errors), param, ctx)

        return float_list


class DecimalListParamType(ListParamType):
    name = 'decimal list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, decimal_list = self._convert_expression_to_list(value, DECIMAL)
        if errors:
            self.fail(self._error_message.format(type='decimal values', errors=errors), param, ctx)

        return decimal_list


class FractionListParamType(ListParamType):
    name = 'fraction list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, fraction_list = self._convert_expression_to_list(value, FRACTION)
        if errors:
            self.fail(self._error_message.format(type='fraction values', errors=errors), param, ctx)

        return fraction_list


class ComplexListParamType(ListParamType):
    name = 'complex list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, complex_list = self._convert_expression_to_list(value, COMPLEX)
        if errors:
            self.fail(self._error_message.format(type='complex values', errors=errors), param, ctx)

        return complex_list
