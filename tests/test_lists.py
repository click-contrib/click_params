import click
import pytest

from click_params.lists import (
    StringListParamType, IntListParamType, FloatListParamType, DecimalListParamType, FractionListParamType,
    ComplexListParamType, DomainListParamType, UrlListParamType, PublicUrlListParamType, EmailListParamType,
    SlugListParamType, IpAddressListParamType, Ipv4AddressListParamType, Ipv6AddressListParamType,
    IpNetworkListParamType, Ipv4NetworkListParamType, Ipv6NetworkListParamType
)
from tests.helpers import assert_equals_output, assert_in_output


@pytest.mark.parametrize(('name', 'parameter'), [
    ('string list', StringListParamType()),
    ('int list', IntListParamType()),
    ('float list', FloatListParamType()),
    ('decimal list', DecimalListParamType()),
    ('fraction list', FractionListParamType()),
    ('complex list', ComplexListParamType()),
    ('domain list', DomainListParamType()),
    ('url list', UrlListParamType()),
    ('url list', PublicUrlListParamType()),
    ('email list', EmailListParamType()),
    ('slug list', SlugListParamType()),
    ('ip address list', IpAddressListParamType()),
    ('ipv4 address list', Ipv4AddressListParamType()),
    ('ipv6 address list', Ipv6AddressListParamType()),
    ('ip network list', IpNetworkListParamType()),
    ('ipv4 network list', Ipv4NetworkListParamType()),
    ('ipv6 network list', Ipv6NetworkListParamType())

])
def test_parameter_name_and_representation_are_correct(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(('parameter', 'expression', 'message'), [
    (IntListParamType(), '1,foo,2,2.5', "integers: ['foo', '2.5']"),
    (FloatListParamType(), '1.2,foo,2.5,bar', "floating point values: ['foo', 'bar']"),
    (DecimalListParamType(), '1.2,foo,2.5,bar', "decimal values: ['foo', 'bar']"),
    (FractionListParamType(' '), '1/3 foo/2 2.5 3/bar tar', "fraction values: ['foo/2', '3/bar', 'tar']"),
    (ComplexListParamType(' '), '5 foo 2+1j 1.4 bar', "complex values: ['foo', 'bar']"),
    (DomainListParamType(' '), 'foo.com bar', "domain names: ['bar']"),
    (UrlListParamType(' '), 'http://foo.com foo://bar.com', "urls: ['foo://bar.com']"),
    (PublicUrlListParamType(' '), 'http://foo.com ftp://10.0.0.1', "urls: ['ftp://10.0.0.1']"),
    (EmailListParamType(' '), 'bar@yahoo.fr bogus@@ foo@gmail.com', "emails: ['bogus@@']"),
    (SlugListParamType(' '), 'foo bar.com tar_foo', "slugs: ['bar.com']"),
    (IpAddressListParamType(' '), 'foo 10.0.0.1 1452', "ip addresses: ['foo', '1452']"),
    (Ipv4AddressListParamType(', '), '10.0.0.1, foo, ::1', "ipv4 addresses: ['foo', '::1']"),
    (Ipv6AddressListParamType(' '), '::1 foo ::dead:beef 10.0.0.1', "ipv6 addresses: ['foo', '10.0.0.1']"),
    (IpNetworkListParamType(' '), '192.168.1.0/24 foo 1254 2001:db00::/24', "ip networks: ['foo', '1254']"),
    (Ipv4NetworkListParamType(' '), '10.0.0.0/8 152 192.168.1.0/24', "ipv4 networks: ['152']"),
    (Ipv6NetworkListParamType(' '), '2001:db00::/24 foo 2001:db00::0/ffff:ff00::',
     "ipv6 networks: ['foo', '2001:db00::0/ffff:ff00::']")
])
def test_should_print_error_when_giving_wrong_value(runner, parameter, expression, message):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_in_output(2, f'These items are not {message}', result)


@pytest.mark.parametrize(('parameter', 'expression', 'expected_output'), [
    # string list
    (StringListParamType(), 'foo,bar', "['foo', 'bar']\n"),
    (StringListParamType(), '', "['']\n"),
    (StringListParamType(' '), '1 2 foo', "['1', '2', 'foo']\n"),
    # int list
    (IntListParamType(), '1,2', '[1, 2]\n'),
    (IntListParamType(';'), '1;2', '[1, 2]\n'),
    # float list
    (FloatListParamType(), '1,.2', '[1.0, 0.2]\n'),
    (FloatListParamType('; '), '1; .2', '[1.0, 0.2]\n'),
    # decimal list
    (DecimalListParamType(), '1,.2', "[Decimal('1'), Decimal('0.2')]\n"),
    (DecimalListParamType(' '), '1 .2', "[Decimal('1'), Decimal('0.2')]\n"),
    # fraction list
    (FractionListParamType(), '1/3,.5', '[Fraction(1, 3), Fraction(1, 2)]\n'),
    (FractionListParamType(' '), '1/3 .5', '[Fraction(1, 3), Fraction(1, 2)]\n'),
    # complex list
    (ComplexListParamType(), '5,1.4,2+1j', '[(5+0j), (1.4+0j), (2+1j)]\n'),
    (ComplexListParamType(', '), '5, 1.4, 2+1j', '[(5+0j), (1.4+0j), (2+1j)]\n'),
    # domain list
    (DomainListParamType(), 'foo.com,bar.fr', "['foo.com', 'bar.fr']\n"),
    (DomainListParamType(' '), 'foo.com bar.fr', "['foo.com', 'bar.fr']\n"),
    # url list
    (UrlListParamType(), 'https://foo.com,ftp://bar.fr', "['https://foo.com', 'ftp://bar.fr']\n"),
    (UrlListParamType(' '), 'https://10.0.0.1 ftp://bar.fr', "['https://10.0.0.1', 'ftp://bar.fr']\n"),
    (PublicUrlListParamType(), 'https://foo.com,ftp://bar.fr', "['https://foo.com', 'ftp://bar.fr']\n"),
    (PublicUrlListParamType(' '), 'https://foo.com ftp://1.1.1.1', "['https://foo.com', 'ftp://1.1.1.1']\n"),
    # email list
    (EmailListParamType(), 'bar@académie.fr,foo@gmail.com', "['bar@académie.fr', 'foo@gmail.com']\n"),
    (EmailListParamType(' '), 'bar@académie.fr foo@gmail.com', "['bar@académie.fr', 'foo@gmail.com']\n"),
    # slug list
    (SlugListParamType(), 'foo,bar_com,tar-1', "['foo', 'bar_com', 'tar-1']\n"),
    (SlugListParamType(', '), 'foo, bar_com, tar-1', "['foo', 'bar_com', 'tar-1']\n"),
    # ip address list
    (IpAddressListParamType(), '192.168.1.2,::dead:beef', "[IPv4Address('192.168.1.2'), IPv6Address('::dead:beef')]\n"),
    (IpAddressListParamType(' '), '192.168.1.2 ::dead:beef',
     "[IPv4Address('192.168.1.2'), IPv6Address('::dead:beef')]\n"),
    # ipv4 address list
    (Ipv4AddressListParamType(), '10.0.0.1,192.168.1.2', "[IPv4Address('10.0.0.1'), IPv4Address('192.168.1.2')]\n"),
    (Ipv4AddressListParamType(' '), '10.0.0.1 192.168.1.2', "[IPv4Address('10.0.0.1'), IPv4Address('192.168.1.2')]\n"),
    # ipv6 address list
    (Ipv6AddressListParamType(), '::1,::dead:beef', "[IPv6Address('::1'), IPv6Address('::dead:beef')]\n"),
    (Ipv6AddressListParamType(', '), '::1, ::dead:beef', "[IPv6Address('::1'), IPv6Address('::dead:beef')]\n"),
    # ip network list
    (IpNetworkListParamType(), '192.168.1.0/24,2001:db00::/24',
     "[IPv4Network('192.168.1.0/24'), IPv6Network('2001:db00::/24')]\n"),
    (IpNetworkListParamType(' '), '192.168.1.0/24 2001:db00::/24',
     "[IPv4Network('192.168.1.0/24'), IPv6Network('2001:db00::/24')]\n"),
    # ipv4 network list
    (Ipv4NetworkListParamType(), '10.0.0.0/8,192.168.1.0/24',
     "[IPv4Network('10.0.0.0/8'), IPv4Network('192.168.1.0/24')]\n"),
    (Ipv4NetworkListParamType(', '), '10.0.0.0/8, 192.168.1.0/24',
     "[IPv4Network('10.0.0.0/8'), IPv4Network('192.168.1.0/24')]\n"),
    # ipv6 network list
    (Ipv6NetworkListParamType(), '2001:db00::/24,2001:db8:1234::/48',
     "[IPv6Network('2001:db00::/24'), IPv6Network('2001:db8:1234::/48')]\n"),
    (Ipv6NetworkListParamType(', '), '2001:db00::/24, 2001:db8:1234::/48',
     "[IPv6Network('2001:db00::/24'), IPv6Network('2001:db8:1234::/48')]\n"),
])
def test_should_print_correct_output_when_giving_correct_value(runner, parameter, expression, expected_output):
    @click.command()
    @click.option('-v', 'values', type=parameter)
    def cli(values):
        click.echo(values)

    result = runner.invoke(cli, ['-v', expression])

    assert_equals_output(0, expected_output, result)
