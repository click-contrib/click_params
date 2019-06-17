from decimal import Decimal
from fractions import Fraction

import click
import pytest

from click_params.lists import (
    BaseList, StringListParamType, IntListParamType, FloatListParamType, DecimalListParamType,
    FractionListParamType, ComplexListParamType
)
from tests.helpers import assert_equals_output, assert_in_output


class TestBaseList:
    """Tests class BaseList"""

    @pytest.mark.parametrize('separator', [2, 2.5])
    def test_should_raise_error_when_instantiating_with_non_string_parameter(self, separator):
        with pytest.raises(TypeError) as exc_info:
            # noinspection PyTypeChecker
            BaseList(separator)

        assert 'separator must be a string' == str(exc_info.value)

    @pytest.mark.parametrize('separator', [
        {},  # default separator should be used i.e ","
        {'separator': ' '},
        {'separator': ';'}
    ])
    def test_should_not_raise_error_when_instantiating_with_a_string(self, separator):
        try:
            BaseList(**separator)
        except TypeError:
            pytest.fail(f'unexpected fail with separator = {separator}')

    # we test method _strip_separator

    @pytest.mark.parametrize(('separator', 'expression'), [
        (',', '1,2'),
        (',', ',1,2,'),
        (';', ';1;2'),
        (' ', '1 2 '),
    ])
    def test_should_return_correct_expression(self, separator, expression):
        base_list = BaseList(separator)
        assert f'1{separator}2' == base_list._strip_separator(expression)

    # we test method _convert_expression_to_numeric_list

    @pytest.mark.parametrize(('expression', '_type', 'expected_errors', 'expected_num_list'), [
        ('1,2,3', int, [], [1, 2, 3]),
        ('1,2.5', float, [], [1.0, 2.5]),
        ('', int, [''], []),
        ('', float, [''], []),
        ('1,foo,2', int, ['foo'], [1, 2]),
        ('1.4,bar,2.8', float, ['bar'], [1.4, 2.8]),
        ('1,.2,foo', Decimal, ['foo'], [Decimal('1'), Decimal('0.2')]),
        ('2,1/0', Fraction, ['1/0'], [Fraction(2, 1)]),
        ('5,1.4,foo,2+1j', complex, ['foo'], [complex(5, 0), complex(1.4, 0), complex(2, 1)])
    ])
    def test_should_return_correct_list_of_tuples(self, expression, _type, expected_errors, expected_num_list):
        base_list = BaseList()
        errors, numeric_list = base_list._convert_expression_to_numeric_list(expression, _type)

        assert expected_errors == errors
        assert expected_num_list == numeric_list


@pytest.mark.parametrize(('name', 'parameter'), [
    ('string list', StringListParamType()),
    ('int list', IntListParamType()),
    ('float list', FloatListParamType()),
    ('decimal list', DecimalListParamType()),
    ('fraction list', FractionListParamType()),
    ('complex list', ComplexListParamType())
])
def test_parameter_name_and_representation_are_correct(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(('parameter', 'expression'), [
    (StringListParamType(), 'foo,bar'),
    (IntListParamType(), '1,2'),
    (FloatListParamType(), '1.2,2.5'),
    (DecimalListParamType(), '1,.5'),
    (FractionListParamType(' '), '1/3 .5'),
    (ComplexListParamType(' '), '5 2+1j')
])
def test_parameter_convert_method_calls_strip_separator(mocker, parameter, expression):
    strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
    parameter.convert(expression, None, None)

    strip_mock.assert_called_once_with(expression)


@pytest.mark.parametrize(('parameter', 'expression', 'message'), [
    (IntListParamType(), '1,foo,2,2.5', "integers: ['foo', '2.5']"),
    (FloatListParamType(), '1.2,foo,2.5,bar', "floating point values: ['foo', 'bar']"),
    (DecimalListParamType(), '1.2,foo,2.5,bar', "decimal values: ['foo', 'bar']"),
    (FractionListParamType(' '), '1/3 foo/2 2.5 3/bar tar', "fraction values: ['foo/2', '3/bar', 'tar']"),
    (ComplexListParamType(' '), '5 foo 2+1j 1.4 bar', "complex values: ['foo', 'bar']")
])
def test_should_print_error_when_giving_wrong_value(runner, parameter, expression, message):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_in_output(2, f'These items are not {message}', result)


@pytest.mark.parametrize(('parameter', 'expression', 'expected_output'), [
    # string list
    (StringListParamType(), 'foo,bar', "['foo', 'bar']\n"),
    (StringListParamType(), '', "['']\n"),
    (StringListParamType(' '), '1 2 foo', "['1', '2', 'foo']\n"),
    # int list
    (IntListParamType(), '1,2', '[1, 2]\n'),
    (IntListParamType(';'), '1;2', '[1, 2]\n'),
    # float list
    (FloatListParamType(), '1,.2', '[1.0, 0.2]\n'),
    (FloatListParamType('; '), '1; .2', '[1.0, 0.2]\n'),
    # decimal list
    (DecimalListParamType(), '1,.2', "[Decimal('1'), Decimal('0.2')]\n"),
    (DecimalListParamType(' '), '1 .2', "[Decimal('1'), Decimal('0.2')]\n"),
    # fraction list
    (FractionListParamType(), '1/3,.5', '[Fraction(1, 3), Fraction(1, 2)]\n'),
    (FractionListParamType(' '), '1/3 .5', '[Fraction(1, 3), Fraction(1, 2)]\n'),
    # complex list
    (ComplexListParamType(), '5,1.4,2+1j', '[(5+0j), (1.4+0j), (2+1j)]\n'),
    (ComplexListParamType(', '), '5, 1.4, 2+1j', '[(5+0j), (1.4+0j), (2+1j)]\n')
])
def test_should_print_correct_output_when_giving_correct_value(runner, parameter, expression, expected_output):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_equals_output(0, expected_output, result)
