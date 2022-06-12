# python-decorators-explained

A helper repo to illustrate how and why python decorators work.

There are some examples of some decorators to start.

## Running examples

* `python -m venv .venv`
* `source .venv/bin/activate`
* `python file-name.py`

## Examples

Going through examples of decorators. Each section will give an example of a decorator and
how they work. First starting with how Python modules are ran as scripts. Each example builds
into the next. Information from `a0_intro.py` will build into the next until the end.

### a0_intro.py

This file contains the most basic information for how these examples will work. Every module has a
`print("Module Loaded")` statement at the top. This is just to show when the module is loaded.

1. The module uses the `__name__` == `__main__` to determine if it is being run as a script or imported (more details https://stackoverflow.com/a/419185/1686511)
2. `print` is used to help show what code is executing
3. The `inspect` module is used to know what code is calling other code
4. There will be a `running_function` and a `main` function to illustrate execution.

The point of this intro file is to show how to run a module as a script. As well as to get familiar with
what `inspect` is doing to show us what functions are calling other functions.

```zsh
(.venv) ➜  python-decorators-explained git:(main) ✗ python a0_intro.py
Module Loaded
IN MAIN
IN RUN FUNC
CALLED BY main_func
OUT MAIN
```

The above output shows the `main_func` is calling the `running_function` and the
running function is being called by the `main_func`.

### b1_beginning.py

This is the first use of a decorator. Decorators are used by prefacing a function with an `@` symbol.
This works because of how the Python interpreter reads the `@` symbol.

1. Decorators are functions that are then used with an `@` before another function
2. Decorators execute whenever the `@` is interpreted

To see how this works run the

```zsh
(.venv) ➜  python-decorators-explained git:(main) ✗ python b1_beginning.py
Module Loaded
IN DECORATOR
CALLED BY <module>
RETURNING running_function
OUT DECORATOR

IN MAIN
IN RUN FUNC
CALLED BY main
OUT MAIN
```

It may not be clear the `@example_beginning_decorator` is getting executed _before_ the `main_func` is called.
Looking at the output this is somewhat clear, however, reading the code it may not be clear. As another
example open a python shell and import the `b1_beginning.py` file.

```
(.venv) ➜  python-decorators-explained git:(main) ✗ ipython
Python 3.10.3 (main, May  4 2022, 09:22:28) [Clang 13.1.6 (clang-1316.0.21.2)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from b1_beginning import *
Module Loaded
IN DECORATOR
CALLED BY <module>
RETURNING running_function
OUT DECORATOR
```

Notice how the `example_beginning_decorator` is outputting the print statements. Even whenever the
file is imported. This is because the `@` symbol is interpreted as a decorator, and immediately
executed. Further, whenever a decorator is executed you can see from the `RETURNING running_function`
in the output, that the `example_beginning_decorator` was called with the function passed as an
argument.

### c2_beginning_with_explanation.py

This example works exactly like the only before, only it is showing that a decorator is the same
as the following:

```python
def example_beginning_decorator(func):
    print("IN DECORATOR")
    print(f"CALLED BY {inspect.stack()[1][3]}")
    print(f"RETURNING {func.__name__}")
    print("OUT DECORATOR\n")
    return func

def running_function():
    """
    Example of a decorator function invoked later.
    """
    print(f"IN RUN FUNC")
    print(f"CALLED BY {inspect.stack()[1][3]}")

    return "Running Function Value"

decorated_running_function = example_beginning_decorator(running_function)
```

Try out running the code from `c2_beginning_with_explanation.py` in a shell.

```zsh
(.venv) ➜  python-decorators-explained git:(main) ✗ python c2_beginning_with_explanation.py
IN DECORATOR
CALLED BY <module>
RETURNING running_function
OUT DECORATOR

IN DECORATOR
CALLED BY <module>
RETURNING running_function
OUT DECORATOR

IN MAIN
IN RUN FUNC
CALLED BY main
OUT MAIN
IN MAIN
IN RUN FUNC
CALLED BY main
OUT MAIN
```

Both usages of the `@example_beginning_decorator` and `example_beginning_decorator(running_function)` result
in the same exact output. This illustrates how decorators are effectively nice syntax around function
definitions.

However, the decorators so far are not very useful, because they are executing immediately and not doing
much to "enhance" our functions. Or to keep track of information.

### d3_adding_some_state.py

In this example two things are done. The goal is to show how you _could_ go about managing state to
keep track of information by using a decorator.

1. We are adding information to a function by "slapping on an attribute" -- it's allowed!
2. The function used as a decorator is adding information each time it runs

Try running the script in a shell.

```zsh
(.venv) ➜  python-decorators-explained git:(main) ✗ python d3_adding_some_state.py
Decorator used with func_1
Decorator used with func_2
Decorator used with func_3
Decorator used with func_4
IN MAIN
IN FUNC 1
IN FUNC 2
IN FUNC 3
IN FUNC 4
OUT MAIN
```

Nothing too special is happening. The decorator is used to decorator the 4 functions. And then the 4
functions are called. Now look at the decorator in repl (read evaluate print loop).

```python
(.venv) ➜  python-decorators-explained git:(main) ✗ ipython
Python 3.10.3 (main, May  4 2022, 09:22:28) [Clang 13.1.6 (clang-1316.0.21.2)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

Decorator used with func_1
Decorator used with func_2
Decorator used with func_3
Decorator used with func_4
In [1]: from d3_adding_some_state import decorator_with_state

In [2]: decorator_with_state.called_functions
Out[2]: ['func_1', 'func_2', 'func_3', 'func_4']
```

What's cool here is that you can see the decorator is adding information to the function. this happens
because the decorator is called whenever it is imported, as shown before.

From the above, we can go one step further to show that using a decorator is just like calling the
function.

```python
In [3]: decorator_with_state(lambda x: x)
Decorator used with <lambda>
Out[3]: <function __main__.<lambda>(x)>

In [4]: decorator_with_state.called_functions
Out[4]: ['func_1', 'func_2', 'func_3', 'func_4', '<lambda>']
```

The `decorator_with_state` function is called wth a `lambda`. The output then shows the lambda as part
of the group of functions passed to `decorator_with_state`.

### e4_using_a_wrapper.py

This example starts to show what most folks think about when they use decorators.  Notice how there
is no output when the file is imported. It happens when the `running_function` is called.

```shell
(.venv) ➜  python-decorators-explained git:(main) ✗ python e4_using_a_wrapper.py
IN MAIN
IN DECORATOR
CALLED BY main
CALLING running_function
IN RUN FUNC
CALLED BY wrapper
OUT DECORATOR

OUT MAIN
```

To further show the execution of the decorator happens when the `running_function` is called look at
the output in the REPL.

```python
(.venv) ➜  python-decorators-explained git:(main) ✗ ipython
Python 3.10.3 (main, May  4 2022, 09:22:28) [Clang 13.1.6 (clang-1316.0.21.2)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from e4_using_a_wrapper import running_function

In [2]: running_function()
IN DECORATOR
CALLED BY <cell line: 1>
CALLING running_function
IN RUN FUNC
CALLED BY wrapper
OUT DECORATOR
```

### f5_using_a_wrapper_incorrectly.py

This example is exactly like the one before, only it shows what can go wrong if one forgets to call the
decorated function.  Look what happens when the function is called.

```sh
(.venv) ➜  python-decorators-explained git:(main) ✗ python f5_usaing_a_wrapper_incorrectly.py
IN MAIN
IN DECORATOR
CALLED BY main
OUT DECORATOR

OUT MAIN
```

Notice the `running_function` body never executes. This is because on line `8` the function is never
called that was decorated.  Recall that a decorator is the same as doing

```python

def my_decorator(func):
    print("decoratred")
    def wrapper():
        print("In the wrapper")
        func()
    return wrapper

def my_function():
    print("function called")


my_function = my_decorator(my_function)
```

```shell
In [2]: def my_decorator(func):
   ...:     print("decorated")
   ...:     def wrapper():
   ...:         print("In the wrapper")
   ...:         func()
   ...:     return wrapper
   ...:
   ...: def my_function():
   ...:     print("function called")
   ...:
   ...:
   ...: my_function = my_decorator(my_function)
decorated

In [3]: my_function()
In the wrapper
function called
```

Notice the `decorated` was printed because the function call to `my_decorator`. Then during the call to
`my_function` we see the wrapper called, and then the original `my_function` called. This is why it's
very important to remember to call the decorated function.  This also helps to show that a decorator
is the same as redefining a function.


### g6_using_a_wrapper_correctly.py

Something that may not have been clear before, we were using `wapper` incorrectly. Usually whenever you
wrap a function you want to be transparent about the wrapping, and return the decorated function as far
as other parts of a program are concerned. Look at this new example:

```shell
(.venv) ➜  python-decorators-explained git:(main) ✗ python g6_using_a_wrapper_correctly.py
IN MAIN
Calling the ____ wrapper ____
IN DECORATOR
CALLED BY main
IN RUN FUNC
CALLED BY wrapper
OUT DECORATOR
```

It's not clear where our code came from. It appears to be calling a function called `wrapper` which we
did not create in our `decorator_with_wrapper_no_wraps`.


The reason this isn't very helpful is we did not pass along the function definition whenever
we wrapped the function. Fortunately Python has a neat builtin tool to help us out called `functools.wraps`
See all the cool details about on the website: https://docs.python.org/3/library/functools.html#functools.wraps

> This is a convenience function for invoking update_wrapper() as a function decorator when defining a wrapper function. It is equivalent to partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated).

