# click-params

A bunch of useful click parameter types.

## Why?

I often find myself wanting to use a click parameter able to handle list of strings, so I decide to put this in a library
and I ended adding more parameter types that can be useful for various scripts including network, mathematics and so on.


## Installation

```bash
pip install click-params
```

click-params starts working from **python 3.6**. It has a few dependencies:
- [click](https://click.palletsprojects.com/en/7.x/) (I think this is obvious)
- [validators](https://validators.readthedocs.io/en/latest/)

## Usage

```python
import click
from click_params import Ipv4AddressListParamType

@click.command()
@click.option('-a', '--addresses', help='list of ipv4 addresses', prompt='list of ipv4 addresses to reserve',
 type=Ipv4AddressListParamType())
def pool(addresses):
    click.echo('reserved ips:')
    for ip in addresses:
        click.echo(ip)
```

```bash
$ pool --addresses='192.168.1.1,192.168.1.14'
reserved ips:
192.168.1.1
192.168.1.14
```

You can change the default separator "," by passing it when initializing the parameter type.

## Documentation

Documentation is available at https://click-params.readthedocs.io/en/latest/.

