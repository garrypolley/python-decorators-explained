#!/usr/bin/env python
import inspect

print("Module Loaded")

def example_beginning_decorator(func):
    print("IN DECORATOR")
    print(f"CALLED BY {inspect.stack()[1][3]}")
    print(f"RETURNING {func.__name__}")
    print("OUT DECORATOR\n")
    return func

@example_beginning_decorator
def running_function():
    """
    Example of a decorator function invoked later.
    """
    print(f"IN RUN FUNC")
    print(f"CALLED BY {inspect.stack()[1][3]}")

    return "Running Function Value"


def main():
    """
    Example of a main program having a decorator and then calling a decorator.
    """
    print("IN MAIN")
    running_function()
    print("OUT MAIN")

if __name__ == "__main__":
    main()
