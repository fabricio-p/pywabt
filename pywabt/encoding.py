import leb128
from array import array
from .opcodes import sections
from .util import flatten, setup

def encode_vector(data):
	return bytes([
		*leb128.u.encode(len(data)),
		*flatten(data)
	])

def create_section(section_type, data):
	return bytes([
		sections[section_type],
		*encode_vector(data)
	])

def ieee754_f32(n):
	buf = array('f', bytes([0]) * 4)
	buf[0] = n
	return buf.tobytes()

def ieee754_f64(n):
    buf = array('d', bytes([0]) * 4)
    buf[0] = n
    return buf.tobytes()

def encode_string(string):
	return bytes([len(string), *bytes(string, 'utf-8')])

#print(vars())
setup(vars())

# TODO: Make leb128 internal. Avoid deps as much as possible
