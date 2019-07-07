"""Parameter types to represent list of items."""

import click

from .base import ListParamType
from .numeric import DECIMAL, FRACTION, COMPLEX
from .domain import DOMAIN, URL, PUBLIC_URL, EMAIL, SLUG
from .network import IP_ADDRESS, IPV4_ADDRESS, IPV6_ADDRESS, IP_NETWORK, IPV4_NETWORK, IPV6_NETWORK


class StringListParamType(ListParamType):
    name = 'string list'

    def __init__(self, separator: str = ','):
        super().__init__(click.STRING, separator)

    def convert(self, value, param, ctx):
        value = self._strip_separator(value)
        return value.split(self._separator)


class IntListParamType(ListParamType):
    name = 'int list'

    def __init__(self, separator: str = ','):
        super().__init__(click.INT, separator=separator, name='integers')


class FloatListParamType(ListParamType):
    name = 'float list'

    def __init__(self, separator: str = ','):
        super().__init__(click.FLOAT, separator=separator, name='floating point values')


class DecimalListParamType(ListParamType):
    name = 'decimal list'

    def __init__(self, separator: str = ','):
        super().__init__(DECIMAL, separator=separator, name='decimal values')


class FractionListParamType(ListParamType):
    name = 'fraction list'

    def __init__(self, separator: str = ','):
        super().__init__(FRACTION, separator=separator, name='fraction values')


class ComplexListParamType(ListParamType):
    name = 'complex list'

    def __init__(self, separator: str = ','):
        super().__init__(COMPLEX, separator=separator, name='complex values')


class DomainListParamType(ListParamType):
    name = 'domain list'

    def __init__(self, separator: str = ','):
        super().__init__(DOMAIN, separator=separator, name='domain names')


class UrlListParamType(ListParamType):
    name = 'url list'

    def __init__(self, separator: str = ','):
        super().__init__(URL, separator=separator, name='urls')


class PublicUrlListParamType(ListParamType):
    name = 'url list'

    def __init__(self, separator: str = ','):
        super().__init__(PUBLIC_URL, separator=separator, name='urls')


class EmailListParamType(ListParamType):
    name = 'email list'

    def __init__(self, separator: str = ','):
        super().__init__(EMAIL, separator=separator, name='emails')


class SlugListParamType(ListParamType):
    name = 'slug list'

    def __init__(self, separator: str = ','):
        super().__init__(SLUG, separator=separator, name='slugs')


class IpAddressListParamType(ListParamType):
    name = 'ip address list'

    def __init__(self, separator: str = ','):
        super().__init__(IP_ADDRESS, separator=separator, name='ip addresses')


class Ipv4AddressListParamType(ListParamType):
    name = 'ipv4 address list'

    def __init__(self, separator: str = ','):
        super().__init__(IPV4_ADDRESS, separator=separator, name='ipv4 addresses')


class Ipv6AddressListParamType(ListParamType):
    name = 'ipv6 address list'

    def __init__(self, separator: str = ','):
        super().__init__(IPV6_ADDRESS, separator=separator, name='ipv6 addresses')


class IpNetworkListParamType(ListParamType):
    name = 'ip network list'

    def __init__(self, separator: str = ','):
        super().__init__(IP_NETWORK, separator=separator, name='ip networks')


class Ipv4NetworkListParamType(ListParamType):
    name = 'ipv4 network list'

    def __init__(self, separator: str = ','):
        super().__init__(IPV4_NETWORK, separator=separator, name='ipv4 networks')


class Ipv6NetworkListParamType(ListParamType):
    name = 'ipv6 network list'

    def __init__(self, separator: str = ','):
        super().__init__(IPV6_NETWORK, separator=separator, name='ipv6 networks')
