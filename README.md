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

from pynaryen import Module
wasm_module = Module("pynaryen-tutorial")
wasm_module.add_function("add", ['i32', 'i32'], ['i32'], [
	'get_local', 0,
	'get_local', 1,
	'i32.add'
])
wasm_module.add_export(0, "function")
wasm_module.emit_binary()
```
