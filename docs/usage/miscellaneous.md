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

## UUIDListParamType

Signature: `UUIDListParamType(separator: str = ',')`

Converts string to a list of `uuid.UUID` objects.

````python
import click
from click_params import UUIDListParamType

@click.command()
@click.option('-u', '--uuid-list', type=UUIDListParamType(' '))
def cli(uuid_list):
    click.echo('Your list of uuid is:')
    for uuid in uuid_list:
        click.echo(f'- {uuid}')
````

````bash
$ python cli.py --uuid-list='a7309d0b-c858-4d54-b6e1-1c20f8c22047 bfa65f3c-e6ac-4844-8e09-e84535f8cdc5'
Your list of uuid is:
- a7309d0b-c858-4d54-b6e1-1c20f8c22047
- bfa65f3c-e6ac-4844-8e09-e84535f8cdc5

$ python cli.py --uuid-list='452-45 bfa65f3c-e6ac-4844-8e09-e84535f8cdc5 410'
Error: These items are not uuid: ['452-45', '410']
````

## DateTimeParamListType

Signature: `DateTimeParamListType(separator: str = ',', formats: List[str] = None)`

Converts string to a list of `datetime.datetime` objects. Unlike other classes, this class has a `formats` parameter
that is exactly the same as the one passed to the constructor of `click.DateTime` class.

````python
import click
from click_params import DateTimeListParamType

@click.command()
@click.option('-d', '--datetimes', type=DateTimeListParamType(', '))
def cli(datetimes):
    click.echo('The dates your entered are:')
    for datetime in datetimes:
        click.echo(f'- {datetime}')
````

````bash
$ python cli.py --datetimes='2018-04-05, 2019-01-01 01:00:00'
The dates your entered are:
- 2018-04-05 00:00:00
- 2019-01-01 01:00:00

$ python cli.py --datetimes='2019/01/01, 2019-01-01'
Error: These items are not datetimes: ['2019/01/01']
````

Two remarks compared to the last script.

- The separator used for the previous command is `', '`. This come in handy because one of the datetime passed as option
has a whitespace, therefore the separator helps to split properly.
- In the last example the datetime `2019/01/01` fails because the format `%Y/%m/%d` is not one of the defaults used by
`click.DateTime`. If you want this datetime to be accepted, you need to provide a `formats` argument with the appropriate
formats.