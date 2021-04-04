import leb128
uleb128 = leb128.u.encode
from .opcodes import instructions

global encode_vector
global ieee754

def setup(encoding):
    encode_vector = encoding["encode_vector"]
    ieee754 = encoding["ieee754"]
def eval_expression(expression) -> bytearray:
    return bytearray(flatten(list(map(eval_token, expression))))

def flatten(arr):
    return _concat([], arr)

def _concat(t, arrs):
    for arr in arrs:
        t.extend(arr if type(arr) in (list, tuple, bytes, bytearray) else [arr])
    return t

def eval_token(ins):
    if type(ins) == str:
        return uleb128(instructions[ins])
    elif type(ins) == float:
        return ieee754(ins)
    elif type(ins) == int:
        return uleb128(ins)
    else:
        return ins
