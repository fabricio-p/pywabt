import leb128
uleb128 = leb128.u.encode
from .opcodes import instructions, types as typecodes

global encode_vector
global ieee754

def setup(encoding):
    encode_vector = encoding["encode_vector"]
    ieee754 = encoding["ieee754"]
def eval_expression(expression) -> bytearray:
    return bytearray(flatten(map(eval_token, expression)))
def eval_types(types):
    return list(map(typecodes.get, types))
def flatten(arr):
    return _concat([], arr)

def _concat(t, arrs):
    for arr in arrs:
        t.extend(arr if type(arr) in (list, tuple, bytes, bytearray) else [arr])
    return t

def trace(fn):
    def _fn(*args, **kwargs):
        return tracer(fn.__name__, fn(*args, **kwargs))
    return _fn

#@trace
def eval_token(ins):
    if isinstance(ins, str):
        return (#tracer("token is str",
                uleb128(instructions[ins]))
    elif isinstance(ins, float):
        return (#tracer("token is float",
                ieee754(ins))
    elif isinstance(ins, int):
        return (#tracer("token is int",
                uleb128(ins))
    else:
        return tracer(f"token is {type(ins)}", ins)
#
def tracer(message, data=""):
    print("{}: {}".format(message, data))
    return data
