import pytest
from click.testing import CliRunner


@pytest.fixture()
def runner():
    """Click test runner"""
    return CliRunner()
