# Numeric

We will cover the different numeric parameter types in this tutorial.
For all the examples, we assume that the file is called cli.py and has a section like the following at the end.

````python
if __name__ == '__main__':
    cli()
````

!!! note
    For windows users, instead of using simple quotes for the following examples related to list parameters,
    you should use double quotes.

## FRACTION

Converts a string to a `fractions.Fraction` object.

````python
import click
from click_params import FRACTION

@click.command()
@click.option('-f', '--fraction', type=FRACTION)
def cli(fraction):
    click.echo(fraction)
````

````bash
$ python cli.py -f 0.4
2/5

$ python cli.py -f 1/2
1/2
````

## FractionRange

Signature: `FractionRange(minimum: fractions.Fraction = None, maximum: fractions.Fraction = None, clamp: bool = False)`

A parameter that works similar to [FRACTION](#fraction) but restricts the value to fit into a range. The default
behavior is to fail if the value falls outside the range, but it can also be silently clamped between the two edges.

````python
from fractions import Fraction

import click
from click_params import FractionRange

min_fraction = Fraction('1/10')
max_fraction = Fraction('1')

@click.command()
@click.option('-f', '--first-fraction', type=FractionRange(min_fraction, max_fraction))
@click.option('-s', '--second-fraction', type=FractionRange(min_fraction, max_fraction, clamp=True))
def cli(first_fraction, second_fraction):
    click.echo(first_fraction)
    click.echo(second_fraction)
````

````bash
$ python cli.py -f 0.2 -s 3/2
1/5
1

$ python cli.py -f 0.01 -s 1/4
Error: 1/100 is not in the valid range of 1/10 to 1.
````

## FractionListParamType

Signature: `FractionListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts a string to a list of `fractions.Fraction` objects.

````python
import click
from click_params import FractionListParamType

@click.command()
@click.option('-f', '--fractions', '_fractions', type=FractionListParamType(' '))
def cli(_fractions):
    click.echo('Your fractions:')
    for fraction in _fractions:
        click.echo(f'- {fraction}')
````

````bash
$ python cli.py --fractions='0.1 0.4 2/5 0.3'
Your fractions:
- 1/10
- 2/5
- 2/5
- 3/10

$ python cli.py --fractions='0.1 foo 2/5'
Error: These items are not fractions: ['foo']
````

## DECIMAL

Converts a string to a `decimal.Decimal` object.

````python
import click
from click_params import DECIMAL

@click.command()
@click.option('-v', '--value', type=DECIMAL)
def cli(value):
    click.echo(value)
````

````bash
$ python cli.py -v 4.2
4.2

$ python cli.py -v 1
1

$ python cli.py -f 1/2
Error: 1/2 is not a valid decimal
````

## DecimalRange

Signature: `DecimalRange(minimum: decimal.Decimal = None, maximum: decimal.Decimal = None, clamp: bool = False)`

A parameter that works similar to [DECIMAL](#decimal) but restricts the value to fit into a range. The default
behavior is to fail if the value falls outside the range, but it can also be silently clamped between the two edges.

````python
from decimal import Decimal

import click
from click_params import DecimalRange

min_decimal = Decimal('0.5')
max_decimal = Decimal('1.5')

@click.command()
@click.option('-f', '--first-decimal', type=DecimalRange(min_decimal, max_decimal))
@click.option('-s', '--second-decimal', type=DecimalRange(min_decimal, max_decimal, clamp=True))
def cli(first_decimal, second_decimal):
    click.echo(first_decimal)
    click.echo(second_decimal)
````

````bash
$ python cli.py -f 0.6 -s 1.7
0.6
1.5

$ python cli.py -f 0.3 -s 1
Error: 0.3 is not in the valid range of 0.5 to 1.5.
````

## DecimalListParamType

Signature: `DecimalListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts a string to a list of `decimal.Decimal` objects.

````python
import click
from click_params import DecimalListParamType

@click.command()
@click.option('-v', '--values', type=DecimalListParamType(' '))
def cli(values):
    click.echo('The numbers you entered are:')
    for value in values:
        click.echo(f'- {value}')
````

````bash
$ python cli.py --values='.1 1 4.2'
The numbers you entered are:
- 0.1
- 1
- 4.2

$ python cli.py --values='.1 foo 4.2 1/2'
Error: These items are not decimal values: ['foo', '1/2']
````

## COMPLEX

Converts a string to a `complex` object.

````python
import click
from click_params import COMPLEX

@click.command()
@click.option('-c', '--complex', 'complex_number', type=COMPLEX)
def cli(complex_number):
    click.echo(complex_number)
````

````bash
$ python cli.py -c 4
(4+0j)

$ python cli.py -c 1+2j
(1+2j)

$ python cli.py -c 1 + 2j
Error: 1 + 2j is not a valid complex
````

You will notice in the last example that space is not allowed when specifying the imaginary part.

## ComplexListParamType

Signature: `ComplexListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts a string to a list of `complex` values.

````python
import click
from click_params import ComplexListParamType

@click.command()
@click.option('-c', '--complex-values', type=ComplexListParamType(' '))
def cli(complex_values):
    click.echo('the complex values you entered are:')
    for _complex in complex_values:
        click.echo(f'- {_complex}')
````

````bash
python cli.py --complex-values='1 12j 1-2j 5.4+3j'
the complex values you entered are:
- (1+0j)
- 12j
- (1-2j)
- (5.4+3j)

python cli.py --complex-values='1 1/2 1+1.2j 12j'
Error: These items are not complex values: ['1/2']
````

## IntListParamType

Signature: `IntListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts a string to a list of integers.

````python
import click
from click_params import IntListParamType

@click.command()
@click.option('-i', '--integers', type=IntListParamType(' '))
def cli(integers):
    click.echo('The integers you entered are:')
    for _int in integers:
        click.echo(f'- {_int}')
````

````bash
$ python cli.py --integers='1 45'
The integers you entered are:
1
45

$ python cli.py --integers='1 4.5 41'
Error: These items are not integers: ['4.5']
````

## FloatListParamType

Signature: `FloatListParamType(separator: str = ',', ignore_empty: bool = False)`

Converts a string to a list of floating point values.

````python
import click
from click_params import FloatListParamType

@click.command()
@click.option('-f', '--floats', type=FloatListParamType(' '))
def cli(floats):
    click.echo('The floating point values you entered are:')
    for _float in floats:
        click.echo(f'- {_float}')
````

````bash
$ python cli.py --floats='1 .5 -2.1'
The floating point values you entered are:
- 1.0
- 0.5
- -2.1

$ python cli.py --floats='1 1/2 -2.1'
Error: These items are not floating point values: ['1/2']
````
