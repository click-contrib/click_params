# Miscellaneous

We will cover the parameter types that don't fit in other thematics in this tutorial.
For all the examples, we assume that the file is called cli.py and has a section like the following at the end.

````python
if __name__ == '__main__':
    cli()
````

!!! note
    For windows users, instead of using simple quotes for the following examples related to list parameters,
    you should use double quotes.


## JSON

Validates that a string is a valid JSON statement and returns a dict.

````python
import click
from click_params import JSON

@click.command()
@click.option('-j', '--json', 'value', type=JSON)
def cli(value):
    click.echo(f'Your fruits and vegetables: {value}')
````

````bash
$ python cli.py -j '{"fruits": ["apples", "strawberries"], "vegetables": ["tomatoes", "cucumbers"]}'
Your fruits and vegetables: {'fruits': ['apples', 'strawberries'], 'vegetables': ['tomatoes', 'cucumbers']}

$ python cli.py -j a
Error: 'a' is not a valid json string
````

## MAC_ADDRESS

Validates that a string is a valid mac address.

````python
import click
from click_params import MAC_ADDRESS

@click.command()
@click.option('-m', '--mac-address', 'value', type=MAC_ADDRESS)
def cli(mac_address):
    click.echo(f'Your mac address is: {mac_address}')
````

````bash
$ python cli.py -m 01:23:45:67:AB:CD
Your mac address is 01:23:45:67:AB:CD

$ python cli.py -m 00:00:00:00:00
Error: 00:00:00:00:00 is not a valid mac address
````

## MacAddressListParamType

Signature: `MacAddressListParamType(separator: str = ',')`

Validates and returns a list of mac addresses

````python
import click
from click_params import MacAddressListParamType

@click.command()
@click.option('-m', '--mac-addresses', type=MacAddressListParamType(' '),
 help='list of mac addresses separated by a white space')
def cli(mac_addresses):
    click.echo('Your list of mac addresses:')
    for mac_address in mac_addresses:
        click.echo(f'- {mac_address}')
````

````bash
$ python cli.py --mac-addresses='00:00:00:00:00:00 01:23:45:67:AB:CD'
Your list of domain names:
- 00:00:00:00:00:00
- 01:23:45:67:AB:CD

$ python cli.py --mac-addresses='foo 01:23:45:67:AB:CD'
Error: These items are not mac addresses: ['foo']
````

## StringListParamType

Signature: `StringListParamType(separator: str = ',')`

Converts given string to a list of strings.

````python
import click
from click_params import StringListParamType

@click.command()
@click.option('-f', '--fruits', type=StringListParamType(' '),
 help='list of fruits separated by a white space')
def cli(fruits):
    click.echo('Your list of preferred fruits:')
    for fruit in fruits:
        click.echo(f'- {fruit}')
````

````bash
$ python cli.py --fruits='apples pineaples strawberries'
Your list of preferred fruits:
- apples
- pineapples
- strawberries
````
