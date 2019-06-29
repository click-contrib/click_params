from decimal import Decimal
from fractions import Fraction

import click
import pytest

from click_params.numeric import DECIMAL, FRACTION, COMPLEX, DecimalRange, FractionRange
from tests.helpers import assert_in_output, assert_equals_output


@pytest.mark.parametrize(('name', 'parameter'), [
    ('decimal', DECIMAL),
    ('fraction', FRACTION),
    ('complex', COMPLEX),
])
def test_parameter_name_and_representation_are_correct_for_simple_types(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(('name', 'representation', 'parameter'), [
    ('decimal range', f'DecimalRange({repr(Decimal(0.1))}, {repr(Decimal(0.8))})',
     DecimalRange(Decimal(0.1), Decimal(0.8))),
    ('fraction range', f'FractionRange({repr(Fraction(0.1))}, {repr(Fraction(0.8))})',
     FractionRange(Fraction(0.1), Fraction(0.8)))
])
def test_parameter_name_and_representation_are_correct_for_range_types(name, representation, parameter):
    assert name == parameter.name
    assert representation == repr(parameter)


@pytest.mark.parametrize(('parameter', 'str_type', 'param_value'), [
    (DECIMAL, 'decimal', 'foo'),
    (FRACTION, 'fraction', 'foo'),
    (FRACTION, 'fraction', '2/0'),
    (COMPLEX, 'complex', 'foo'),
])
def test_should_print_error_when_giving_incorrect_option(runner, parameter, str_type, param_value):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_in_output(2, f'{param_value} is not a valid {str_type}', result)


@pytest.mark.parametrize(('parameter', 'value', 'message'), [
    (DecimalRange(Decimal('0.1'), Decimal('0.8')), '0.01', '0.01 is not in the valid range of 0.1 to 0.8.'),
    (FractionRange(Fraction('0.1'), Fraction('0.8')), '0.01', '1/100 is not in the valid range of 1/10 to 4/5.')
])
def test_should_print_error_when_giving_value_is_out_of_limits(runner, parameter, value, message):
    @click.command()
    @click.option('-c', 'count', type=parameter)
    def cli(count):
        click.echo(count)

    result = runner.invoke(cli, ['-c', value])

    assert_in_output(2, message, result)


@pytest.mark.parametrize(('parameter', 'param_value', 'expected_output'), [
    (DECIMAL, '5.0', '5.0\n'),
    (FRACTION, '5.0', '5\n'),
    (FRACTION, '1/3', '1/3\n'),
    (COMPLEX, '5', '(5+0j)\n'),
    (COMPLEX, '1+2j', '(1+2j)\n'),
    (DecimalRange(Decimal('0.1'), Decimal('0.8')), '0.4', '0.4\n'),
    (FractionRange(Fraction('0.1'), Fraction('0.8')), '0.4', '2/5\n')
])
def test_should_print_correct_output_when_giving_correct_option(runner, parameter, param_value, expected_output):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_equals_output(0, expected_output, result)
