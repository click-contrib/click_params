# Network

We will cover the different network parameter types in this tutorial.
For all the examples, we assume that the file is called cli.py and has a section like the following at the end.

````python
if __name__ == '__main__':
    cli()
````

!!! note
    For windows users, instead of using simple quotes for the following examples related to list parameters,
    you should use double quotes.

## IP_ADDRESS

Converts string to an `ipaddress.IPv4Address` or `ipaddress.IPv6Address` object.

````python
import click
from click_params import IP_ADDRESS

@click.command()
@click.option('-i', '--ip-address', type=IP_ADDRESS)
def cli(ip_address):
    click.echo(f'Your ip address is {ip_address}')
````

````bash
$ python cli.py -i 10.0.0.1
Your ip address is 10.0.0.1

$ python cli.py -i ::1
Your ip address is ::1

$ python cli.py -i 12.45
Error: 12.45 is not a valid ip address
````

## IpAddressListParamType

Signature: `IpAddressListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts string to a list of `ipaddress.IPv4Address` or `ipaddress.IPv6Address` objects.

````python
import click
from click_params import IpAddressListParamType

@click.command()
@click.option('-i', '--ip-addresses', type=IpAddressListParamType(' '),
 help='list of ip addresses separated by a white space')
def cli(ip_addresses):
    click.echo('Your list of ip addresses:')
    for ip_address in ip_addresses:
        click.echo(f'- {ip_address}')
````

````bash
$ python cli.py --ip-addresses='127.0.0.1 ::1'
Your list of ip addresses:
- 127.0.0.1
- ::1

$ python cli.py --ip-addresses='127.0.0.1 1245 ::1'
Error: These items are not ip addresses: ['1245']
````

## IPV4_ADDRESS

Converts string to a `ipaddress.IPv4Address` object.

````python
import click
from click_params import IPV4_ADDRESS

@click.command()
@click.option('-i', '--ip-address', type=IPV4_ADDRESS)
def cli(ip_address):
    click.echo(f'Your ipv4 address is {ip_address}')
````

````bash
$ python cli.py -i 10.0.0.1
Your ipv4 address is 10.0.0.1

$ python cli.py -i ::1
Error: ::1 is not a valid ipv4 address
````

## Ipv4AddressRange

Signature: `Ipv4AddressRange(minimum: ipaddress.IPv4Address = None, maximum: ipaddress.IPv4Address = None, clamp: bool = False)`

A parameter that works similar to [IPV4_ADDRESS](#ipv4_address) but restricts the value to fit into a range. The default
behavior is to fail if the value falls outside the range, but it can also be silently clamped between the two edges.

````python
from ipaddress import IPv4Address

import click
from click_params import Ipv4AddressRange

min_ip = IPv4Address('127.0.0.1')
max_ip = IPv4Address('127.0.0.125')

@click.command()
@click.option('-f', '--first-ip', type=Ipv4AddressRange(min_ip, max_ip))
@click.option('-s', '--second-ip', type=Ipv4AddressRange(min_ip, max_ip, clamp=True))
def cli(first_ip, second_ip):
    click.echo(first_ip)
    click.echo(second_ip)
````

````bash
$ python cli.py -f 127.0.0.1 -s 127.0.0.130
127.0.0.1
127.0.0.125

$ python cli.py -f 127.0.0.0 -s 127.0.0.4
Error: 127.0.0.0 is not in the valid range of 127.0.0.1 to 127.0.0.125.
````

## Ipv4AddressListParamType

Signature: `Ipv4AddressListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts string to a list of `ipaddress.IPv4Address` objects.

````python
import click
from click_params import Ipv4AddressListParamType

@click.command()
@click.option('-i', '--ip-addresses', type=Ipv4AddressListParamType(' '),
 help='list of ipv4 addresses separated by a white space')
def cli(ip_addresses):
    click.echo('Your list of ipv4 addresses:')
    for ip_address in ip_addresses:
        click.echo(f'- {ip_address}')
````

````bash
$ python cli.py --ip-addresses='127.0.0.1 1.1.1.1'
Your list of ipv4 addresses:
- 127.0.0.1
- 1.1.1.1

$ python cli.py --ip-addresses='127.0.0.1 1.1.1.1 ::1'
Error: These items are not ipv4 addresses: ['::1']
````

## IPV6_ADDRESS

Converts string to a `ipaddress.IPv6Address` object.

````python
import click
from click_params import IPV6_ADDRESS

@click.command()
@click.option('-i', '--ip-address', type=IPV6_ADDRESS)
def cli(ip_address):
    click.echo(f'Your ipv6 address is {ip_address}')
````

````bash
$ python cli.py -i ::1
Your ipv6 address is ::1

$ python cli.py -i 127.0.0.1
Error: 127.0.0.1 is not a valid ipv6 address
````

## Ipv6AddressRange

Signature: `Ipv6AddressRange(minimum: ipaddress.IPv6Address = None, maximum: ipaddress.IPv6Address = None, clamp: bool = False)`

