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


class TestStringListParamType:
    """Tests StringListParamType"""

    def test_name_and_representation_are_correct(self):
        string_list = StringListParamType()
        name = 'string list'

        assert name == string_list.name
        assert name.upper() == repr(string_list)

    def test_should_call_strip_separator(self, mocker):
        strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
        string_list = StringListParamType()
        string_list.convert('foo,bar', None, None)

        strip_mock.assert_called_once_with('foo,bar')

    @pytest.mark.parametrize(('separator', 'input_data', 'expected_output'), [
        (',', 'foo,bar', "['foo', 'bar']\n"),
        (',', '', "['']\n"),
        (' ', '1 2 foo', "['1', '2', 'foo']\n")
    ])
    def test_should_print_correct_output(self, runner, separator, input_data, expected_output):
        @click.command()
        @click.option('-n', '--names', type=StringListParamType(separator))
        def cli(names):
            click.echo(names)

        result = runner.invoke(cli, ['-n', input_data])

        assert_equals_output(0, expected_output, result)


class TestIntListParamType:
    """Tests IntListParamType"""

    def test_name_and_representation_are_correct(self):
        int_list = IntListParamType()
        name = 'int list'

        assert name == int_list.name
        assert name.upper() == repr(int_list)

    def test_should_call_strip_separator(self, mocker):
        strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
        int_list = IntListParamType()
        int_list.convert('1,2', None, None)

        strip_mock.assert_called_once_with('1,2')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=IntListParamType())
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', '1,foo,2,2.5'])

        assert_in_output(2, "These items are not integers: ['foo', '2.5']", result)

    @pytest.mark.parametrize(('separator', 'expression'), [
        (',', '1,2'),
        (';', '1;2')
    ])
    def test_should_print_correct_output(self, runner, separator, expression):
        @click.command()
        @click.option('-n', '--notes', type=IntListParamType(separator))
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', expression])

        assert_equals_output(0, "[1, 2]\n", result)


class TestFloatListParamType:
    """Tests FloatListParamType"""

    def test_name_and_representation_are_correct(self):
        float_list = FloatListParamType()
        name = 'float list'

        assert name == float_list.name
        assert name.upper() == repr(float_list)

    def test_should_call_strip_separator(self, mocker):
        strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
        float_list = FloatListParamType()
        float_list.convert('1.2,2.5', None, None)

        strip_mock.assert_called_once_with('1.2,2.5')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=FloatListParamType())
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', '1.2,foo,2.5,bar'])

        assert_in_output(2, "These items are not floating point values: ['foo', 'bar']", result)

    @pytest.mark.parametrize(('separator', 'expression'), [
        (',', '1,.2'),
        ('; ', '1; .2')
    ])
    def test_should_print_correct_output(self, runner, separator, expression):
        @click.command()
        @click.option('-n', '--notes', type=FloatListParamType(separator))
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', expression])

        assert_equals_output(0, "[1.0, 0.2]\n", result)


class TestDecimalListParamType:
    """Tests DecimalListParamType"""

    def test_name_and_representation_are_correct(self):
        decimal_list = DecimalListParamType()
        name = 'decimal list'

        assert name == decimal_list.name
        assert name.upper() == repr(decimal_list)

    def test_should_call_strip_separator(self, mocker):
        strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
        decimal_list = DecimalListParamType()
        decimal_list.convert('1,.5', None, None)

        strip_mock.assert_called_once_with('1,.5')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=DecimalListParamType())
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', '1.2,foo,2.5,bar'])

        assert_in_output(2, "These items are not decimal values: ['foo', 'bar']", result)

    @pytest.mark.parametrize(('separator', 'expression'), [
        (',', '1,.2'),
        (' ', '1 .2')
    ])
    def test_should_print_correct_output(self, runner, separator, expression):
        @click.command()
        @click.option('-n', '--notes', type=DecimalListParamType(separator))
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', expression])

        assert_equals_output(0, "[Decimal('1'), Decimal('0.2')]\n", result)


class TestFractionListParamType:
    """Tests FractionListParamType"""

    def test_name_and_representation_are_correct(self):
        fraction_list = FractionListParamType()
        name = 'fraction list'

        assert name == fraction_list.name
        assert name.upper() == repr(fraction_list)

    def test_should_call_strip_separator(self, mocker):
        strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
        fraction_list = FractionListParamType(' ')
        fraction_list.convert('1/3 .5', None, None)

        strip_mock.assert_called_once_with('1/3 .5')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=FractionListParamType(' '))
        def cli(notes):
            click.echo(notes)

        result = runner.invoke(cli, ['-n', '1/3 foo/2 2.5 3/bar tar'])

        assert_in_output(2, "These items are not fraction values: ['foo/2', '3/bar', 'tar']", result)

    @pytest.mark.parametrize(('separator', 'expression'), [
        (',', '1/3,.5'),
        (' ', '1/3 .5')
    ])
    def test_should_print_correct_output(self, runner, separator, expression):
        @click.command()
        @click.option('-r', '--rationals', type=FractionListParamType(separator))
        def cli(rationals):
            click.echo(rationals)

        result = runner.invoke(cli, ['-r', expression])

        assert_equals_output(0, "[Fraction(1, 3), Fraction(1, 2)]\n", result)


class TestComplexListParamType:
    """Tests ComplexListParamType"""

    def test_name_and_representation_are_correct(self):
        complex_list = ComplexListParamType()
        name = 'complex list'

        assert name == complex_list.name
        assert name.upper() == repr(complex_list)

    def test_should_call_strip_separator(self, mocker):
        strip_mock = mocker.patch('click_params.lists.BaseList._strip_separator')
        complex_list = ComplexListParamType(' ')
        complex_list.convert('5 2+1j', None, None)

        strip_mock.assert_called_once_with('5 2+1j')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-c', 'complex_numbers', type=ComplexListParamType(' '))
        def cli(complex_numbers):
            click.echo(complex_numbers)

        result = runner.invoke(cli, ['-c', '5 foo 2+1j 1.4 bar'])

        assert_in_output(2, "These items are not complex values: ['foo', 'bar']", result)

    @pytest.mark.parametrize(('separator', 'expression'), [
        (',', '5,1.4,2+1j'),
        (', ', '5, 1.4, 2+1j')
    ])
    def test_should_print_correct_message(self, runner, separator, expression):
        @click.command()
        @click.option('-c', '--complex_numbers', type=ComplexListParamType(separator))
        def cli(complex_numbers):
            click.echo(complex_numbers)

        result = runner.invoke(cli, ['-c', expression])

        assert_equals_output(0, "[(5+0j), (1.4+0j), (2+1j)]\n", result)
