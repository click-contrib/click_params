# Tests

click-params provides some helper functions to deal with tests.

## assert_equals_output

It will help you to validate the exit code and the string returned by your click command.

````python
import click

@click.command()
@click.option('-n', '--name')
def cli(name):
    if name == 'John':
        raise click.BadParameter('the name is incorrect!')
    click.echo(f'Your name is : {name}')
````

In your test, you can use the helper function as follows:

````python
from click.testing import CliRunner
from click_params import assert_equals_output

from my_project.scripts import cli

def test_echo_name():
    runner = CliRunner()
    result = runner.invoke(cli, ['-n', 'Kevin'])

    assert_equals_output(0, 'Your name is Kevin\n', result)
````

## assert_in_output

It looks like the previous function but is limiting to check if a part of the final string returned by the command is
present.

If we consider again the previous command, if we want to test the case where the name entered by the user is _John_, it
will not be convenient to test the entire error message returned by the click command because a large part is generated
by click itself and it is irrelevant: `"Usage... Error.."`.

Instead, we would prefer to focus on the error message we explicitly send to the user, in this case:
`"the name is incorrect"`

````python
from click.testing import CliRunner
from click_params import assert_in_output

from my_project.scripts import cli

def test_echo_name():
    runner = CliRunner()
    result = runner.invoke(cli, ['-n', 'John'])

    assert_in_output(2, 'the name is incorrect!', result)
````

# assert_list_in_output

This function is useful when you just want to test substrings of the returned string. I often find it useful when the
command we wrote return json output. For example consider we have the following output:

````json
{
  "name": "Kevin T",
  "age": 25
}
````

It will be tricky to test the whole string or even a part of it because it will be necessary to play with the `\n` and the
spaces. In this case we will prefer to test the presence of the different keys and values.

````python
from click.testing import CliRunner
from click_params import assert_list_in_output

from my_project.scripts import cli

def test_echo_json():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert_list_in_output(0, ['name', 'Kevin T', 'age', 25], result)
````
