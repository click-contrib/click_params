"""Module that contains parameters of type comma list"""
from typing import List, Tuple, TypeVar, Union

import click

IntClass = TypeVar('IntClass')
FloatClass = TypeVar('FloatClass')
NumClass = Union[IntClass, FloatClass]
NumList = Union[List[IntClass], List[FloatClass]]


def strip_commas(expression: str) -> str:
    """Remove heading and trailing commas in the expression and returns the new expression."""
    return expression.strip(',')


def convert_expression_to_numeric_list(expression: str, _type: NumClass) -> Tuple[List[str], NumList]:
    """
    Converts expression and returns a tuple (errors, numeric_list) where errors is a list of non-compliant items
    and numeric_list is the list of converted expression items.
    :param expression: a string expression to convert to a list.
    :param _type: the type of every element of a list.
    """
    errors = []
    numeric_list = []
    for item in expression.split(','):
        try:
            numeric_list.append(_type(item))
        except ValueError:
            errors.append(item)
    return errors, numeric_list


class StringListParamType(click.ParamType):
    name = 'string list'

    def convert(self, value, param, ctx):
        value = strip_commas(value)
        return value.split(',')


class IntListParamType(click.ParamType):
    name = 'int list'

    def convert(self, value, param, ctx):
        value = strip_commas(value)
        errors, int_list = convert_expression_to_numeric_list(value, int)
        if errors:
            self.fail(f'These items are not integers: {errors}', param, ctx)

        return int_list


class FloatListParamType(click.ParamType):
    name = 'float list'

    def convert(self, value, param, ctx):
        value = strip_commas(value)
        errors, float_list = convert_expression_to_numeric_list(value, float)
        if errors:
            self.fail(f'These items are not floating point values: {errors}', param, ctx)

        return float_list


STRING_LIST = StringListParamType()
INT_LIST = IntListParamType()
FLOAT_LIST = FloatListParamType()
