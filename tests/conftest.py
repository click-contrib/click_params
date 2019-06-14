from click.testing import CliRunner
import pytest


@pytest.fixture()
def runner():
    """Click test runner"""
    return CliRunner()
