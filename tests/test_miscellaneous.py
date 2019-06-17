from decimal import Decimal

import click
import pytest

from click_params.miscellaneous import JSON, MAC_ADDRESS, JsonParamType

from tests.helpers import assert_in_output, assert_equals_output


@pytest.mark.parametrize(('parameter', 'name'), [
    (JSON, 'json'),
    (MAC_ADDRESS, 'mac address')
])
def test_parameter_name_and_representation_are_correct(parameter, name):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(('parameter', 'expression', 'message'), [
    (JSON, '2019-06-17', 'json string'),
    (JSON, '2f', 'json string'),
    (MAC_ADDRESS, '00:00:00:00:00', 'mac address'),
    (MAC_ADDRESS, 'foo', 'mac address')
])
def test_should_print_error_when_given_value_is_not_correct(runner, parameter, expression, message):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', expression])

    assert_in_output(2, f'{expression} is not a valid {message}', result)


@pytest.mark.parametrize(('parameter', 'expression', 'expected_output'), [
    (JSON, '2', '2\n'),
    (JSON, '"1.5"', '1.5\n'),
    (JSON, '{"b": 2, "a": "foo"}', "{'b': 2, 'a': 'foo'}\n"),
    (MAC_ADDRESS, '01:23:45:67:ab:CD', '01:23:45:67:ab:CD\n')
])
def test_should_print_correct_output_when_given_correct_value(runner, parameter, expression, expected_output):
    @click.command()
    @click.option('-j', 'json_string', type=parameter)
    def cli(json_string):
        click.echo(json_string)

    result = runner.invoke(cli, ['-j', expression])

    assert_equals_output(0, expected_output, result)


class TestJsonParamType:
    """Tests JsonParamType specific cases"""

    def test_should_call_json_loads_with_correct_arguments(self, mocker):
        loads_mock = mocker.patch('json.loads')
        json_type = JsonParamType(parse_float=Decimal, parse_int=int, parse_constant=Decimal)
        json_type.convert(2, None, None)

        loads_mock.assert_called_once_with(2, cls=None, object_hook=None, parse_float=Decimal, parse_int=int,
                                           parse_constant=Decimal, object_pairs_hook=None)
