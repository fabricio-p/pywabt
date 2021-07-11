from .opcodes import instructions, types
from .encoding import encode_vector
from .util import eval_types
from typing import Union

class WasmType(object):
	def __init__(self, params: list[str], results: Union[list[str], str]):
		self.params = params
		self.results = results if isinstance(results, list) else [results]
	def encode(self, typetype='func'):
		return bytes([
			types[typetype],
			*encode_vector(eval_types(self.params)),
			*encode_vector(eval_types(self.results))
		])
