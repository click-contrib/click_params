import pytest
from click.testing import CliRunner, Result

from click_params.test_utils import assert_equals_output, assert_in_output, assert_list_in_output


@pytest.mark.parametrize('callback', [assert_in_output, assert_equals_output, assert_list_in_output])
def test_should_raise_error_when_exit_code_is_different_from_the_result_one(callback):
    result = Result(CliRunner(), b'', b'', '', 1, None)
    with pytest.raises(AssertionError):
        callback(0, '', result)


@pytest.mark.parametrize(
    ('callback', 'data'),
    [
        (assert_in_output, 'bar'),
        (assert_equals_output, 'bar'),
        (assert_list_in_output, ['bar']),
        (assert_list_in_output, ['f', 'a']),
    ],
)
def test_should_raise_error_when_expected_output_not_in_result_output(callback, data):
    result = Result(CliRunner(), b'foo', b'', '', 0, None)
    with pytest.raises(AssertionError):
        callback(0, data, result)


@pytest.mark.parametrize(
    ('callback', 'data'),
    [(assert_in_output, 'bar'), (assert_equals_output, 'foobar'), (assert_list_in_output, ['fo', 'ba'])],
)
def test_should_not_raise_error_when_exit_code_and_output_are_corresponding_to_result_properties(callback, data):
    result = Result(CliRunner(), b'foobar', b'', '', 0, None)
    try:
        callback(0, data, result)
    except AssertionError:
        pytest.fail('Unexpected fail with value foobar')
