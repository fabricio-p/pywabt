from .opcodes import MAGIC_HEADER, MAGIC_VERSION, sections, types, instructions
from .encoding import encode_vector, encode_string, create_section
from .function import WasmFunction
from .glob import WasmGlobal
from .type import WasmType
from os import getcwd
from collections import namedtuple
import io

WasmExport = namedtuple('WasmExport', ['exported', 'name'])

class Module:
    def __init__(self, name):
        self.name = name
        self.types = []
        self.functions = []
        self.globals = []
        self.exports = []
        self.header = [*MAGIC_HEADER, *MAGIC_VERSION]
    
    def emit_binary(self, path = getcwd(), name = None):
        name = self.name if name is None else name
        output = open("%s/%s.wasm" % (path, name), "wb")
        output.truncate()
        output.flush()
        output.write(self.create_buffer())
        output.close()
    
    def create_buffer(self):
        return bytes([
            *self.header,
            *self.type_section(),
            *self.function_section(),
            *self.global_section(),
            *self.export_section(),
            *self.code_section(),
        ])
    
    def generate_buffer(self):
        yield self.header
        yield self.type_section()
        yield self.function_section()
        yield self.global_section()
        yield self.export_section()
        yield self.code_section()
    
    def write_to(self, out, close=True):
        out.truncate(0)
        out.write(header)
        out.write(self.type_section())
        out.write(self.function_section())
        out.write(bytes(f'{sections["global"]}\0\0', 'utf-8'))
        size_index, size, length = out.tell() - 2, 0, 0
        for g in self.generate_globals():
            length += 1
            size += len(g)
            out.write(g)
        out.seek(size_index, io.SEEK_SET)
        out.write(bytes([size, length]))
        out.seek(0, io.SEEK_END)
        out.write(self.export_section())
        out.write(bytes(f'{sections["code"]}\0\0', 'utf-8'))
        size_index, size, length = out.tell() - 2, 0, 0
        for c in self.generate_codes():
            length += 1
            size = len(c)
            out.write(c)
        out.seek(size_index, io.SEEK_SET)
        out.write(bytes([size_length]))
        out.seek(0, io.SEEK_SET)
        if close:
            out.close()
        return out
    
    def type_section(self):
        return create_section(
                "type",
                encode_vector([t.encode() for t in self.types]))
    
    def function_section(self):
        funcs = [f.ref for f in self.functions]
        return create_section(
                "function",
                encode_vector(funcs))
    
    def global_section(self):
        return create_section(
                "global",
                encode_vector([g.encode() for g in self.globals]))
    def generate_globals(self):
        for glob in self.globals:
            yield g.encode()
    
    def export_section(self):
        return create_section(
                "export",
                encode_vector(
                    [e.exported.export(e.name) for e in self.exports]))
    
    def code_section(self):
        return create_section(
                "code",
                encode_vector([f.code() for f in self.functions]))
    
    def add_type(self, params, results):
        #nth = len(self.types)
        self.types.append(WasmType(params, results))
        
    def add_function(self, name, params, rets, locs, body):
        fn_count = len(self.functions)
        #tp_count = len(self.types)
        fn_type = WasmType(params, rets)
        fn = WasmFunction(
                (fn_count,) if name is None else (fn_count, name),
                fn_type,
                locs,
                body)
        self.types.append(fn_type)
        self.functions.append(fn)
        return self
    
    def add_export(self, name, export_type, export_name = None):
        export = self.find(name, export_type)
        if export_name is None:
            export_name = export.name
        self.exports.append(WasmExport(export, export_name))
    
    def add_global(self, name, type_, mutable, expression):
        gl_count = len(self.globals)
        gl = WasmGlobal(
                (gl_count,) if name is None else (gl_count, name),
                type_,
                expression,
                mutable)
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
            raise TypeError("Export type '%s' does not exist or is " % tp +
                    "not implemented yet")
    
    def call(self, name, args = []):
        byte_args = bytearray(flatten([eval_expression(arg) for arg in args]))
        byte_args.extend(bytes([instructions['call'], self.find(name, "function")]))
        return bytes(byte_args)
    
    @classmethod
    def from_scheme(cls, scheme) -> 'Module':
        name, sections = scheme
        module = Module(name)
        for name, data in sections:
            pass
