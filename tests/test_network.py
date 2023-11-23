from ipaddress import IPv4Address, IPv6Address

import click
import pytest

from click_params.network import (
    IP_ADDRESS,
    IP_NETWORK,
    IPV4_ADDRESS,
    IPV4_NETWORK,
    IPV6_ADDRESS,
    IPV6_NETWORK,
    IpAddressListParamType,
    IpNetworkListParamType,
    Ipv4AddressListParamType,
    Ipv4AddressRange,
    Ipv4NetworkListParamType,
    Ipv6AddressListParamType,
    Ipv6AddressRange,
    Ipv6NetworkListParamType,
)
from tests.helpers import assert_equals_output, assert_in_output


@pytest.mark.parametrize(
    ('name', 'parameter'),
    [
        ('ip address', IP_ADDRESS),
        ('ipv4 address', IPV4_ADDRESS),
        ('ipv6 address', IPV6_ADDRESS),
        ('ip network', IP_NETWORK),
        ('ip address list', IpAddressListParamType()),
        ('ipv4 address list', Ipv4AddressListParamType()),
        ('ipv6 address list', Ipv6AddressListParamType()),
        ('ip network list', IpNetworkListParamType()),
        ('ipv4 network list', Ipv4NetworkListParamType()),
        ('ipv6 network list', Ipv6NetworkListParamType()),
    ],
)
def test_parameter_name_and_representation_are_correct_for_simple_and_list_types(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(
    ('name', 'representation', 'parameter'),
    [
        (
            'ipv4 address range',
            f'IPV4AddressRange({repr(IPv4Address("127.0.0.1"))}, {repr(IPv4Address("127.0.0.5"))})',
            Ipv4AddressRange(IPv4Address('127.0.0.1'), IPv4Address('127.0.0.5')),
        ),
        (
            'ipv6 address range',
            f'IPV6AddressRange({repr(IPv6Address("::1"))}, {repr(IPv6Address("::10"))})',
            Ipv6AddressRange(IPv6Address('::1'), IPv6Address('::10')),
        ),
    ],
)
def test_parameter_name_and_representation_are_correct_for_range_types(name, representation, parameter):
    assert name == parameter.name
    assert representation == repr(parameter)


@pytest.mark.parametrize(
    ('parameter', 'param_value'),
    [
        # generic ip address (ipv4 or ipv6)
        (IP_ADDRESS, 'foo'),
        (IP_ADDRESS, '1245'),
        (IP_ADDRESS, '125.5'),
        # ipv4 address
        (IPV4_ADDRESS, 'foo'),
        (IPV4_ADDRESS, '1245'),
        (IPV4_ADDRESS, '125.5'),
        # ipv6 address
        (IPV6_ADDRESS, 'foo'),
        (IPV6_ADDRESS, '1245'),
        (IPV6_ADDRESS, '125.5'),
        # generic ip network (ipv4 or ipv6)
        (IP_NETWORK, 'foo'),
        (IP_NETWORK, '1245'),
        (IP_NETWORK, '1452.5'),
        (IP_NETWORK, '12.0.0.0/45'),
        (IP_NETWORK, '1245/24'),
        (IP_NETWORK, '2001:db00::0/ffff:ff00::'),
        # ipv4 network
        (IPV4_NETWORK, 'foo'),
        (IPV4_NETWORK, '1245'),
        (IPV4_NETWORK, '1452.5'),
        (IPV4_NETWORK, '12.0.0.0/45'),
        (IPV4_NETWORK, '1245/24'),
        # ipv6 network
        (IPV6_NETWORK, 'foo'),
        (IPV6_NETWORK, '1245'),
        (IPV6_NETWORK, '1452.5'),
        (IPV6_NETWORK, '2001:db00::0/ffff:ff00::'),
    ],
)
def test_should_print_error_when_giving_incorrect_option_for_simple_types(runner, parameter, param_value):
    @click.command()
    @click.option('-i', '--ip', type=parameter)
    def cli(ip):
        click.echo(ip)

    result = runner.invoke(cli, ['-i', param_value])

    assert_in_output(2, f'{param_value} is not a valid {parameter.name}', result)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'message'),
    [
        (IpAddressListParamType(' '), 'foo 10.0.0.1 1452', "ip addresses: ['foo', '1452']"),
        (Ipv4AddressListParamType(', '), '10.0.0.1, foo, ::1', "ipv4 addresses: ['foo', '::1']"),
        (Ipv6AddressListParamType(' '), '::1 foo ::dead:beef 10.0.0.1', "ipv6 addresses: ['foo', '10.0.0.1']"),
        (IpNetworkListParamType(' '), '192.168.1.0/24 foo 1254 2001:db00::/24', "ip networks: ['foo', '1254']"),
        (Ipv4NetworkListParamType(' '), '10.0.0.0/8 152 192.168.1.0/24', "ipv4 networks: ['152']"),
        (
            Ipv6NetworkListParamType(' '),
            '2001:db00::/24 foo 2001:db00::0/ffff:ff00::',
            "ipv6 networks: ['foo', '2001:db00::0/ffff:ff00::']",
        ),
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
    ('parameter', 'value', 'message'),
    [
        (
            Ipv4AddressRange(IPv4Address('192.168.1.1'), IPv4Address('192.168.1.254')),
            '192.169.1.1',
            '192.169.1.1 is not in the valid range of 192.168.1.1 to 192.168.1.254.',
        ),
        (
            Ipv6AddressRange(IPv6Address('2001:db00::1'), IPv6Address('2001:dbff:ffff:ffff:ffff:ffff:ffff:fffe')),
            IPv6Address('2001:dc00::9'),
            '2001:dc00::9 is not in the valid range of 2001:db00::1 to 2001:dbff:ffff:ffff:ffff:ffff:ffff:fffe.',
        ),
    ],
)
def test_should_print_error_when_giving_value_is_out_of_limits(runner, parameter, value, message):
    @click.command()
    @click.option('-c', 'count', type=parameter)
    def cli(count):
        click.echo(count)

    result = runner.invoke(cli, ['-c', value])

    assert_in_output(2, message, result)


