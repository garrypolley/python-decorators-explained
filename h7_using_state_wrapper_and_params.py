#!/usr/bin/env python
import inspect
from functools import wraps

valid_permissions = ["read:letter", "write:letter"]

def requires_permission(permission):

    if permission not in valid_permissions:
        raise ValueError(f"{permission} is not a valid permission, choose from {valid_permissions}")

    def inner_func(func):
        @wraps(func)
        def wrapper(person=None, *args, **kwargs):
            """
            The wrapper assumes the function will be passed a `person` first.

            Try this by removing the `person=None` -- there will be an exception and
            trace that may not make sense. However, it is correct because
            the usage of `@wraps` and the `inner_func`. This is where debugging
            decorators can get tricky, and why it's good to get a feel for how they
            work and why.
            """

            if person not in requires_permission.permissions:
                raise Exception(f"{person} does not have permission to {permission}")


            if permission not in requires_permission.permissions[person]:
                raise Exception(f"{person} does not have permission to {permission}")


            print("IN DECORATOR")
            print(f"CALLED BY {inspect.stack()[1][3]}")
            func(person, *args, **kwargs)
            print("OUT DECORATOR\n")
        return wrapper
    return inner_func

# Setup permissions to show the examples
requires_permission.permissions = {
    "garry": ["read:letter"],
    "tyler": ["read:letter", "write:letter"],
    "sayre": []
}

@requires_permission(permission="read:letter")
def read_letter(person=None):
    print(f"{person} is reading a letter")


@requires_permission(permission="write:letter")
def write_letter(person=None):
    print(f"{person} is writing a letter")

def main():
    """
    Example of a main program having a decorator and then calling a decorator.
    """
    print("IN MAIN")
    read_letter()
    print("OUT MAIN")



# @requires_permission("tear:letter")
# def this_will_error(person=None):
#     return "never hit because of error"



if __name__ == "__main__":
    main()
