import inspect

print("Module Loaded")

def running_function():
    """
    Example of a decorator function invoked later.
    """
    print(f"IN RUN FUNC")
    print(f"CALLED BY {inspect.stack()[1][3]}")

    return "Running Function Value"


def main_func():
    """
    Example of a main program having a decorator and then calling a decorator.
    """
    print("IN MAIN")
    running_function()
    print("OUT MAIN")

if __name__ == "__main__":
    main_func()
