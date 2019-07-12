"""Domain parameter types."""
from functools import partial
from typing import List

from validators import domain, url, email, slug

from .base import ValidatorParamType, ListParamType


class DomainParamType(ValidatorParamType):
    name = 'domain name'

    def __init__(self):
        super().__init__(callback=domain)


class DomainListParamType(ListParamType):
    name = 'domain name list'

    def __init__(self, separator: str = ','):
        super().__init__(DOMAIN, separator=separator, name='domain names')


class UrlParamType(ValidatorParamType):
    name = 'url'

    def __init__(self, public: bool = False):
        super().__init__(callback=partial(url, public=public))


class UrlListParamType(ListParamType):
    name = 'url list'

    def __init__(self, separator: str = ','):
        super().__init__(URL, separator=separator, name='urls')


class PublicUrlListParamType(ListParamType):
    name = 'url list'

    def __init__(self, separator: str = ','):
        super().__init__(PUBLIC_URL, separator=separator, name='urls')


class EmailParamType(ValidatorParamType):
    name = 'email address'

    def __init__(self, whitelist: List[str] = None):
        super().__init__(callback=partial(email, whitelist=whitelist))


class EmailListParamType(ListParamType):
    name = 'email address list'

    def __init__(self, separator: str = ','):
        super().__init__(EMAIL, separator=separator, name='email addresses')


class SlugParamType(ValidatorParamType):
    name = 'slug'

    def __init__(self):
        super().__init__(callback=slug)


class SlugListParamType(ListParamType):
    name = 'slug list'

    def __init__(self, separator: str = ','):
        super().__init__(SLUG, separator=separator, name='slugs')


DOMAIN = DomainParamType()
PUBLIC_URL = UrlParamType(public=True)
URL = UrlParamType()  # this type includes private url
EMAIL = EmailParamType()
SLUG = SlugParamType()
