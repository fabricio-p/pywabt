from .encoding import *
from .opcodes import *
from .util import eval_expression
from .type import WasmType
from typing import Union, Optional

class WasmFunction:
	def __init__(self, data: tuple[int, Optional[str]],
      type_descriptor: WasmType, func_locals: list[str],
              body: list[Union[str, int, float]]):
		ref = data[0]
		self.name = "$%i" % ref if len(data) == 1 or data[1] is None else data[1]
		self.ref = ref
		self.types = type_descriptor
		self.locals = func_locals
		self.body = body
	
	def type(self) -> list[int]:
		return self.types.encode()
	
	def export(self, name: str = None) -> list[int]:
		if name is None:
			name = self.name
		return bytes([*encode_string(name), exports["function"], self.ref])
	
	def code(self):
		return encode_vector([
			*encode_vector(self.locals),
			*eval_expression(self.body),
			instructions["end"]])
	def type_text(self, indent):
		params = [type_name(t) for t in self.params]
		rtypes = [type_name(t) for t in self.returns]
		ind = ''.join([indent[0] for _ in range(indent[1])])
		return "%s(type $%s (param %s) %s)" % (
			ind,
			self.name,
			' '.join(params),
			"(result %s)" % (' '.join(rtypes),) if len(rtypes) > 0 else ''
		)
	def add_instructions(self, instr):
		self.body.extend(eval_expression(instr))
	# NOTE: Implement stuff here
	"""def __repr__(self):
		fnc = "%s(func $%s " % '\t', self.name
		fnc += "(param %s) " % ' '.join(list(map(type_name, self.types)))
		if len(self.returns) > 0:
			fnc += "(result %s)\n"%' '.join(list(map(type_name,self.returns)))
		else:
			fnc += '\n'
		for i in range(len(self.body)):
			ins = instruction_name(self.body[i])
			fnc += ins
			if gets_param(ins):
				count, prms = get_params(self.body, i, ins)
				i += count
				fnc += prms
		return fnc"""
