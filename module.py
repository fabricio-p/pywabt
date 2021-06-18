from .opcodes import (MAGIC_HEADER, MAGIC_VERSION, sections, types,
											instructions)
from .encoding import encode_vector, encode_string, create_section
from .function import WasmFunction
from .glob import WasmGlobal
from .type import WasmType
from os import getcwd
from collections import namedtuple
from typing import Optional, Union
import io

WasmExport = namedtuple('WasmExport', ['exported', 'name'])

class Module:
	"""
	class Module:
	The main (and only) container class for building WebAssembly modules.
	Use help(Module.(methodname)) for more info
	"""
	def __init__(self, name: str):
		self.name: str = name
		self.types: list[WasmType] = []
		self.functions: list[WasmFunction] = []
		self.globals: list[WasmGlobal] = []
		self.exports: list[WasmExport] = []
		self.header: bytes = bytes([*MAGIC_HEADER, *MAGIC_VERSION])
	
	def emit_binary(self, path: str = getcwd(), name: str = None):
		"""]
		Direclty emits the binary representation to the specified file.
		If the 'path' argument is not provided, it defaults to the current working directory.
		If the name argument is nof provided, it defaults to the name of the module
		"""
		name = self.name if name is None else name
		output = open("%s/%s.wasm" % (path, name), "wb")
		output.truncate()
		output.flush()
		output.write(self.create_buffer())
		output.close()
	
	def create_buffer(self):
		"""
		Spits out into memory the entire binary encoded module as a 'bytes' object
		"""
		return bytes([
			*self.header,
			*self.type_section(),
			*self.function_section(),
			*self.global_section(),
			*self.export_section(),
			*self.code_section(),
		])
	
	def generate_buffer(self):
		"""
		Generates the encoded sections one at time. The first 'bytes' object
		generated is the (magic) header.
		"""
		yield self.header
		yield self.type_section()
		yield self.function_section()
		yield self.global_section()
		yield self.export_section()
		yield self.code_section()
	
	def write_to(self, out, close=True):
		"""
		Streams the module while it is encoded into a file like object provided
		as the 'out' parameter. If the 'close' argument is True, the file will be
		closed as soon as the streaming ends.
		NOTE: The out parameter MUST be a seekable file like object.
		"""
		out.seek(0, io.SEEK_SET)
		out.truncate(0)
		out.write(self.header)
		out.write(self.type_section()
							if len(self.types) != 0 else b'')
		out.write(self.function_section()
							if len(self.functions) != 0 else b'')
		out.write(self.global_section()
							if len(self.globals) != 0 else b'')
		out.write(self.export_section()
							if len(self.exports) != 0 else b'')
		if len(self.functions) != 0:
			out.write(bytes([sections["code"], 0, len(self.functions)]))
			index = out.tell() - 2
			size = 1
			for function in self.functions:
				binary = function.code()
				size += len(binary)
				out.write(binary)
			out.seek(index, io.SEEK_SET)
			out.write(bytes([size]))
			out.tell()
			out.seek(0, io.SEEK_END)
		if close:
			out.close()
		return out
	
	def type_section(self):
		"""
		Encodes the type section of the module
		"""
		return create_section(
			"type",
			encode_vector([t.encode() for t in self.types]))
	
	def function_section(self):
		"""
		Encodes the function section of the module
		"""
		funcs = [f.ref for f in self.functions]
		return create_section(
			"function",
			encode_vector(funcs))
	
	def global_section(self):
		"""
		Encodes the global section of the module
		"""
		return create_section(
			"global",
			encode_vector([g.encode() for g in self.globals]))
	def generate_globals(self):
		"""
		Generates an encoded global at time
		"""
		for glob in self.globals:
			yield glob.encode()
	
	def export_section(self):
		"""
		Encodes the export section of the module
		"""
		return create_section(
			"export",
			encode_vector([e.exported.export(e.name) for e in self.exports]))
	
	def code_section(self):
		"""
		Encodes the code section of the module
		"""
		return create_section(
			"code",
			encode_vector([f.code() for f in self.functions]))
	def generate_codes(self):
		"""
		Generates the encoded function body of each function one at time
		"""
		for f in self.functions:
			yield f.code()
	
	def add_type(self, params: list[str], results: list[str]):
		"""
		Adds a type to the module.
		NOTE: Try not to use this method. it is use by the 'add_function' method
					to add types for new functions
		"""
		#nth = len(self.types)
		type_ = WasmType(params, results)
		self.types.append(type_)
		return type_
		
	def add_function(self, name: Optional[str], params: list[str],
			rets: list[str], locs: list[str], body: list[Union[str, int, float]]):
		"""
		Adds a function to the module.
		If 'name' is None it will be named by its reference/index. (see help(WasmFunction))
		'params' is a list of types of the params that the function will take.
		'rets' is a list of types or a string with the name of a type of the function's returns. If it is a list with more than 1 typename, the function has multiple returns, else it returns only once.
		'locs' is a list of the types of the function's locals. If empty, the function has no locals.
		'body' is the body of the function. See help(WasmFunction)
		"""
		fn_count = len(self.functions)
		#tp_count = len(self.types)
		fn_type = self.add_type(params, rets)
		fn = WasmFunction((fn_count, name), fn_type, locs, body)
		self.functions.append(fn)
		return self
	
	def add_export(self, name: Union[str, int], export_type: str,
		export_name: str = None):
		"""
	Adds a function or global to be exported.
	'name' is the identifier of which	function/global should be picekd. If it's an int, it will be used as index, else if it is a string, it will be used as the name.
	'export_type' determines the type of the export. Can be 'function' or 'global'.
		"""
		export = self.find(name, export_type)
		if export_name is None:
			export_name = export.name
		self.exports.append(WasmExport(export, export_name))
		# TODO: Finish docstrings
	def add_global(self, name, type_, mutable, expression):
		gl_count = len(self.globals)
		gl = WasmGlobal((gl_count, name), type_, expression, mutable)
		self.globals.append(gl)
	
	def find(self, ni, tp):
		if tp == "global":
			if isinstance(ni, int):
				return self.globals[ni]
			else:
				return list(filter(lambda g: g.name == ni, self.globals))[0]
		elif tp == "function":
			if isinstance(ni, int):
				return self.functions[ni]
			else:
				return list(filter(lambda f: f.name == ni, self.functions))[0]
		else:
			raise TypeError(("Export type '%s' does not exist or is " % tp) +
											 "not implemented yet")
	
	def call(self, name, args = []):
		byte_args = bytearray(flatten([eval_expression(arg) for arg in args]))
		byte_args.extend(bytes([instructions['call'],
					 self.find(name, "function")]))
		return bytes(byte_args)
	
	@classmethod
	def from_scheme(cls, scheme) -> 'Module':
		name, sections = scheme
		module = Module(name)
		for name, data in sections:
			pass
