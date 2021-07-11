from pathlib import Path
from io import BytesIO
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from pywabt import Module, opcodes
from unittest import TestCase, main
parent_dir = Path(__file__).resolve().parent.parent
class ModuleTest(TestCase):
	def test_module(self):
		module = Module("test")
		module.add_function("add", ['i32', 'i32'], ['i32'], [], [
			'get_local', 0,
			'get_local', 1,
			'i32.add'
		])
		module.add_global("foo", 'i32', False, ['i32.const', 69])
		module.add_export(0, 'function')
		with BytesIO() as out:
			module.write_to(out, close=False)
			# print(list(out.getbuffer().tobytes()))
			# print(list(module.create_buffer()))
			with open(str(parent_dir/'tmp/streamed.wasm'), 'wb') as streamed:
				streamed.write(out.getbuffer().tobytes())
			module.dump_binary(str(parent_dir/'tmp'), 'dumped')
			self.assertEqual(out.getbuffer().tobytes(),
							         module.create_buffer())
							 

if __name__ == "__main__":
	main()
