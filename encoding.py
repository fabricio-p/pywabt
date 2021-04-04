import leb128
from array import array
from .opcodes import sections
from .util import flatten, setup

def encode_vector(data):
    return [
        *leb128.u.encode(len(data)),
        *flatten([*data])
    ]

def create_section(section_type, data):
    return [
        sections[section_type],
        *encode_vector(data)
    ]

def ieee754(n):
    buf = array('f', bytes([0]) * 4)
    buf[0] = n
    return buf.tobytes()

def encode_string(string):
    return bytes([len(string), *bytes(string, 'utf-8')])

def uint8(n):
    if n < 0 or n > 255:
        raise Exception("Uint8 range 0..255")
    return bytes([n])

def uint32(n):
    if n < 0 or n > 4294967295:
        raise Exception("Uint32 range 0..4294967295")
    v = []
    for i in range(4):
        v[i] = n & 255
        n = n >> 8
    return v

def varint32(n):
    if n < -2147483648 or n > 2147483647:
        raise Exception("Varint32 range -2147483648..2147483647")
    return leb128.s.encode(n)

def varuint1(n):
    if not n in (0, 1):
        raise Exception("Varuint1 range 0..1")
    return leb128.u.encode(n)

def varuint7(n):
    if n < 0 or n > 127:
        raise Exception("Varuint7 range 0..127")
    return leb128.u.encode(n)

print(vars())
setup(vars())

# TODO: Make leb128 internal. Avoid deps as much as possible
