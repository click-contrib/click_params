import click
import pytest

from click_params.commas_list import (
    strip_commas, convert_expression_to_numeric_list, StringListParamType, STRING_LIST, IntListParamType, INT_LIST,
    FloatListParamType, FLOAT_LIST
)
from tests.helpers import assert_equals_output, assert_in_output


class TestStripCommas:
    """Tests function strip_commas"""

    @pytest.mark.parametrize('expression', [
        ',1,2',
        '1,2',
        '1,2,',
        ',1,2,'
    ])
    def test_should_return_correct_expression(self, expression):
        assert '1,2' == strip_commas(expression)


class TestConvertExpressionToNumericList:
    """Tests function convert_expression_to_numeric_list"""

    @pytest.mark.parametrize(('expression', '_type', 'expected_errors', 'expected_num_list'), [
        ('1,2,3', int, [], [1, 2, 3]),
        ('1,2.5', float, [], [1.0, 2.5]),
        ('', int, [''], []),
        ('', float, [''], []),
        ('1,foo,2', int, ['foo'], [1, 2]),
        ('1.4,bar,2.8', float, ['bar'], [1.4, 2.8])
    ])
    def test_should_return_correct_tuple_of_lists(self, expression, _type, expected_errors, expected_num_list):
        errors, numeric_list = convert_expression_to_numeric_list(expression, _type)

        assert expected_errors == errors
        assert expected_num_list == numeric_list


class TestStringListParamType:
    """Tests StringListParamType"""

    def test_should_call_strip_commas(self, mocker):
        commas_mock = mocker.patch('click_params.commas_list.strip_commas')
        string_list = StringListParamType()
        string_list.convert('foo,bar', None, None)

        commas_mock.assert_called_once_with('foo,bar')

    @pytest.mark.parametrize(('input_data', 'expected_output'), [
        ('foo,bar', "['foo', 'bar']\n"),
        ('', "['']\n")
    ])
    def test_should_print_correct_output(self, runner, input_data, expected_output):
        @click.command()
        @click.option('-n', '--names', type=STRING_LIST)
        def hello(names):
            click.echo(names)

        result = runner.invoke(hello, ['-n', input_data])

        assert_equals_output(0, expected_output, result)


class TestIntListParamType:
    """Tests IntListParamType"""

    def test_should_call_strip_commas(self, mocker):
        commas_mock = mocker.patch('click_params.commas_list.strip_commas')
        int_list = IntListParamType()
        int_list.convert('1,2', None, None)

        commas_mock.assert_called_once_with('1,2')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=INT_LIST)
        def hello(notes):
            click.echo(notes)

        result = runner.invoke(hello, ['-n', '1,foo,2,2.5'])

        assert_in_output(2, "These items are not integers: ['foo', '2.5']", result)

    def test_should_print_correct_output(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=INT_LIST)
        def hello(notes):
            click.echo(notes)

        result = runner.invoke(hello, ['-n', '1,2'])

        assert_equals_output(0, "[1, 2]\n", result)


class TestFloatListParamType:
    """Tests FloatListParamType"""

    def test_should_call_strip_commas(self, mocker):
        commas_mock = mocker.patch('click_params.commas_list.strip_commas')
        float_list = FloatListParamType()
        float_list.convert('1.2,2.5', None, None)

        commas_mock.assert_called_once_with('1.2,2.5')

    def test_should_print_error(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=FLOAT_LIST)
        def hello(notes):
            click.echo(notes)

        result = runner.invoke(hello, ['-n', '1.2,foo,2.5,bar'])

        assert_in_output(2, "These items are not floating point values: ['foo', 'bar']", result)

    def test_should_print_correct_output(self, runner):
        @click.command()
        @click.option('-n', '--notes', type=FLOAT_LIST)
        def hello(notes):
            click.echo(notes)

        result = runner.invoke(hello, ['-n', '1,.2'])

        assert_equals_output(0, "[1.0, 0.2]\n", result)
