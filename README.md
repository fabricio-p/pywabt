# Pynaryen
---
__Binaryen for python__
Pynaryen is a library that does the same as binaryen.
It is pretty minimal compared to the one in nodejs,
simply because it ia written from scratch, meanwhile
the nodejs library is transpiled from its C/C++ source
code into asm.js style javascript via emscripten.

It is included inside your project just as any python
library `import pynaryen`
### Module
The main building block is the **Module** class. It is
the representation of the WebAssembly module that you
will create. WebAssembly's tipical "Hello, world!" is
written as below:
```python
# importing
from pynaryen import Module
#		      module name
wasm_module = Module("pynaryen-tutorial")
#add function to module, name, function params, function returns
wasm_module.add_function("add", ['i32', 'i32'], ['i32'], [ # instructions
	'get_local', 0,
	'get_local', 1,
	'i32.add'
])
# exporting function (can also use the function's name instead of its index)
wasm_module.add_export(0, "function")
# emiting wasm binary
wasm_module.emit_binary()
```
### WasmFunction
It represents a WebAssembly function and is used by **Module**.
The **WasmFunction** class takes pretty much the same arguments as
the *add_function* method of the **Module** class but with one
difference, the firs argument is a two item _tuple_. The _tuple_'s
first item is the function's index in the wasm module and the
second (optional) is the functions label. The function exposes some
methods.
 - **type() -> bytes**
 	(returns its binary representation for the type section)
 - **export(name: str = self.name) -> bytes**
 	(returns its binary representation for the export section by using
	the provided argument as export name (defaults to the label you gave))
 - **code() -> bytes**
	(returns its instructions for the code section)
 - **add_instructions(instructions: list[str|int|float|bytes]) -> void**
	(adds other instructions to the functions if you're not finished)
### WasmGlobal
It represents a WebAssembly global. The **WasmGlobal** class takes 4 arguments
 1. A _tuple_ (like the first parameter of the **WasmFunction** class)
 2. The type ('i32' | 'i64' | 'f32' | 'f64')
 3. The expression that sets its value (like ['i32.const', 24])
 4. The global's mutability (True | False)
The class exposes some methods.
 - **export(name: str = self.name) -> bytes**
	(works like the **WasmFunction**'s _export_ method)
 - **global_() -> bytes**
	(works like **WasmFunction**'s _export_ method, but for global section)

