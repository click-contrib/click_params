import click
import pytest

from click_params.base import RangeParamType


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
