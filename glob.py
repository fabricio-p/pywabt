from .encoding import *
from .opcodes import *
from  leb128 import u as _u
from .util import eval_expression
uleb128 = _u.encode

class WasmGlobal:
    def __init__(self, data, type_: str, expression, mutable: bool):
        ref = data[0]
        name = "$%i" % ref if len(data) == 1 or data[1] is None else data[1]
        self.ref = ref
        self.name = name
        self.type = type_
        self.mutable = mutable
        self.expression = expression
    def export(self, name=None):
        if name is None:
             name = self.name
        return bytes([*encode_string(name), exports["global"], self.ref])
    def encode(self):
        return bytes([
                types[self.type],
                int(self.mutable),
                *flatten(eval_expression(self.expression)),
                instructions['end']
                ])
