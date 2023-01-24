import types


def func_copy(f):
    return types.FunctionType(f.__code__, f.__globals__, None, f.__defaults__, f.__closure__)
