from fractions import Fraction

import click
import pytest
from validators.utils import validator

from click_params.base import RangeParamType, BaseParamType, ValidatorParamType, ListParamType, UnionParamType
from click_params.numeric import DECIMAL, FRACTION, COMPLEX


class IntType(BaseParamType):
    """We use this custom type to test BaseParamType"""
    name = 'integer'

    def __init__(self):
        super().__init__(_type=int, errors=ValueError)


class TestBaseParamType:
    """Tests BaseParamType"""

    def test_class_representation_is_correct(self):
        assert 'INTEGER' == repr(IntType())

    @pytest.mark.parametrize('value', ['foo', '4.5'])
    def test_should_raise_error_when_value_has_incorrect_type(self, value):
        with pytest.raises(click.BadParameter) as exc_info:
            IntType().convert(value, None, None)

        assert f'{value} is not a valid integer' == str(exc_info.value)

    def test_should_return_converted_value_when_giving_correct_input(self):
        str_value = '4'
        try:
            value = IntType().convert(str_value, None, None)
            assert int(str_value) == value
        except click.BadParameter:
            pytest.fail(f'Unexpected fail with value: {str_value}')


@validator
def even(value):
    """Simple validator defined for test purpose"""
    return not (int(value) % 2)


class EvenType(ValidatorParamType):
    name = 'even'

    def __init__(self):
        super().__init__(even, 'even number')


class TestValidatorParamType:
    """Tests class ValidatorParamType"""

    def test_class_representation_is_correct(self):
        assert 'EVEN' == repr(EvenType())

    @pytest.mark.parametrize('value', ['5', '13'])
    def test_should_raise_error_when_value_is_incorrect(self, value):
        with pytest.raises(click.BadParameter) as exc_info:
            EvenType().convert(value, None, None)

        assert f'{value} is not a valid even number' == str(exc_info.value)

    @pytest.mark.parametrize('value', ['0', '4'])
    def test_should_return_value_when_giving_corrected_value(self, value):
        try:
            assert value == EvenType().convert(value, None, None)
        except click.BadParameter:
            pytest.fail(f'Unexpected error with value {value}')


class IntRange(RangeParamType):
    """This class will be used to test the correctness of RangeParamType"""
    name = 'int range'

    def __init__(self, minimum: int = None, maximum: int = None, clamp: bool = False):
        super().__init__(click.INT, minimum, maximum, clamp)


class TestRangeParamType:
    """Tests class RangeParamType"""

    def test_class_representation_is_correct(self):
        assert 'IntRange(4, 6)' == repr(IntRange(4, 6))

    # we test clamp parameter usage

    @pytest.mark.parametrize(('minimum', 'maximum', 'given_input', 'expected_value'), [
        (None, 5, '-1', -1),
        (None, 5, '8', 5),
        (5, 10, '8', 8),
        (5, 10, '2', 5),
        (5, None, '8', 8)
    ])
    def test_should_return_correct_value_when_setting_clamp_to_true(self, minimum, maximum, given_input,
                                                                    expected_value):
        int_range = IntRange(minimum, maximum, True)
        assert expected_value == int_range.convert(given_input, None, None)

    @pytest.mark.parametrize(('minimum', 'maximum', 'value'), [
        (5, 10, '6'),
        (5, 10, '5'),
        (5, 10, '10')
    ])
    def test_should_return_correct_value_when_setting_clamp_to_false(self, minimum, maximum, value):
        int_range = IntRange(minimum, maximum)
        assert int(value) == int_range.convert(value, None, None)

    @pytest.mark.parametrize(('minimum', 'maximum', 'given_input', 'message'), [
        (5, None, '4', '4 is smaller than the minimum valid value 5.'),
        (None, 10, '11', '11 is bigger than the maximum valid value 10.'),
        (5, 10, '4', '4 is not in the valid range of 5 to 10.'),
        (5, 10, '11', '11 is not in the valid range of 5 to 10.')
    ])
    def test_should_raise_error_when_giving_values_outside_limits(self, minimum, maximum, given_input, message):
        with pytest.raises(click.BadParameter) as exc_info:
            int_range = IntRange(minimum, maximum, False)
            int_range.convert(given_input, None, None)

        assert message == str(exc_info.value)