The above is from the Python docs, but shows how to use the `@wraps` decorator.  The `@wraps` decorator
keeps the original functions information available to the rest of the program.

Rerun the above with `doit` passed as an argument, to see the output difference:

```shell
(.venv) ➜  python-decorators-explained git:(main) ✗ python g6_using_a_wrapper_correctly.py doit
showing the one with wraps
Calling the ____ running_function_with_wraps ____
IN DECORATOR
CALLED BY main
IN RUN FUNC
CALLED BY wrapper
OUT DECORATOR

IN MAIN
Calling the ____ wrapper ____
IN DECORATOR
CALLED BY main
IN RUN FUNC
CALLED BY wrapper
OUT DECORATOR

OUT MAIN
```

Notice how the first one is called by the correct name, `running_function_with_wraps`. This may seem trivial,
however, it is very important as your systems grow more complex. The `@wraps` decorator is a way to keep the
execution lineage of your code, and not attribute all errors to a function named `wrapper`. As an example
tools like `pytest` will look at function `__name__` you are doing some testing. If the `wrapper` function
is not properly passing the decorated function information back, then it's harder to know what's happening
in your tests. There are also other tools that take advantage of knowing the names and types of your functions.
By using `@wraps` you can keep this information around for other tools to use.

There is a minor exercise to show that the `@wraps` is used as a decorator. However the same result can
be achieved by redefining the function like decorators do anyway. And also shows using a parameter,
which comes in the next example.

