from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from pywabt.type import WasmType
from pywabt.opcodes import types
from unittest import TestCase, main

class WasmTypeTest(TestCase):
  def setUp(self):
    self.type = WasmType(['i32', 'f32', 'i64'], 'f64')
  def test_encode(self):
    self.assertEqual(self.type.encode(), bytes([types['func'],
                                                3, types['i32'],
                                                   types['f32'],
                                                   types['i64'],
                                                1, types['f64']]))

if __name__ == "__main__":
  main()
