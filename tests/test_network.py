from ipaddress import IPv4Address, IPv6Address

import click
import pytest

from click_params.network import (
    IP_ADDRESS, IPV4_ADDRESS, IPV6_ADDRESS, IP_NETWORK, IPV4_NETWORK, IPV6_NETWORK, Ipv4AddressRange, Ipv6AddressRange
)
from tests.helpers import assert_in_output, assert_equals_output


@pytest.mark.parametrize(('name', 'parameter'), [
    ('ip address', IP_ADDRESS),
    ('ipv4 address', IPV4_ADDRESS),
    ('ipv6 address', IPV6_ADDRESS),
    ('ip network', IP_NETWORK)
])
def test_parameter_name_and_representation_are_correct_for_simple_types(name, parameter):
    assert name == parameter.name
    assert name.upper() == repr(parameter)


@pytest.mark.parametrize(('name', 'representation', 'parameter'), [
    ('ipv4 address range', f'IPV4AddressRange({repr(IPv4Address("127.0.0.1"))}, {repr(IPv4Address("127.0.0.5"))})',
     Ipv4AddressRange(IPv4Address('127.0.0.1'), IPv4Address('127.0.0.5'))),
    ('ipv6 address range', f'IPV6AddressRange({repr(IPv6Address("::1"))}, {repr(IPv6Address("::10"))})',
     Ipv6AddressRange(IPv6Address('::1'), IPv6Address('::10')))
])
def test_parameter_name_and_representation_are_correct_for_range_types(name, representation, parameter):
    assert name == parameter.name
    assert representation == repr(parameter)


@pytest.mark.parametrize(('parameter', 'param_value'), [
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
])
def test_should_print_error_when_giving_incorrect_option(runner, parameter, param_value):
    @click.command()
    @click.option('-i', '--ip', type=parameter)
    def cli(ip):
        click.echo(ip)

    result = runner.invoke(cli, ['-i', param_value])

    assert_in_output(2, f'{param_value} is not a valid {parameter.name}', result)


@pytest.mark.parametrize(('parameter', 'param_value'), [
    (IP_ADDRESS, '192.168.1.1'),
    (IP_ADDRESS, '::dead:beef'),
    (IPV4_ADDRESS, '192.168.1.1'),
    (IPV6_ADDRESS, '::dead:beef'),
    (IP_NETWORK, '192.168.0.0/24'),
    (IP_NETWORK, '2001:db00::/24'),
    (IPV4_NETWORK, '192.168.0.0/24'),
    (IPV6_NETWORK, '2001:db00::/24')
])
def test_should_print_correct_output_when_giving_correct_option(runner, parameter, param_value):
    @click.command()
    @click.option('-i', '--ip', type=parameter)
    def cli(ip):
        click.echo(ip)

    result = runner.invoke(cli, ['-i', param_value])

    assert_equals_output(0, f'{param_value}\n', result)
