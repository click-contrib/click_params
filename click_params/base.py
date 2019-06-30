"""Base classes to implement various parameter types"""
from typing import Union, Tuple, Callable, List, Any

import click

from .annotations import Min, Max, Error


class BaseParamType(click.ParamType):
    def __init__(self, _type: Any, errors: Union[Error, Tuple[Error]], name: str = None):
        self._type = _type
        self._errors = errors
        self._name = name or self.name
        self._error_message = '{value} is not a valid %s' % self._name

    def convert(self, value, param, ctx):
        try:
            return self._type(value)
        except self._errors:
            self.fail(self._error_message.format(value=value), param, ctx)

    def __repr__(self):
        return self.name.upper()


class ValidatorParamType(click.ParamType):
    """This class is intended to be inherit by classes using validators functions."""

    def __init__(self, callback: Callable, name: str = None):
        self._callback = callback
        self._name = name or self.name
        self._error_message = '{value} is not a valid %s' % self._name

    def convert(self, value, param, ctx):
        if not self._callback(value):
            self.fail(self._error_message.format(value=value), param, ctx)
        return value

    def __repr__(self):
        return self.name.upper()


class RangeParamType(click.ParamType):

    def __init__(self, param_type: click.ParamType, minimum: Min = None, maximum: Max = None, clamp: bool = False):
        self._minimum = minimum
        self._maximum = maximum
        self._clamp = clamp
        self._param_type = param_type

    def convert(self, value, param, ctx):
        converted_value = self._param_type.convert(value, param, ctx)
        inferior_to_minimum = self._minimum is not None and converted_value < self._minimum
        superior_to_maximum = self._maximum is not None and converted_value > self._maximum

        if self._clamp:
            if inferior_to_minimum:
                return self._minimum
            if superior_to_maximum:
                return self._maximum

        if inferior_to_minimum or superior_to_maximum:
            if self._minimum is None:
                self.fail(f'{converted_value} is bigger than the maximum valid value {self._maximum}.', param, ctx)
            elif self._maximum is None:
                self.fail(f'{converted_value} is smaller than the minimum valid value {self._minimum}.', param, ctx)
            else:
                self.fail(f'{converted_value} is not in the valid range of {self._minimum} to {self._maximum}.',
                          param, ctx)
        return converted_value

    def __repr__(self):
        parts = self.name.split(' ')
        titles = [part.title() for part in parts]
        new_name = ''.join(titles)
        return f'{new_name}({repr(self._minimum)}, {repr(self._maximum)})'


class ListParamType(click.ParamType):
    """
    This class is not intended to be used directly but to serve as a basis to implement
    custom classes of item lists.
    """

    def __init__(self, separator: str = ','):
        if not isinstance(separator, str):
            raise TypeError('separator must be a string')
        self._separator = separator
        self._error_message = 'These items are not {type}: {errors}'

    def _strip_separator(self, expression: str) -> str:
        """Returns a new expression with heading and trailing separator character removed."""
        return expression.strip(self._separator)

    def _convert_expression_to_list(self, expression: str, param_type: click.ParamType) -> Tuple[List[str], Any]:
        """
        Converts expression and returns a tuple (errors, converted_items) where errors is a list of non-compliant items
        and converted_items is the list of converted expression items.
        :param expression: a string expression to convert to a list.
        :param param_type: the click param type used to convert items.
        """
        errors = []
        converted_items = []
        for item in expression.split(self._separator):
            try:
                converted_items.append(param_type.convert(item, None, None))
            except click.BadParameter:
                errors.append(item)
        return errors, converted_items

    def __repr__(self):
        return self.name.upper()
