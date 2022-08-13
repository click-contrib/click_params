# Domain

We will cover the different domain parameter types in this tutorial.
For all the examples, we assume that the file is called cli.py and has a section like the following at the end.

````python
if __name__ == '__main__':
    cli()
````

!!! note
    For windows users, instead of using simple quotes for the following examples related to list parameters,
    you should use double quotes.

## DOMAIN

Validates that a string is a regular domain name.

!!! warning
    This parameter depends on function `validators.domain` and it seems that it does not allow a dot at the end of a
    string. So `foo.com` is fine but `foo.com.` not. This is currently a limitation of the `validators` library.

Example

````python
import click
from click_params import DOMAIN

@click.command()
@click.option('-d', '--domain', type=DOMAIN)
def cli(domain):
    click.echo(f'Your domain is {domain}')
````

````bash
$ python cli.py -d foo.com
Your domain is foo.com

$ python cli.py -d hello
Error: hello is not a valid domain name
````

## DomainListParamType

Signature: `DomainListParamType(separator: str = ',', ignore_empty: bool = False)`

Validates and returns a list of domain names.

Example:

````python
import click
from click_params import DomainListParamType

@click.command()
@click.option('-d', '--domains', type=DomainListParamType(' '), help='list of domain names separated by a white space')
def cli(domains):
    click.echo('Your list of domain names:')
    for domain in domains:
        click.echo(f'- {domain}')
````

````bash
$ python cli.py --domains='foo.com bar.com'
Your list of domain names:
- foo.com
- bar.com

$ python cli.py --domains='foo bar.com bar'
Error: These items are not domain names: ['foo', 'bar']
````

## PUBLIC_URL

Validates that a string is a regular url.

!!! note
    For the host part, private ip addresses are not allowed, hence the name of this parameter. So an url like
    `http://10.0.0.1` is not correct.

Example:

````python
import click
from click_params import PUBLIC_URL

@click.command()
@click.option('-u', '--url', type=PUBLIC_URL)
def cli(url):
    click.echo(f'Your url is {url}')
````

````bash
$ python cli.py -d http://bar.com/path
Your url is http://bar.com/path

$ python cli.py -d hello
Error: hello is not a valid public url
````

## PublicUrlListParamType

Signature: `PublicUrlListParamType(separator: str = ',', ignore_empty: bool = False)`

Validates and returns a list of public urls.

````python
import click
from click_params import PublicUrlListParamType

@click.command()
@click.option('-u', '--urls', type=PublicUrlListParamType(' '), help='list of url separated by a white space')
def cli(urls):
    click.echo('Your list of urls:')
    for url in urls:
        click.echo(f'- {url}')
````

````bash
$ python cli.py --urls='http://1.1.1.1/ https://example.com'
Your list of urls:
- http://1.1.1.1/
- http://example.com

$ python cli.py htp://foo.com ftp://1.1.1.1
Error: These items are not urls: ['htp://foo.com']
````

## URL

It is like [PUBLIC_URL](#public_url) but it also accepts private ip addresses.

````python
import click
from click_params import URL

@click.command()
@click.option('-u', '--url', type=URL)
def cli(url):
    click.echo(f'Your url is {url}')
````

````bash
$ python cli.py -d http://10.0.0.1/path
Your url is http://10.0.0.1/path

$ python cli.py -d hello
Error: hello is not a valid public url
````

## UrlListParamType

Signature: `UrlListParamType(separator: str = ',', ignore_empty: bool = False)`

It is like [PublicUrlListParamType](#publicurllistparamtype) but accepts private ip addresses.

````python
import click
from click_params import UrlListParamType

@click.command()
@click.option('-u', '--urls', type=UrlListParamType(' '), help='list of url separated by a white space')
def cli(urls):
    click.echo('Your list of urls:')
    for url in urls:
        click.echo(f'- {url}')
````

````bash
$ python cli.py --urls='http://10.0.0.1/ https://example.com'
Your list of urls:
- http://10.0.0.1/
- http://example.com

$ python cli.py htp://foo.com ftp://1.1.1.1
Error: These items are not urls: ['htp://foo.com']
````

## EMAIL

Validates that a string is a valid email address.

````python
import click
from click_params import EMAIL

@click.command()
@click.option('-e', '--email', type=EMAIL)
def cli(email):
    click.echo(f'Your email is {email}')
````

````bash
$ python cli.py -e foo@académie.fr
Your email is foo@académie.fr

$ python cli.py -e roo@foo
Error: roo@foo is not a valid email address
````

!!! note
    There is also a more generic parameter type `EmailParamType(whitelist: List[str] = None)` that you can use, it
    comes from the validators function `validators.email`. To be honest, I don't understand the usefulness of the
    `whitelist` parameter but I provided it in case anyone finds it.

## EmailListParamType

Signature: `EmailListParamType(separator: str = ',', ignore_empty: bool = False)`

Validates and returns a list of email addresses.

````python
import click
from click_params import EmailListParamType

@click.command()
@click.option('-a', '--addresses', type=EmailListParamType(' '), help='list of email addresses separated by a white space')
def cli(addresses):
    click.echo('Your list of email addresses:')
    for address in addresses:
        click.echo(f'- {address}')
````

````bash
$ python cli.py --emails='foo@yahoo.fr bar@gmail.com'
Your list of email addresses:
- foo@yahoo.fr
- bar@gmail.com

$ python cli.py --emails='roo foo@yahoo.fr tar@gz bar.gmail.com'
Error: These items are not email addresses: ['roo', 'tar@gz']
````

## SLUG

Validates that a string is a slug.

````python
import click
from click_params import SLUG

@click.command()
@click.option('-s', '--slug', type=SLUG)
def cli(slug):
    click.echo(f'You enter the following slug: {slug}')
````

````bash
$ python cli.py -s foo-bar
You enter the following slug: foo-bar

$ python cli.py -s foo.bar
Error: foo.bar is not a valid slug
````

## SlugListParamType

Signature: `SlugListParamType(separator: str = ',', ignore_empty: bool = False)`

Validates and returns a list of slugs.

````python
import click
from click_params import SlugListParamType

@click.command()
@click.option('-s', '--slugs', type=SlugListParamType(' '), help='list of slugs separated by a white space')
def cli(slugs):
    click.echo('Your list of slugs:')
    for slug in slugs:
        click.echo(f'- {slug}')
````

````bash
$ python cli.py --slugs='foo foo-bar foo_bar-tar'
Your list of slugs:
- foo
- foo-bar
- foo-bar_tar

$ python cli.py --slugs='foo .foo foo-bar'
Error: These items are not slugs: ['.foo']
````
