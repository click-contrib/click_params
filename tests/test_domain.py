import click
import pytest

from click_params.domain import DOMAIN, PUBLIC_URL, URL, EMAIL, SLUG
from tests.helpers import assert_in_output, assert_equals_output


@pytest.mark.parametrize(('name', 'parameter'), [
    ('domain name', DOMAIN),
    ('url', PUBLIC_URL),
    ('url', URL),
    ('email', EMAIL),
    ('slug', SLUG)
])
def test_parameter_name_and_representation_are_correct(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(('parameter', 'param_value'), [
    (DOMAIN, 'foo'),
    (DOMAIN, '4'),
    # public url
    (PUBLIC_URL, 'http://foo'),
    (PUBLIC_URL, 'foo://bar.com'),
    (PUBLIC_URL, 'http://10.0.0.1'),
    # URL
    (URL, 'http://foo'),
    (URL, 'foo://bar.com'),
    # email
    (EMAIL, 'bogus@@'),
    (EMAIL, 'bogus@foo'),
    # slug
    (SLUG, 'foo.bar')
])
def test_should_print_error_when_giving_incorrect_option(runner, parameter, param_value):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_in_output(2, f'{param_value} is not a valid {parameter.name}', result)


@pytest.mark.parametrize(('parameter', 'param_value'), [
    (DOMAIN, 'foo.com'),
    # public url
    (PUBLIC_URL, 'http://foo.com'),
    (PUBLIC_URL, 'https://1.1.1.1/path'),
    # url
    (URL, 'ftp://bar.com'),
    (URL, 'http://10.0.0.1'),
    # email
    (EMAIL, 'foo@bar.com'),
    (EMAIL, 'bar@académie.fr'),
    # slug
    (SLUG, 'foo'),
    (SLUG, 'foo-bar'),
    (SLUG, 'foo-bar_tar')
])
def test_should_print_correct_output_when_giving_correct_option(runner, parameter, param_value):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_equals_output(0, f'{param_value}\n', result)
