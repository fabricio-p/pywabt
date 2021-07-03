from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from unittest import TestCase, main
from pywabt.encoding import (encode_vector, create_section,
                              ieee754_f32, encode_string)
from pywabt.opcodes import sections

class EncodingTest(TestCase):
  def test_encode_vector(self):
    self.assertEqual(encode_vector([8, 24, [44, 34], bytes([13, 65, 12])]),
                     bytes([4, 8, 24, 44, 34, 13, 65, 12]))
  def test_create_section(self):
    self.assertEqual(create_section('code', [bytes([24, 23]),
                                             bytes([24, 112, 54]),
                                             bytes([34, 98])]),
                     bytes([sections['code'], 3, 24, 23, 24,
                                              112, 54, 34, 98]))
  def test_ieee754(self):
    self.assertEqual(ieee754_f32(4.5), bytes([0, 0, 144, 64]))
  def test_encode_string(self):
    self.assertEqual(encode_string("Hello, World!"), b'\x0dHello, World!')

if __name__ == "__main__":
  main()
