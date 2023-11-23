from decimal import Decimal

import click
import pytest

from click_params.miscellaneous import (
    JSON,
    MAC_ADDRESS,
    ChoiceListParamType,
    DateTimeListParamType,
    FirstOf,
    JsonParamType,
    MacAddressListParamType,
    StringListParamType,
    UUIDListParamType,
)
from tests.helpers import assert_equals_output, assert_in_output


@pytest.mark.parametrize(
    ('parameter', 'name'),
    [
        (JSON, 'json'),
        (MAC_ADDRESS, 'mac address'),
        (StringListParamType(), 'string list'),
        (ChoiceListParamType(['a', 'b', 'c']), 'choice list'),
        (MacAddressListParamType(), 'mac address list'),
        (UUIDListParamType(), 'uuid list'),
        (DateTimeListParamType(), 'datetime list'),
    ],
)
def test_parameter_name_and_representation_are_correct(parameter, name):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'message'),
    [
        (JSON, '2019-06-17', 'json string'),
        (JSON, '2f', 'json string'),
        (MAC_ADDRESS, '00:00:00:00:00', 'mac address'),
        (MAC_ADDRESS, 'foo', 'mac address'),
    ],
)
def test_should_print_error_when_giving_incorrect_option_for_simple_types(runner, parameter, expression, message):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', expression])

    assert_in_output(2, f'{expression} is not a valid {message}', result)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'message'),
    [
        (
            MacAddressListParamType(' '),
            'D4:6A:6A:12:B0:75 foo 00:00:00:00:00',
            "mac addresses: ['foo', '00:00:00:00:00']",
        ),
        (UUIDListParamType(' '), 'foo a7309d0b-c858-4d54-b6e1-1c20f8c22047 142-48dr', "uuid: ['foo', '142-48dr']"),
        (DateTimeListParamType(' '), '145 2019-01-01 2019/01/01', "datetimes: ['145', '2019/01/01']"),
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
    ('parameter', 'expression', 'expected_output'),
    [
        (JSON, '2', '2\n'),
        (JSON, '"1.5"', '1.5\n'),
        (JSON, '{"b": 2, "a": "foo"}', "{'b': 2, 'a': 'foo'}\n"),
        (MAC_ADDRESS, '01:23:45:67:ab:CD', '01:23:45:67:ab:CD\n'),
    ],
)
def test_should_print_correct_output_when_giving_correct_option_for_simple_types(
    runner, parameter, expression, expected_output
):
    @click.command()
    @click.option('-j', 'json_string', type=parameter)
    def cli(json_string):
        click.echo(json_string)

    result = runner.invoke(cli, ['-j', expression])

    assert_equals_output(0, expected_output, result)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'expected_output'),
    [
        # string list
        (StringListParamType(), 'foo,bar', "['foo', 'bar']\n"),
        (StringListParamType(), '', "['']\n"),
        (StringListParamType(' '), '1 2 foo', "['1', '2', 'foo']\n"),
        # choice list
        (ChoiceListParamType(['a', 'b', 'c']), 'a,b', "['a', 'b']\n"),
        (ChoiceListParamType(['a', 'b', 'c'], separator=' '), 'a b c', "['a', 'b', 'c']\n"),
        # mac address list
        (
            MacAddressListParamType(),
            'D4:6A:6A:12:B0:75,01:23:45:67:ab:CD',
            "['D4:6A:6A:12:B0:75', '01:23:45:67:ab:CD']\n",
        ),
        (
            MacAddressListParamType(' '),
            'D4:6A:6A:12:B0:75 01:23:45:67:ab:CD',
            "['D4:6A:6A:12:B0:75', '01:23:45:67:ab:CD']\n",
        ),
        # uuid list
        (
            UUIDListParamType(),
            'a7309d0b-c858-4d54-b6e1-1c20f8c22047,bfa65f3c-e6ac-4844-8e09-e84535f8cdc5',
            "[UUID('a7309d0b-c858-4d54-b6e1-1c20f8c22047'), UUID('bfa65f3c-e6ac-4844-8e09-e84535f8cdc5')]\n",
        ),
        (
            UUIDListParamType(' '),
            'a7309d0b-c858-4d54-b6e1-1c20f8c22047 bfa65f3c-e6ac-4844-8e09-e84535f8cdc5',
            "[UUID('a7309d0b-c858-4d54-b6e1-1c20f8c22047'), UUID('bfa65f3c-e6ac-4844-8e09-e84535f8cdc5')]\n",
        ),
        # datetime list
        (
            DateTimeListParamType(),
            '2019-01-01,2019-01-01 01:00:00',
            '[datetime.datetime(2019, 1, 1, 0, 0), datetime.datetime(2019, 1, 1, 1, 0)]\n',
        ),
        (
            DateTimeListParamType(', '),
            '2019-01-01, 2019-01-01 01:00:00',
            '[datetime.datetime(2019, 1, 1, 0, 0), datetime.datetime(2019, 1, 1, 1, 0)]\n',
        ),
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
    'param_type', [StringListParamType, MacAddressListParamType, UUIDListParamType, DateTimeListParamType]
)
def test_miscellaneous_list_param_types_ignore_empty_string(param_type):
    misc_list_type = param_type(ignore_empty=True)

    assert misc_list_type.convert('', None, None) == []


