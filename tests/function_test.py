from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from unittest import TestCase, main
from pynaryen.function import WasmFunction
from pynaryen.type import WasmType
from pynaryen.opcodes import types, instructions, exports

class WasmFunctionTest(TestCase):
	def setUp(self):
		self.function = WasmFunction((0, 'foo'), WasmType(['i32', 'i32'], 'i32'),
				[], [
					'get_local', 0,
					'get_local', 1,
					'i32.add'
				])
	def test_type(self):
		self.assertEqual(self.function.type(), bytes([types['func'],
																									2, types['i32'],
																										 types['i32'],
																									1, types['i32']]))
	def test_export(self):
		self.assertEqual(self.function.export(),
					           bytes([3, *b'foo', exports['function'], 0]))

if __name__ == "__main__":
    main()
