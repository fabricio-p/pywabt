# PyWABT
---
__WebAssembly encoding for python__<br />
Pywabt is a library that makes WebAssembly binary encoding easy.
It works pretty much like.wabt.

It can be included inside your project just as any python
library by doing `import pywabt`
#### Module
The main building block is the **Module** class. It is the representation of
the WebAssembly module that you will create. The class takes only a parameter,
the modules name.
 1. :
```python
# importing
from pywabt import Module
#		      module name
wasm_module = Module("pywabt-tutorial")
#add function to module, name, function params, function returns
wasm_module.add_function("add", ['i32', 'i32'], ['i32'], [
	# instructions
	'get_local', 0,
	'get_local', 1,
	'i32.add'
])
# exporting function (can also use the function's name instead of its index)
wasm_module.add_export(0, "function")
# emiting wasm binary
wasm_module.emit_binary()
# You can also do wasm_module.write_to(open("pywabt-module.wasm", "wb+"))
```
This class exposes the following methods.
 - **emit_binary(path: str = os.getcwd(), name: str = None)**
 	(dumps the encoded content of the module to the file with the path as `path` and name as `name`.
	if `path` is not provided, it defaults to the current working directory.
	if `name` is `None`, it defaults to the current module's name)
 - **create_buffer() -> bytes**
 	(returns the `bytes` object of the encoded module)
 - **generate_module()**
	(returns a generator that yields a section at a time)
 - **write_to(out: IO, close: bool = True) -> IO**
 	(stream-writes while encoding the module to the provided `IO` object.
	if `close` is `True`, the `IO` object will be closed.
	returns the first parameter)
 - **type_section() -> bytes**
 	(returns the encoded type section of the module)
 - **function_section() -> bytes**
 	(returns the encoded function section of the module)
 - **global_section() -> bytes**
	(returns the encoded global section of the module)
 - **export_section() ->bytes**
 	(returns the encoded export section of the module)
 - **code_section() -> bytes**
 	(returns fhe encoded code section of the module)
 - **generate_globals() -> Generator[bytes]**
 	(yields an encoded global at a time)
 - **generate_codes() -> Generator[bytes]**
 	(yields the encoded body of each function one at a time)
 - **add_type(params: list[str], results: list[str])**
 	(adds a type to the module.
	each item of each `list` must be either 'i32', 'i64', 'f32', 'f64')
 - **add_function(name: Optional[str], params: list[str], rets: list[str],
 		  locs: list[str], body: list[Union[str, int, float]])**
	(adds a function to the module.
	the `params` and `rets` are the same as `params` and `results` of the **add_type** method.
	the `locs` parameter follows the same rules as `name` or `rets`, but uit is for the function locals.
	the body is a list containing string literals for the instructions, integers and floats for numbers)
 - **add_export(name: Union[str, int], export_type: str, export_name: str)**
 	(adds an export to the module.
	the `name` must be the index or the name that you gave to a function or gloabal that you added to the module.
	the `export_type` indicates if the export is a function or global, must be 'global' or 'function'.
	the `export_name` is the name of the export. will default to the function's or global's name tht you are exporting)

#### WasmFunction
It represents a WebAssembly function and is used by **Module**.
The **WasmFunction** class takes pretty much the same arguments as
the *add_function* method of the **Module** class but with one
difference, the firs argument is a two item _tuple_. The _tuple_'s
first item is the function's index in the wasm module and the
second (optional) is the functions label. The class exposes the following
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
#### WasmGlobal
It represents a WebAssembly global. The **WasmGlobal** class takes 4 arguments
 1. A _tuple_ (like the first parameter of the **WasmFunction** class)
 2. The type ('i32' | 'i64' | 'f32' | 'f64')
 3. The expression that sets its value (like ['i32.const', 24])
 4. The global's mutability (True | False)
The class exposes the following methods.
 - **export(name: str = self.name) -> bytes**
	(works like the __WasmFunction__'s _export_ method)
 - **encode() -> bytes**
	(works like **WasmFunction**'s _export_ method, but for global section)
#### WasmType
An WebAssembly function type container used only for easier encoding. The **WasmType** class takes 2 arguments.
 1. A _list_ of the names of the types of the parameters that the function will take.
 2. A _list_ of the names of the types of the function's results. If the function has only one result, a *str*ing with the type's name can be passed.
