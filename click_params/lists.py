"""Module that contains parameters types to represent list of items."""
from decimal import Decimal, DecimalException
from fractions import Fraction
from typing import List, Tuple, TypeVar

import click

NumClass = TypeVar('NumClass')  # it can be int, float, etc..
NumList = List[NumClass]


class BaseList(click.ParamType):
    """
    This class is not intended to be used directly but to serve as a basis to implement
    custom classes of item lists.
    """

    def __init__(self, separator: str = ','):
        if not isinstance(separator, str):
            raise TypeError('separator must be a string')
        self._separator = separator

    def _strip_separator(self, expression: str) -> str:
        """Returns a new expression with heading and trailing separator character removed."""
        return expression.strip(self._separator)

    def _convert_expression_to_numeric_list(self, expression: str, _type: NumClass) -> Tuple[List[str], NumList]:
        """
        Converts expression and returns a tuple (errors, numeric_list) where errors is a list of non-compliant items
        and numeric_list is the list of converted expression items.
        :param expression: a string expression to convert to a list.
        :param _type: the type of every element of a list.
        """
        errors = []
        numeric_list = []
        for item in expression.split(self._separator):
            try:
                numeric_list.append(_type(item))
            except (ValueError, ZeroDivisionError, DecimalException):
                errors.append(item)
        return errors, numeric_list


class StringListParamType(BaseList):
    name = 'string list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        return value.split(self._separator)

    def __repr__(self):
        return self.name.upper()


class IntListParamType(BaseList):
    name = 'int list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, int_list = self._convert_expression_to_numeric_list(value, int)
        if errors:
            self.fail(f'These items are not integers: {errors}', param, ctx)

        return int_list

    def __repr__(self):
        return self.name.upper()


class FloatListParamType(BaseList):
    name = 'float list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, float_list = self._convert_expression_to_numeric_list(value, float)
        if errors:
            self.fail(f'These items are not floating point values: {errors}', param, ctx)

        return float_list

    def __repr__(self):
        return self.name.upper()


class DecimalListParamType(BaseList):
    name = 'decimal list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, decimal_list = self._convert_expression_to_numeric_list(value, Decimal)
        if errors:
            self.fail(f'These items are not decimal values: {errors}', param, ctx)

        return decimal_list

    def __repr__(self):
        return self.name.upper()


class FractionListParamType(BaseList):
    name = 'fraction list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, fraction_list = self._convert_expression_to_numeric_list(value, Fraction)
        if errors:
            self.fail(f'These items are not fraction values: {errors}', param, ctx)

        return fraction_list

    def __repr__(self):
        return self.name.upper()


class ComplexListParamType(BaseList):
    name = 'complex list'

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        errors, complex_list = self._convert_expression_to_numeric_list(value, complex)
        if errors:
            self.fail(f'These items are not complex values: {errors}', param, ctx)

        return complex_list

    def __repr__(self):
        return self.name.upper()
