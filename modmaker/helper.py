import struct

def as_f32(x): return struct.pack('>f', float(x))
def as_f64(x): return struct.pack('>d', float(x))