```python
(.venv) ➜  python-decorators-explained git:(main) ✗ ipython
Python 3.10.3 (main, May  4 2022, 09:22:28) [Clang 13.1.6 (clang-1316.0.21.2)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from g6_using_a_wrapper_correctly import running_function_with_wraps_no_dec

In [2]: running_function_with_wraps_no_dec()
IN DECORATOR
CALLED BY <cell line: 1>
IN RUN FUNC
CALLED BY wrapper
OUT DECORATOR


In [3]: running_function_with_wraps_no_dec.__name__
Out[3]: 'running_function_with_wraps_no_dec'
```

Notice the `running_function_with_wraps_no_dec` name is still the same. This is because the `wraps`
being used.

### h7_using_a_wrapper_with_state.py

This example will be the last example of a function based decorator. This one will use state and parameters
to show how decorators can work.  And the real power of decorators across a system. For this example
we'll create a "permission" decorator where we check if the person passed in has permissions to use the
function called.

The most important part to realize about a decorator that takes parameters, is the number of functions
involved. You have 4 functions involved:

1. The function being decorated
2. The decorator function
3. The inner function that is passed the `decorator` function
4. The wrapper function that uses `@wraps` and executes around the decorated function.

First look at the `h7_using_state_wrapper_and_params.py`. This may be confusing at first. What's
happening is the `requires_permission` is called as a regular function and passed `permission`. Then because
of the usage of `@` the result of calling `requires_permission` is called as a decorator.

