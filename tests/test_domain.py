import click
import pytest

from click_params.domain import (
    DOMAIN, PUBLIC_URL, URL, EMAIL, SLUG, DomainListParamType, PublicUrlListParamType, UrlListParamType,
    EmailListParamType, SlugListParamType
)
from tests.helpers import assert_in_output, assert_equals_output


@pytest.mark.parametrize(('name', 'parameter'), [
    ('domain name', DOMAIN),
    ('url', PUBLIC_URL),
    ('url', URL),
    ('email address', EMAIL),
    ('slug', SLUG),
    ('domain name list', DomainListParamType()),
    ('url list', UrlListParamType()),
    ('url list', PublicUrlListParamType()),
    ('email address list', EmailListParamType()),
    ('slug list', SlugListParamType()),
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
def test_should_print_error_when_giving_incorrect_option_for_simple_types(runner, parameter, param_value):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_in_output(2, f'{param_value} is not a valid {parameter.name}', result)


@pytest.mark.parametrize(('parameter', 'expression', 'message'), [
    (DomainListParamType(' '), 'foo.com bar', "domain names: ['bar']"),
    (UrlListParamType(' '), 'http://foo.com foo://bar.com', "urls: ['foo://bar.com']"),
    (PublicUrlListParamType(' '), 'http://foo.com ftp://10.0.0.1', "urls: ['ftp://10.0.0.1']"),
    (EmailListParamType(' '), 'bar@yahoo.fr bogus@@ foo@gmail.com', "email addresses: ['bogus@@']"),
    (SlugListParamType(' '), 'foo bar.com tar_foo', "slugs: ['bar.com']"),
])
def test_should_print_error_when_giving_incorrect_option_for_list_types(runner, parameter, expression, message):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_in_output(2, f'These items are not {message}', result)


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
def test_should_print_correct_output_when_giving_correct_option_for_simple_types(runner, parameter, param_value):
    @click.command()
    @click.option('-v', 'value', type=parameter)
    def cli(value):
        click.echo(value)

    result = runner.invoke(cli, ['-v', param_value])

    assert_equals_output(0, f'{param_value}\n', result)


@pytest.mark.parametrize(('parameter', 'expression', 'expected_output'), [
    # domain list
    (DomainListParamType(), 'foo.com,bar.fr', "['foo.com', 'bar.fr']\n"),
    (DomainListParamType(' '), 'foo.com bar.fr', "['foo.com', 'bar.fr']\n"),
    # url list
    (UrlListParamType(), 'https://foo.com,ftp://bar.fr', "['https://foo.com', 'ftp://bar.fr']\n"),
    (UrlListParamType(' '), 'https://10.0.0.1 ftp://bar.fr', "['https://10.0.0.1', 'ftp://bar.fr']\n"),
    # public url list
    (PublicUrlListParamType(), 'https://foo.com,ftp://bar.fr', "['https://foo.com', 'ftp://bar.fr']\n"),
    (PublicUrlListParamType(' '), 'https://foo.com ftp://1.1.1.1', "['https://foo.com', 'ftp://1.1.1.1']\n"),
    # email list
    (EmailListParamType(), 'bar@académie.fr,foo@gmail.com', "['bar@académie.fr', 'foo@gmail.com']\n"),
    (EmailListParamType(' '), 'bar@académie.fr foo@gmail.com', "['bar@académie.fr', 'foo@gmail.com']\n"),
    # slug list
    (SlugListParamType(), 'foo,bar_com,tar-1', "['foo', 'bar_com', 'tar-1']\n"),
    (SlugListParamType(', '), 'foo, bar_com, tar-1', "['foo', 'bar_com', 'tar-1']\n"),
])
def test_should_print_correct_output_when_giving_correct_option_for_list_types(runner, parameter, expression,
                                                                               expected_output):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_equals_output(0, expected_output, result)
