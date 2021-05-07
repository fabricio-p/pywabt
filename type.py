from .opcodes import instructions, types
from .encoding import encode_vector
from .util import eval_types
from dataclasses import dataclass
from typing import Union

@dataclass(order=True)
class WasmType(object):
    #index: int
    params: list[str]
    results: list[str]
    def encode(self, typetype='func'):
        return bytes([
            types[typetype],
            *encode_vector(eval_types(self.params)),
            *encode_vector(eval_types(self.results))
            ])
