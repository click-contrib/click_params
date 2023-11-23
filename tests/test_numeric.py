from decimal import Decimal
from fractions import Fraction

import click
import pytest

from click_params.numeric import (
    COMPLEX,
    DECIMAL,
    FRACTION,
    ComplexListParamType,
    DecimalListParamType,
    DecimalRange,
    FloatListParamType,
    FractionListParamType,
    FractionRange,
    IntListParamType,
)
from tests.helpers import assert_equals_output, assert_in_output


@pytest.mark.parametrize(
    ('name', 'parameter'),
    [
        ('decimal', DECIMAL),
        ('fraction', FRACTION),
        ('complex', COMPLEX),
        ('int list', IntListParamType()),
        ('float list', FloatListParamType()),
        ('decimal list', DecimalListParamType()),
        ('fraction list', FractionListParamType()),
        ('complex list', ComplexListParamType()),
    ],
)
def test_parameter_name_and_representation_are_correct_for_simple_and_list_types(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(
    ('name', 'representation', 'parameter'),
    [
        (
            'decimal range',
            f'DecimalRange({repr(Decimal(0.1))}, {repr(Decimal(0.8))})',
            DecimalRange(Decimal(0.1), Decimal(0.8)),
        ),
        (
            'fraction range',
            f'FractionRange({repr(Fraction(0.1))}, {repr(Fraction(0.8))})',
            FractionRange(Fraction(0.1), Fraction(0.8)),
        ),
    ],
)
def test_parameter_name_and_representation_are_correct_for_range_types(name, representation, parameter):
    assert name == parameter.name
    assert representation == repr(parameter)


@pytest.mark.parametrize(
    ('parameter', 'str_type', 'param_value'),
    [
        (DECIMAL, 'decimal', 'foo'),
        (FRACTION, 'fraction', 'foo'),
        (FRACTION, 'fraction', '2/0'),
        (COMPLEX, 'complex', 'foo'),
    ],
)
def test_should_print_error_when_giving_incorrect_option_for_simple_types(runner, parameter, str_type, param_value):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_in_output(2, f'{param_value} is not a valid {str_type}', result)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'message'),
    [
        (IntListParamType(), '1,foo,2,2.5', "integers: ['foo', '2.5']"),
        (FloatListParamType(), '1.2,foo,2.5,bar', "floating point values: ['foo', 'bar']"),
        (DecimalListParamType(), '1.2,foo,2.5,bar', "decimal values: ['foo', 'bar']"),
        (FractionListParamType(' '), '1/3 foo/2 2.5 3/bar tar', "fractions: ['foo/2', '3/bar', 'tar']"),
        (ComplexListParamType(' '), '5 foo 2+1j 1.4 bar', "complex values: ['foo', 'bar']"),
    ],
)
def test_should_print_error_when_giving_incorrect_option_for_list_types(runner, parameter, expression, message):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_in_output(2, f'These items are not {message}', result)


@pytest.mark.parametrize(
    ('parameter', 'value', 'message'),
    [
        (DecimalRange(Decimal('0.1'), Decimal('0.8')), '0.01', '0.01 is not in the valid range of 0.1 to 0.8.'),
        (FractionRange(Fraction('0.1'), Fraction('0.8')), '0.01', '1/100 is not in the valid range of 1/10 to 4/5.'),
    ],
)
def test_should_print_error_when_giving_value_is_out_of_limits(runner, parameter, value, message):
    @click.command()
    @click.option('-c', 'count', type=parameter)
    def cli(count):
        click.echo(count)

    result = runner.invoke(cli, ['-c', value])

    assert_in_output(2, message, result)


@pytest.mark.parametrize(
    ('parameter', 'param_value', 'expected_output'),
    [
        (DECIMAL, '5.0', '5.0\n'),
        (FRACTION, '5.0', '5\n'),
        (FRACTION, '1/3', '1/3\n'),
        (COMPLEX, '5', '(5+0j)\n'),
        (COMPLEX, '1+2j', '(1+2j)\n'),
        (DecimalRange(Decimal('0.1'), Decimal('0.8')), '0.4', '0.4\n'),
        (FractionRange(Fraction('0.1'), Fraction('0.8')), '0.4', '2/5\n'),
    ],
)
def test_should_print_correct_output_when_giving_correct_option_for_simple_and_range_types(
    runner, parameter, param_value, expected_output
):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_equals_output(0, expected_output, result)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'expected_output'),
    [
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
        (ComplexListParamType(', '), '5, 1.4, 2+1j', '[(5+0j), (1.4+0j), (2+1j)]\n'),
    ],
)
def test_should_print_correct_output_when_giving_correct_option_for_list_types(
    runner, parameter, expression, expected_output
):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_equals_output(0, expected_output, result)


@pytest.mark.parametrize(
    'param_type',
    [IntListParamType, FloatListParamType, ComplexListParamType, DecimalListParamType, FractionListParamType],
)
def test_numeric_list_param_types_ignore_empty_string(param_type):
    numeric_list_type = param_type(ignore_empty=True)

    assert numeric_list_type.convert('', None, None) == []
