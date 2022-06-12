import inspect



def decorator_with_state(func):
    print(f"Decorator used with {func.__name__}")
    decorator_with_state.called_functions.append(func.__name__)
    return func


# Keep track of the called functions
# Oh, and you can add state to functions by just "slapping on"
# an attribute
decorator_with_state.called_functions = []


@decorator_with_state
def func_1():
    print("IN FUNC 1")
    return "hi"


@decorator_with_state
def func_2():
    print("IN FUNC 2")
    return "hi"


@decorator_with_state
def func_3():
    print("IN FUNC 3")
    return "hi"

@decorator_with_state
def func_4():
    print("IN FUNC 4")
    return "hi"


def main_func():
    print("IN MAIN")
    func_1()
    func_2()
    func_3()
    func_4()
    print("OUT MAIN")


if __name__ == "__main__":
    main_func()
