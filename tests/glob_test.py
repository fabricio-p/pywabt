import sys, os, pathlib
project_dir = pathlib.Path(__file__).parent.parent
sys.path.append(str(project_dir.parent))

from unittest import TestCase, main

from pywabt.glob import WasmGlobal
from pywabt import opcodes

class WasmGlobalTest(TestCase):
  def setUp(self):
    self.glob = WasmGlobal((0, 'a_global'), 'i32', ['i32.const', 69], False)
  def test_export(self):
    self.assertEqual(
        self.glob.export(),
        bytes([
                len('a_global'),
                *b'a_global',
                opcodes.exports["global"],
                0 # self.glob.ref
              ]))
  def test_encode(self):
    self.assertEqual(
        self.glob.encode(),
        bytes([
                opcodes.types['i32'],
                0, # immutable
                *bytes([opcodes.instructions['i32.const'], 69]),
                opcodes.instructions['end']
              ]))

if __name__ == "__main__":
  main()
