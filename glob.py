from .encoding import *
from .opcodes import *
from  leb128 import u as _u
uleb128 = _u.encode

class WasmGlobal:
    def __init__(self, data, type_: str, expression, mutable: bool):
        ref = data[0]
        name = "$%i" % ref if len(data) == 1 else data[1]
        self.ref = ref
        self.name = name
        self.type = types[type_]
        self.mutable = mutable
        self.expression = flatten([
            instructions[ins] if type(ins)==str else uleb128(ins) for ins in expression
        ])
    def export(self, name=None):
        if name is None:
             name = self.name
        return [*encode_string(name), exports["global"], self.ref]
    def global_(self):
        return [self.type, int(self.mutable), *flatten(self.expression), 0x0b]
