from .opcodes import MAGIC_HEADER, MAGIC_VERSION, sections, types, instructions
from .encoding import encode_vector, encode_string, create_section
from .function import WasmFunction
from .glob import WasmGlobal
#from .export import WasmExport
from os import getcwd


class Module:
    def __init__(self, name):
        self.name = name
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
    
    def type_section(self):
        return create_section(
                "type",
                encode_vector([f.type() for f in self.functions]))
    
    def function_section(self):
        funcs = [f.ref for f in self.functions]
        return create_section(
                "function",
                encode_vector(funcs))
    
    def global_section(self):
        return create_section(
                "global",
                encode_vector([g.global_() for g in self.globals]))
    
    def export_section(self):
        return create_section(
                "export",
                encode_vector([e[0].export(e[1]) for e in self.exports]))
    
    def code_section(self):
        return create_section(
                "code",
                encode_vector([f.code() for f in self.functions]))
    def add_function(self, name, params, rets, locs, body):
        fn_count = len(self.functions)
        fn = WasmFunction(
                (fn_count,) if name is None else (fn_count, name),
                params,
                rets,
                locs,
                body)
        self.functions.append(fn)
        return self
    
    def add_export(self, name, export_type, export_name = None):
        export = self.find(name, export_type)
        if export_name is None:
            export_name = export.name
        self.exports.append((export, export_name))
    
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
            if type(ni) == int:
                return self.globals[ni]
            else:
                return list(filter(lambda g: g.name == ni, self.globals))[0]
        elif tp == "function":
            if type(ni) == int:
                return self.functions[ni]
            else:
                return list(filter(lambda f: f.name == ni, self.functions))[0]
        else:
            raise TypeError("Export type '%s' does not exist or is " % tp +
                    "not implemented yet")