A parameter that works similar to [IPV6_ADDRESS](#ipv6_address) but restricts the value to fit into a range. The default
behavior is to fail if the value falls outside the range, but it can also be silently clamped between the two edges.

````python
from ipaddress import IPv6Address

import click
from click_params import Ipv6AddressRange

min_ip = IPv6Address('2001:db00::1')
max_ip = IPv6Address('2001:dbff:ffff:ffff:ffff:ffff:ffff:fffe')

@click.command()
@click.option('-f', '--first-ip', type=Ipv6AddressRange(min_ip, max_ip))
@click.option('-s', '--second-ip', type=Ipv6AddressRange(min_ip, max_ip, clamp=True))
def cli(first_ip, second_ip):
    click.echo(first_ip)
    click.echo(second_ip)
````

````bash
$ python cli.py -f 2001:db00::2 -s 2001:dc00::9
2001:db00::2
2001:dbff:ffff:ffff:ffff:ffff:ffff:fffe

$ python cli.py -f 2001:dc00::9 -s 2001:db00::2
Error: 2001:dc00::9 is not in the valid range of 2001:db00::1 to 2001:dbff:ffff:ffff:ffff:ffff:ffff:fffe.
````

## Ipv6AddressListParamType

Signature: `Ipv6AddressListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts string to a list of `ipaddress.IPv6Address` objects.

````python
import click
from click_params import Ipv6AddressListParamType

@click.command()
@click.option('-i', '--ip-addresses', type=Ipv6AddressListParamType(' '),
 help='list of ipv6 addresses separated by a white space')
def cli(ip_addresses):
    click.echo('Your list of ipv6 addresses:')
    for ip_address in ip_addresses:
        click.echo(f'- {ip_address}')
````

````bash
$ python cli.py --ip-addresses='::1 ::dead:beef'
Your list of ipv6 addresses:
- ::1
- ::dead:beef

$ python cli.py --ip-addresses='127.0.0.1 ::1'
Error: These items are not ipv6 addresses: ['127.0.0.1']
````

## IP_NETWORK

Converts string to a `ipaddress.IPv4Network` or `ipaddress.IPv6Network` object.

````python
import click
from click_params import IP_NETWORK

@click.command()
@click.option('-n', '--network', type=IP_NETWORK)
def cli(network):
    click.echo(f'Your network is {network}')
````

````bash
$ python cli.py -n 192.168.1.0/24
Your network is 192.168.1.0/24

$ python cli.py -n 2001:db00::/24
Your network is 2001:db00::/24

$ python cli.py -n 1245
Error: 1245 is not a valid ip network
````

## IpNetworkListParamType

Signature: `IpNetworkListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts string to a list of `ipaddress.IPv4Network` or `ipaddress.IPv6Network` objects.

````python
import click
from click_params import IpNetworkListParamType

@click.command()
@click.option('-n', '--networks', type=IpNetworkListParamType(' '),
 help='list of ip networks separated by a white space')
def cli(networks):
    click.echo('Your list of ip networks:')
    for network in networks:
        click.echo(f'- {network}')
````

````bash
$ python cli.py --networks='192.168.1.0/24 2001:db00::/24'
Your list of ip networks:
- 192.168.1.0/24
- 2001:db00::/24

$ python cli.py --networks='192.168.1.0/24 142.5 2001:db00::/24'
Error: These items are not ip networks: ['142.5']
````

## IPV4_NETWORK

Converts string to a `ipaddress.IPv4Network` object.

````python
import click
from click_params import IPV4_NETWORK

@click.command()
@click.option('-n', '--network', type=IPV4_NETWORK)
def cli(network):
    click.echo(f'Your network is {network}')
````

````bash
$ python cli.py -n 192.168.1.0/24
Your network is 192.168.1.0/24

$ python cli.py -n 2001:db00::/24
Error: 2001:db00::/24 is not a valid ipv4 network
````

## Ipv4NetworkListParamType

Signature: `Ipv4NetworkListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts string to a list of `ipaddress.IPv4Network` objects.

````python
import click
from click_params import Ipv4NetworkListParamType

@click.command()
@click.option('-n', '--networks', type=Ipv4NetworkListParamType(' '),
 help='list of ipv4 networks separated by a white space')
def cli(networks):
    click.echo('Your list of ipv4 networks:')
    for network in networks:
        click.echo(f'- {network}')
````

````bash
$ python cli.py --networks='192.168.1.0/24 10.0.0.0/8'
Your list of ipv4 networks:
- 192.168.1.0/24
- 10.0.0.0/8

$ python cli.py --networks='192.168.1.0/24 2001:db00::/24'
Error: These items are not ipv4 networks: ['2001:db00::/24']
````

## IPV6_NETWORK

Converts string to a `ipaddress.IPv6Network` object.

````python
import click
from click_params import IPV6_NETWORK

@click.command()
@click.option('-n', '--network', type=IPV6_NETWORK)
def cli(network):
    click.echo(f'Your network is {network}')
````

````bash
$ python cli.py -n 2001:db00::/24
Your network is 2001:db00::/24

$ python cli.py -n 192.168.1.0/24
Error: 192.168.1.0/24 is not a valid ipv6 network
````

## Ipv6NetworkListParamType

Signature: `Ipv6NetworkListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts string to a list of `ipaddress.IPv6Network` objects.

````python
import click
from click_params import Ipv6NetworkListParamType

@click.command()
@click.option('-n', '--networks', type=Ipv6NetworkListParamType(' '),
 help='list of ipv6 networks separated by a white space')
def cli(networks):
    click.echo('Your list of ipv6 networks:')
    for network in networks:
        click.echo(f'- {network}')
````

````bash
$ python cli.py --networks='2001:db8:1234::/48 2001:db00::/24'
Your list of ip networks:
- 2001:db8:1234::/48
- 2001:db00::/24

$ python cli.py --networks='192.168.1.0/24 2001:db8:1234::/48 2001:db00::/24'
Error: These items are not ip networks: ['192.168.1.0/24']
````