@pytest.mark.parametrize(
    ('parameter', 'param_value'),
    [
        (IP_ADDRESS, '192.168.1.1'),
        (IP_ADDRESS, '::dead:beef'),
        (IPV4_ADDRESS, '192.168.1.1'),
        (IPV6_ADDRESS, '::dead:beef'),
        (IP_NETWORK, '192.168.0.0/24'),
        (IP_NETWORK, '2001:db00::/24'),
        (IPV4_NETWORK, '192.168.0.0/24'),
        (IPV6_NETWORK, '2001:db00::/24'),
        (Ipv4AddressRange(IPv4Address('192.168.1.1'), IPv4Address('192.168.1.254')), '192.168.1.1'),
        (
            Ipv6AddressRange(IPv6Address('2001:db00::1'), IPv6Address('2001:dbff:ffff:ffff:ffff:ffff:ffff:fffe')),
            '2001:db00::4',
        ),
    ],
)
def test_should_print_correct_output_when_giving_correct_option_for_simple_and_range_types(
    runner, parameter, param_value
):
    @click.command()
    @click.option('-i', '--ip', type=parameter)
    def cli(ip):
        click.echo(ip)

    result = runner.invoke(cli, ['-i', param_value])

    assert_equals_output(0, f'{param_value}\n', result)


@pytest.mark.parametrize(
    ('parameter', 'expression', 'expected_output'),
    [
        # ip address list
        (
            IpAddressListParamType(),
            '192.168.1.2,::dead:beef',
            "[IPv4Address('192.168.1.2'), IPv6Address('::dead:beef')]\n",
        ),
        (
            IpAddressListParamType(' '),
            '192.168.1.2 ::dead:beef',
            "[IPv4Address('192.168.1.2'), IPv6Address('::dead:beef')]\n",
        ),
        # ipv4 address list
        (Ipv4AddressListParamType(), '10.0.0.1,192.168.1.2', "[IPv4Address('10.0.0.1'), IPv4Address('192.168.1.2')]\n"),
        (
            Ipv4AddressListParamType(' '),
            '10.0.0.1 192.168.1.2',
            "[IPv4Address('10.0.0.1'), IPv4Address('192.168.1.2')]\n",
        ),
        # ipv6 address list
        (Ipv6AddressListParamType(), '::1,::dead:beef', "[IPv6Address('::1'), IPv6Address('::dead:beef')]\n"),
        (Ipv6AddressListParamType(', '), '::1, ::dead:beef', "[IPv6Address('::1'), IPv6Address('::dead:beef')]\n"),
        # ip network list
        (
            IpNetworkListParamType(),
            '192.168.1.0/24,2001:db00::/24',
            "[IPv4Network('192.168.1.0/24'), IPv6Network('2001:db00::/24')]\n",
        ),
        (
            IpNetworkListParamType(' '),
            '192.168.1.0/24 2001:db00::/24',
            "[IPv4Network('192.168.1.0/24'), IPv6Network('2001:db00::/24')]\n",
        ),
        # ipv4 network list
        (
            Ipv4NetworkListParamType(),
            '10.0.0.0/8,192.168.1.0/24',
            "[IPv4Network('10.0.0.0/8'), IPv4Network('192.168.1.0/24')]\n",
        ),
        (
            Ipv4NetworkListParamType(', '),
            '10.0.0.0/8, 192.168.1.0/24',
            "[IPv4Network('10.0.0.0/8'), IPv4Network('192.168.1.0/24')]\n",
        ),
        # ipv6 network list
        (
            Ipv6NetworkListParamType(),
            '2001:db00::/24,2001:db8:1234::/48',
            "[IPv6Network('2001:db00::/24'), IPv6Network('2001:db8:1234::/48')]\n",
        ),
        (
            Ipv6NetworkListParamType(', '),
            '2001:db00::/24, 2001:db8:1234::/48',
            "[IPv6Network('2001:db00::/24'), IPv6Network('2001:db8:1234::/48')]\n",
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
    'param_type',
    [
        IpAddressListParamType,
        Ipv4AddressListParamType,
        Ipv6AddressListParamType,
        IpNetworkListParamType,
        Ipv4NetworkListParamType,
        Ipv6NetworkListParamType,
    ],
)
def test_network_list_param_types_ignore_empty_string(param_type):
    network_list_type = param_type(ignore_empty=True)

    assert network_list_type.convert('', None, None) == []