def test_cli_with_multiple_similar_string_list_param_types(runner):
    @click.command()
    @click.option('-v', 'values', type=StringListParamType(','))
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', 'abc,def'])

    assert result.output == "['abc', 'def']\n"

    result = runner.invoke(cli, ['-v', 'abc,def'])

    assert result.output == "['abc', 'def']\n"


class TestJsonParamType:
    """Tests JsonParamType specific cases"""

    def test_should_call_json_loads_with_correct_arguments(self, mocker):
        loads_mock = mocker.patch('json.loads')
        json_type = JsonParamType(parse_float=Decimal, parse_int=int, parse_constant=Decimal)
        json_type.convert(2, None, None)

        loads_mock.assert_called_once_with(
            2,
            cls=None,
            object_hook=None,
            parse_float=Decimal,
            parse_int=int,
            parse_constant=Decimal,
            object_pairs_hook=None,
        )


class TestFirstOf:
    """Test class FirstOf"""

    def test_class_representation_is_correct(self):
        class CoreNumber(FirstOf):
            name = 'core number'

        assert 'CORE NUMBER' == repr(CoreNumber(click.INT, click.Choice(['all', 'half'])))
        assert 'CORE NUMBER' == repr(FirstOf(click.INT, click.Choice(['all', 'half']), name='core number'))
        assert '(INTEGER | CHOICE)' == repr(FirstOf(click.INT, click.Choice(['all', 'half'])))

    @pytest.mark.parametrize(
        ('expression', 'param_types', 'value'),
        [
            ('12', (click.INT,), 12),
            ('auto', (click.Choice(['auto', 'full']), click.INT), 'auto'),
            ('full', (click.Choice(['auto', 'full']), click.INT), 'full'),
            ('12', (click.Choice(['auto', 'full']), click.INT), 12),
            ('auto', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 'auto'),
            ('full', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 'full'),
            ('12', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 12),
            ('12.3', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 12.3),
        ],
    )
    def test_should_parse_expression_successfully(self, expression, param_types, value):
        union_type = FirstOf(*param_types)
        converted_value = union_type.convert(expression, None, None)
        assert type(value) == type(converted_value)
        assert value == converted_value

    @pytest.mark.parametrize(
        ('expression', 'param_types', 'expected_param_type'),
        [
            ('12', (click.INT,), click.INT),
            ('auto', (click.Choice(['auto', 'full']), click.INT), click.Choice(['auto', 'full'])),
            ('full', (click.Choice(['auto', 'full']), click.INT), click.Choice(['auto', 'full'])),
            ('12', (click.Choice(['auto', 'full']), click.INT), click.INT),
            ('12.3', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), click.FLOAT),
        ],
    )
    def test_should_return_correct_param_type(self, expression, param_types, expected_param_type):
        union_type = FirstOf(*param_types, return_param=True)
        (param_type, _) = union_type.convert(expression, None, None)
        assert repr(expected_param_type) == repr(param_type)

    @pytest.mark.parametrize(
        ('expression', 'param_types'),
        [
            ('auto', (click.INT,)),
            ('12.6', (click.Choice(['auto', 'full']), click.INT)),
            ('bla', (click.Choice(['auto', 'full']), click.INT, click.FLOAT)),
        ],
    )
    def test_should_parse_expression_unsuccessfully(self, expression, param_types):
        union_type = FirstOf(*param_types)
        with pytest.raises(click.BadParameter, match=r'.*\n -  '.join(p.name.upper() for p in param_types)):
            union_type.convert(expression, None, None)
