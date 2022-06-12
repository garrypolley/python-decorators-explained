#!/usr/bin/env python
import inspect
from functools import wraps

def decorator_with_wrapper_no_wraps(func):
    def wrapper():
        print("IN DECORATOR")
        print(f"CALLED BY {inspect.stack()[1][3]}")
        func()
        print("OUT DECORATOR\n")
    return wrapper

@decorator_with_wrapper_no_wraps
def running_function():
    """
    Example of a decorator function invoked later.
    """
    print(f"IN RUN FUNC")
    print(f"CALLED BY {inspect.stack()[1][3]}")

    return "I hope this is right"

def decorator_with_wraps(func):
    @wraps(func)
    def wrapper():
        print("IN DECORATOR")
        print(f"CALLED BY {inspect.stack()[1][3]}")
        func()
        print("OUT DECORATOR\n")
    return wrapper

@decorator_with_wraps
def running_function_with_wraps():
    """
    Example of a decorator function invoked later.
    """
    print(f"IN RUN FUNC")
    print(f"CALLED BY {inspect.stack()[1][3]}")

    return "I hope this is right"



def decorator_with_wraps_no_dec(func):
    def wrapper():
        print("IN DECORATOR")
        print(f"CALLED BY {inspect.stack()[1][3]}")
        func()
        print("OUT DECORATOR\n")
    return wraps(func)(wrapper)

@decorator_with_wraps_no_dec
def running_function_with_wraps_no_dec():
    """
    Example of a decorator function invoked later.
    """
    print(f"IN RUN FUNC")
    print(f"CALLED BY {inspect.stack()[1][3]}")

    return "I hope this is right"


def main():
    """
    Example of a main program having a decorator and then calling a decorator.
    """
    import sys
    if len(sys.argv) > 1 and  sys.argv[1] == "doit":
        print("showing the one with wraps")
        print(f"Calling the ____ {running_function_with_wraps.__name__} ____")
        running_function_with_wraps()

    print("IN MAIN")
    print(f"Calling the ____ {running_function.__name__} ____")
    running_function()
    print("OUT MAIN")



if __name__ == "__main__":
    main()
