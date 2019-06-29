"""Domain parameter types."""
from functools import partial
from typing import List

from validators import domain, url, email, slug

from .base import ValidatorParamType


class DomainParamType(ValidatorParamType):
    name = 'domain name'

    def __init__(self):
        super().__init__(callback=domain)


class UrlParamType(ValidatorParamType):
    name = 'url'

    def __init__(self, public: bool = False):
        super().__init__(callback=partial(url, public=public))


class EmailParamType(ValidatorParamType):
    name = 'email'

    def __init__(self, whitelist: List[str] = None):
        super().__init__(callback=partial(email, whitelist=whitelist))


class SlugParamType(ValidatorParamType):
    name = 'slug'

    def __init__(self):
        super().__init__(callback=slug)


DOMAIN = DomainParamType()
PUBLIC_URL = UrlParamType(public=True)
URL = UrlParamType()  # this type includes private url
EMAIL = EmailParamType()
SLUG = SlugParamType()
