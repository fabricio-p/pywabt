import os.path, sys
sys.path.append(os.path.expandvars("$HOME/python"))
from pynaryen import Module

module = Module("test")
module.add_function("add", ['i32', 'i32'], ['i32'], [], [
    'get_local', 0,
    'get_local', 1,
    'i32.add'
])
module.add_export(0, 'function')

# module.emit_binary(os.path.expandvars("$HOME/webassembly"))
with open(os.path.expandvars("$HOME/webassembly/test.wasm"), 'wb+') as out:
    module.write_to(out)

print("Finished")
