"""Domain parameter types."""
from functools import partial

from deprecated import deprecated
from validators import domain, email, slug, url

from .base import ListParamType, ValidatorParamType


class DomainParamType(ValidatorParamType):
    name = 'domain name'

    def __init__(self):
        super().__init__(callback=domain)


class DomainListParamType(ListParamType):
    name = 'domain name list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(DOMAIN, separator=separator, name='domain names', ignore_empty=ignore_empty)


class UrlParamType(ValidatorParamType):
    name = 'url'

    def __init__(
        self,
        skip_ipv6_addr: bool = False,
        skip_ipv4_addr: bool = False,
        may_have_port: bool = False,
        simple_host: bool = False,
        rfc_1034: bool = False,
        rfc_2782: bool = False,
    ):
        super().__init__(
            callback=partial(
                url,
                skip_ipv6_addr=skip_ipv6_addr,
                skip_ipv4_addr=skip_ipv4_addr,
                may_have_port=may_have_port,
                simple_host=simple_host,
                rfc_1034=rfc_1034,
                rfc_2782=rfc_2782,
            )
        )


class UrlListParamType(ListParamType):
    name = 'url list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(URL, separator=separator, name='urls', ignore_empty=ignore_empty)


@deprecated(
    version='0.5.0',
    reason='This class now works in the same way as UrlListParamType and will be removed in a future release. '
    'You may want to create your custom type only validating public urls if you want that specific behaviour',
)
class PublicUrlListParamType(ListParamType):
    name = 'url list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(PUBLIC_URL, separator=separator, name='urls', ignore_empty=ignore_empty)


class EmailParamType(ValidatorParamType):
    name = 'email address'

    def __init__(
        self,
        ipv6_address: bool = False,
        ipv4_address: bool = False,
        simple_host: bool = False,
        rfc_1034: bool = False,
        rfc_2782: bool = False,
    ):
        super().__init__(
            callback=partial(
                email,
                ipv6_address=ipv6_address,
                ipv4_address=ipv4_address,
                simple_host=simple_host,
                rfc_1034=rfc_1034,
                rfc_2782=rfc_2782,
            )
        )


class EmailListParamType(ListParamType):
    name = 'email address list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(EMAIL, separator=separator, name='email addresses', ignore_empty=ignore_empty)


class SlugParamType(ValidatorParamType):
    name = 'slug'

    def __init__(self):
        super().__init__(callback=slug)


class SlugListParamType(ListParamType):
    name = 'slug list'

    def __init__(self, separator: str = ',', ignore_empty: bool = False):
        super().__init__(SLUG, separator=separator, name='slugs', ignore_empty=ignore_empty)


DOMAIN = DomainParamType()
URL = UrlParamType()
PUBLIC_URL = URL  # Just an alias for backward compatibility
EMAIL = EmailParamType()
SLUG = SlugParamType()
