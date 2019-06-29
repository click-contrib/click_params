"""Network parameter types"""
import ipaddress

from .base import BaseParamType, RangeParamType


class IpAddress(BaseParamType):
    name = 'ip address'

    def __init__(self):
        super().__init__(_type=ipaddress.ip_address, errors=ValueError)


class Ipv4Address(BaseParamType):
    name = 'ipv4 address'

    def __init__(self):
        super().__init__(_type=ipaddress.IPv4Address, errors=ValueError)


class Ipv4AddressRange(RangeParamType):
    name = 'ipv4 address range'

    def __init__(self, minimum: ipaddress.IPv4Address = None, maximum: ipaddress.IPv4Address = None,
                 clamp: bool = False):
        super().__init__(Ipv4Address(), minimum, maximum, clamp)

    def __repr__(self):
        return f'IPV4AddressRange({repr(self._minimum)}, {repr(self._maximum)})'


class Ipv6Address(BaseParamType):
    name = 'ipv6 address'

    def __init__(self):
        super().__init__(_type=ipaddress.IPv6Address, errors=ValueError)


class Ipv6AddressRange(RangeParamType):
    name = 'ipv6 address range'

    def __init__(self, minimum: ipaddress.IPv6Address = None, maximum: ipaddress.IPv6Address = None,
                 clamp: bool = False):
        super().__init__(Ipv6Address(), minimum, maximum, clamp)

    def __repr__(self):
        return f'IPV6AddressRange({repr(self._minimum)}, {repr(self._maximum)})'


class IpNetwork(BaseParamType):
    name = 'ip network'

    def __init__(self):
        super().__init__(_type=ipaddress.ip_network, errors=ValueError)


class Ipv4Network(BaseParamType):
    name = 'ipv4 network'

    def __init__(self):
        super().__init__(_type=ipaddress.IPv4Network, errors=ValueError)


class Ipv6Network(BaseParamType):
    name = 'ipv6 network'

    def __init__(self):
        super().__init__(_type=ipaddress.IPv6Network, errors=ValueError)


IP_ADDRESS = IpAddress()
IPV4_ADDRESS = Ipv4Address()
IPV6_ADDRESS = Ipv6Address()
IP_NETWORK = IpNetwork()
IPV4_NETWORK = Ipv4Network()
IPV6_NETWORK = Ipv6Network()
