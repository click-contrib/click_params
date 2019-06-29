import click
import pytest

from click_params.lists import (
    StringListParamType, IntListParamType, FloatListParamType, DecimalListParamType,
    FractionListParamType, ComplexListParamType
)
from tests.helpers import assert_equals_output, assert_in_output


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
    strip_mock = mocker.patch('click_params.base.ListParamType._strip_separator')
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
