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
        self.type = types[type_]
        self.mutable = mutable
        self.expression = eval_expression(expression)
    def export(self, name=None):
        if name is None:
             name = self.name
        return bytes([*encode_string(name), exports["global"], self.ref])
    def global_(self):
        return bytes([self.type,
                int(self.mutable),
                *flatten(self.expression),
                instructions['wnd']])