class TestListParamType:
    """Tests class ListParamType"""

    @pytest.mark.parametrize('separator', [2, 2.5])
    def test_should_raise_error_when_instantiating_with_non_string_parameter(self, separator):
        with pytest.raises(TypeError) as exc_info:
            # noinspection PyTypeChecker
            ListParamType(click.INT, separator)

        assert 'separator must be a string' == str(exc_info.value)

    @pytest.mark.parametrize('separator', [
        {},  # default separator should be used i.e ","
        {'separator': ' '},
        {'separator': ';'}
    ])
    def test_should_not_raise_error_when_instantiating_with_a_string(self, separator):
        try:
            ListParamType(click.INT, **separator)
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
        base_list = ListParamType(click.INT, separator)
        assert f'1{separator}2' == base_list._strip_separator(expression)

    @pytest.mark.parametrize(('expression', 'param_type', 'name', 'errors'), [
        ('1,foo,2', click.INT, 'integers', ['foo']),
        ('1.4,bar,2.8', click.FLOAT, 'floating point values', ['bar']),
        ('1,.2,foo', DECIMAL, 'decimal values', ['foo']),
        ('2,1/0', FRACTION, 'fraction values', ['1/0']),
    ])
    def test_should_raise_error_when_items_are_incorrect(self, expression, param_type, name, errors):
        base_list = ListParamType(param_type, name=name)

        with pytest.raises(click.BadParameter) as exc_info:
            base_list.convert(expression, None, None)

        assert f'These items are not {name}: {errors}' == str(exc_info.value)

    @pytest.mark.parametrize(('expression', 'param_type', 'name', 'values'), [
        ('1,2,3', click.INT, 'integers', [1, 2, 3]),
        ('1,2.5', click.FLOAT, 'floating point values', [1.0, 2.5]),
        ('2', FRACTION, 'fraction values', [Fraction(2, 1)]),
        ('5,1.4,2+1j', COMPLEX, 'complex values', [complex(5, 0), complex(1.4, 0), complex(2, 1)])
    ])
    def test_should_return_correct_items_when_giving_correct_expression(self, expression, param_type, name, values):
        # noinspection PyTypeChecker
        base_list = ListParamType(param_type, name=name)
        assert values == base_list.convert(expression, None, None)


class TestUnionParamType:
    """Test class UnionParamType"""

    @pytest.mark.parametrize(('expression', 'param_types', 'value'), [
        ('12', (click.INT,), 12),
        ('auto', (click.Choice(['auto', 'full']), click.INT), 'auto'),
        ('full', (click.Choice(['auto', 'full']), click.INT), 'full'),
        ('12', (click.Choice(['auto', 'full']), click.INT), 12),
        ('auto', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 'auto'),
        ('full', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 'full'),
        ('12', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 12),
        ('12.3', (click.Choice(['auto', 'full']), click.INT, click.FLOAT), 12.3)
    ])
    def test_parse_expression_successfully(self, expression, param_types, value):
        union_type = UnionParamType(param_types=param_types)
        converted_value = union_type.convert(expression, None, None)
        assert type(value) == type(converted_value)
        assert value == converted_value

    @pytest.mark.parametrize(('expression', 'param_types'), [
        ('auto', (click.INT,)),
        ('12.6', (click.Choice(['auto', 'full']), click.INT)),
        ('bla', (click.Choice(['auto', 'full']), click.INT, click.FLOAT)),
    ])
    def test_parse_expression_unsuccessfully(self, expression, param_types):
        union_type = UnionParamType(param_types=param_types)
        with pytest.raises(click.BadParameter):
            union_type.convert(expression, None, None)
