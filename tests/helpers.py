"""Helper functions for test"""
from click.testing import Result


def assert_in_output(exit_code: int, expected_output: str, result: Result) -> None:
    assert exit_code == result.exit_code
    assert expected_output in result.output


def assert_equals_output(exit_code: int, expected_output: str, result: Result) -> None:
    assert exit_code == result.exit_code
    assert expected_output == result.output
