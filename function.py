from .encoding import *
from .opcodes import *

class WasmFunction:
    def __init__(self, data, arguments: list[str], returns: list[str], func_locals: list[str], body):
        ref = data[0]
        name = "$%i" % ref if len(data) == 1 else data[1]
        self.ref = ref
        self.name = "${}".format(ref) if name is None else name
        self.params = [types[arg] for arg in arguments]
        self.returns =[types[ret] for ret in  returns]
        self.locals = [types[loc] for loc in func_locals]
        self.body = flatten([instructions[ins] if type(ins) == str else ieee754(ins)if type(ins) == float else ins for ins in body])
    
    def type(self) -> list[int]:
        return [types["func"], *encode_vector(self.params), *encode_vector(self.returns)]
    
    def export(self, name: str = None) -> list[int]:
        if name is None:
            name = self.name
        return [*encode_string(name), exports["function"], self.ref]
    
    def code(self):
        return encode_vector(
                [*encode_vector(self.locals), *self.body, instructions["end"]])
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
        self.body.extend(
            flatten(
                [
                    instructions[ins] if type(ins) == str else ieee754(ins) if type(ins) == float else ins for ins in body]))
    # NOTE: Implement stuff here
    def __repr__(self):
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
        return fnc
