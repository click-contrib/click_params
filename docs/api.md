# API

We will see the different base classes you can use to create your own click parameters.

## BaseParamType

Signature: `BaseParamType(_type: Any, errors: Union[Error, Tuple[Error]], name: str = None)`

This is the base class you will want to use to implement simple types such as `DECIMAL` or `FRACTION`.

Parameters:

- `_type`: the class used to convert the string passed as option or argument.
- `errors`: a single error class or a tuple of error classes that can be raised when trying to convert the string.
- `name`: the name used in the error message to specify the type of the parameter, if it is not provided, the `name`
class attribute will be used instead.

Below is an example to create a custom integer type. This is just for example because click already has a `click.INT`
type.

````python
from click_params import BaseParamType

class IntType(BaseParamType):
    name = 'integer'

    def __init__(self):
        super().__init__(_type=int, errors=ValueError)
````

Here is another example where we have a tuple of errors. It is in fact the implementation of `FRACTION` type.

````python
from fractions import Fraction

class FractionParamType(BaseParamType):
    name = 'fraction'

    def __init__(self):
        super().__init__(_type=Fraction, errors=(ValueError, ZeroDivisionError))
````

## ValidatorParamType

Signature: `ValidatorParamType(callback: Callable, name: str = None)`

This class is for those who use the excellent `validators` library. If you want to check that a string follows a certain
pattern you can create a validator function and used it to create a custom click parameter type.

Parameters:

- `callback`: validator function used to check the string passed as option or argument.
- `name`: the name used in the error message to specify the type of the parameter, if it is not provided, the `name`
class attribute will be used instead.

Below is an example to create a custom type that will check that the number passed as option or argument is even.

````python
from validators import validator
from click_params import ValidatorParamType

@validator
def even(value):
    return not (int(value) % 2)

class EvenType(ValidatorParamType):
    name = 'even'

    def __init__(self):
        super().__init__(even, 'even number')
````

Some wise people will notice that the check is not complete in the `even` function because we don't check if the string
is an integer and it could raise error. This is for the simplicity of the example but you are encouraged to make all
the necessary tests in your code ;)

## RangeParamType

Signature: `RangeParamType(param_type: click.ParamType, minimum: Min = None, maximum: Max = None, clamp: bool = False)`

This class helps to create types where values needed to be bounded. The `minimum` and `maximum` parameters **must** have
the **same type** and the type **must** implement comparison operators (<, >, ..).

Parameters:

- `param_type`: the click type used to convert string passed as option or argument.
- `minimum`: the minimum value to allow. If not specified, it will be None, meaning that there is no lower limit.
- `maximum`: the maximum value to allow. If not specified, it will be None, meaning that there is no upper limit.
- `clamp`: if `True` the value falling outside the range will be clamped to the nearest limit (e.g: if you have a range
of 0 to 3 and a user provides 4, the value saved will be 3), if `False` the value falling outside the range will raise
an error.

Below is an example to create a custom IntRange. This is for example because click already provides a `click.IntRange`
type.

````python
import click
from click_params import RangeParamType

class IntRange(RangeParamType):
    """This class will be used to test the correctness of RangeParamType"""
    name = 'int range'

    def __init__(self, minimum: int = None, maximum: int = None, clamp: bool = False):
        super().__init__(click.INT, minimum, maximum, clamp)
````

!!! note
    If you look at the `__repr__` implementation of the `RangeParamType`, you will notice that it expects a `name`
    attribute with two words separated by a whitespace. If you don't want this behaviour you can override this method.

## ListParamType

Signature: `ListParamType(param_type: click.ParamType, separator: str = ',', name: str = None)`

This class is used to implement custom list types.

Parameters:

- `param_type`: the click type used to convert each item of the string passed as option or argument.
- `separator`: the string used to delimit each item of the string.
- `name`: the name used in the error message to specify the type of the parameter, if it is not provided, the `name`
class attribute will be used instead.
- `ignore_empty`: when this flag is True, will treat empty strings as empty lists. This is useful when we want empty
list to be our default value.

Below is the implementation of the `IntListParamType`.

````python
import click
from click_params import ListParamType

class IntListParamType(ListParamType):
    name = 'int list'

    def __init__(self, separator: str = ','):
        super().__init__(click.INT, separator=separator, name='integers')
````