Seen another way, this could be done without the `@` usage.

```python
def read_letter(person=None):
    print(f"{person} is reading a letter")

read_letter = requires_permission("read:letter")(read_letter)

read_letter("tyler")
```

The key is the function is really called twice in a row because of the usage of the `@` making it a decorator.

`@requires_permission("read:letter")` uses the return value as a function to be immediately called.

To see how this works to limit permissions, use the repl, like the below:

```python
(.venv) ➜  python-decorators-explained git:(main) ✗ ipython
Python 3.10.3 (main, May  4 2022, 09:22:28) [Clang 13.1.6 (clang-1316.0.21.2)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from h7_using_state_wrapper_and_params import read_letter

In [2]: read_letter("sayre")
---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
Input In [2], in <cell line: 1>()
----> 1 read_letter("sayre")

File ~/dev/garrypolley/python-decorators-explained/h7_using_state_wrapper_and_params.py:30, in requires_permission.<locals>.inner_func.<locals>.wrapper(person, *args, **kwargs)
     26     raise Exception(f"{person} does not have permission to {permission}")
     29 if permission not in requires_permission.permissions[person]:
---> 30     raise Exception(f"{person} does not have permission to {permission}")
     33 print("IN DECORATOR")
     34 print(f"CALLED BY {inspect.stack()[1][3]}")

Exception: sayre does not have permission to read:letter

In [3]: read_letter("garry")
IN DECORATOR
CALLED BY <cell line: 1>
garry is reading a letter
OUT DECORATOR


In [4]: read_letter("tyler")
IN DECORATOR
CALLED BY <cell line: 1>
tyler is reading a letter
OUT DECORATOR
```

Whenever the decorator encounters a person who does not have permission to read a letter it raises an
exception and _does not_ execute the decorated function. This is usually how most web applications manage
authorization to resources. It's usually easy to read, and allows you the developer to assume that once
your function is being executed, the person has permission to make the changes happening in your code.

Another way this parameterized decorator is useful is in data validation.  Looking at the bottom of the file
uncomment the `@requires_permission` decorator and see how it works.

```shell
(.venv) ➜  python-decorators-explained git:(main) ✗ python h7_using_state_wrapper_and_params.py
Traceback (most recent call last):
  File "/Users/garrypolley/dev/garrypolley/python-decorators-explained/h7_using_state_wrapper_and_params.py", line 66, in <module>
    @requires_permission("tear:letter")
  File "/Users/garrypolley/dev/garrypolley/python-decorators-explained/h7_using_state_wrapper_and_params.py", line 10, in requires_permission
    raise ValueError(f"{permission} is not a valid permission, choose from {valid_permissions}")
ValueError: tear:letter is not a valid permission, choose from ['read:letter', 'write:letter']
```

What happens is when the code is imported (which often happens during tests running) the decorator is
validating that the function definitions are correct. That means you can ensure no one tries to create
an invalid permission to check against.  Another example of how decorators can be pretty great.

Next up, we'll look at this same decorator, only as a class. When creating class based decorators, it
can be a bit more clear what's happening if you're familiar with classes.

### TBD: need to add class based example
