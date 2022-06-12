#!/usr/bin/env python
import inspect

def decorator_with_wrapper(func):
    def wrapper():
        print("IN DECORATOR")
        print(f"CALLED BY {inspect.stack()[1][3]}")
        print(f"CALLING {func.__name__}")
        func() # -- this is executing the function
        print("OUT DECORATOR\n")
    return wrapper

@decorator_with_wrapper
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
