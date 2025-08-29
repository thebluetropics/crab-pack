from sys import (exit, stderr)
from . import utf8

def bind_to_constant_pool():
	pass

def get_utf8(cp, i):
	for entry in cp:
		if entry[0].__eq__(i):
			if entry[1].__eq__(b"\x01"):
				return utf8.decode(entry[3])

	return None

def vcp_utf8_get(cp, i):
	if type(i) is bytes:
		pass

	for entry in cp:
		if entry[0].__eq__(i):
			if entry[1].__eq__(b"\x01"):
				return utf8.decode(entry[3])

	return None

def ecp_get(cp, i):
	for entry in cp:
		if entry[0].__eq__(i):
			return entry

	print("Err: can't find specified entry.")
	exit(1)

def icp_utf8_get(cp, s0):
	for entry in cp:
		if entry[1].__eq__(b"\x01"):
			s1 = utf8.decode(entry[3])

			if s0.__eq__(s1):
				return entry[0]

	print("Err: can't find specified utf-8 entry.")
	exit(1)

def i2cp_utf8_get(cp, s0):
	for entry in cp:
		if entry[1].__eq__(b"\x01"):
			s1 = utf8.decode(entry[3])

			if s0.__eq__(s1):
				return entry[0].to_bytes(2)

	print("Err: can't find specified utf-8 entry.")
	exit(1)

def icp_class_get(cp, class_name):
	for entry in cp:
		if entry[1].__eq__(b"\x07"):
			i, _, i2cp_to_utf8 = entry
			vcp_utf8 = vcp_utf8_get(cp, int.from_bytes(i2cp_to_utf8))

			if vcp_utf8.__eq__(class_name):
				return i

	print("Err: can't find specified class entry.")
	exit(1)

def i2cp_class_get(cp, class_name):
	return icp_class_get(cp, class_name).to_bytes(2)

def icp_f_get(cp, owner, name, desc):
	for entry in cp:
		if entry[1].__eq__(b"\x09"):
			i, *_ = entry
			icp_to_class = int.from_bytes(entry[2][0:2])
			icp_to_ntp = int.from_bytes(entry[2][2:4])

			ecp_class = ecp_get(cp, icp_to_class)
			icp_utf8_0 = int.from_bytes(ecp_class[2])
			vcp_utf8_0 = vcp_utf8_get(cp, icp_utf8_0)

			if not owner.__eq__(vcp_utf8_0):
				continue

			ecp_ntp = ecp_get(cp, icp_to_ntp)
			icp_utf8_1 = int.from_bytes(ecp_ntp[2][0:2])
			vcp_utf8_1 = vcp_utf8_get(cp, icp_utf8_1)

			if not name.__eq__(vcp_utf8_1):
				continue

			icp_utf8_2 = int.from_bytes(ecp_ntp[2][2:4])
			vcp_utf8_2 = vcp_utf8_get(cp, icp_utf8_2)

			if not desc.__eq__(vcp_utf8_2):
				continue

			return i

	print("Err: can't find specified field reference entry.")
	exit(1)

def i2cp_f_get(cp, owner, name, desc):
	return icp_f_get(cp, owner, name, desc).to_bytes(2)

def icp_m_get(cp, owner, name, desc):
	for entry in cp:
		if entry[1].__eq__(b"\x0a"):
			i, *_ = entry
			icp_to_class = int.from_bytes(entry[2][0:2])
			icp_to_ntp = int.from_bytes(entry[2][2:4])

			ecp_class = ecp_get(cp, icp_to_class)
			icp_utf8_0 = int.from_bytes(ecp_class[2])
			vcp_utf8_0 = vcp_utf8_get(cp, icp_utf8_0)

			if not owner.__eq__(vcp_utf8_0):
				continue

			ecp_ntp = ecp_get(cp, icp_to_ntp)
			icp_utf8_1 = int.from_bytes(ecp_ntp[2][0:2])
			vcp_utf8_1 = vcp_utf8_get(cp, icp_utf8_1)

			if not name.__eq__(vcp_utf8_1):
				continue

			icp_utf8_2 = int.from_bytes(ecp_ntp[2][2:4])
			vcp_utf8_2 = vcp_utf8_get(cp, icp_utf8_2)

			if not desc.__eq__(vcp_utf8_2):
				continue

			return i

	print("Err: can't find specified method reference entry.")
	exit(1)

def i2cp_m_get(cp, owner, name, desc):
	return icp_m_get(cp, owner, name, desc).to_bytes(2)

class ConstantPoolHelper:
	def __init__(self, cf):
		self.cf = cf
		self.idx_cache = {}
		self.cache = {}

def use_helper(cf):
	cp = ConstantPoolHelper(cf)

	for entry in cf[0x04]:
		cp.idx_cache[entry[0]] = entry

	for entry in cf[0x04]:
		if entry[1].__eq__(b'\x01'):
			cp.cache[(0x01, utf8.decode(entry[3]))] = entry[0]

	for entry in cf[0x04]:
		if entry[1].__eq__(b'\x07'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp.idx_cache[int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8.decode(ecp_utf8[3])
			cp.cache[(0x07, vcp_utf8)] = i
			continue

		if entry[1].__eq__(b'\x08'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp.idx_cache[int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8.decode(ecp_utf8[3])
			cp.cache[(0x08, vcp_utf8)] = i
			continue

		if entry[1].__eq__(b'\x0c'):
			i = entry[0]
			ecp_name = cp.idx_cache[int.from_bytes(entry[2][0:2])]
			ecp_type = cp.idx_cache[int.from_bytes(entry[2][2:4])]
			name_string = utf8.decode(ecp_name[3])
			type_string = utf8.decode(ecp_type[3])
			cp.cache[(0x0c, name_string, type_string)] = i
			continue

	for entry in cf[0x04]:
		if entry[1].__eq__(b'\x09'):
			i = entry[0]
			ecp_class = cp.idx_cache[int.from_bytes(entry[2][0:2])]
			ecp_name_and_type = cp.idx_cache[int.from_bytes(entry[2][2:4])]
			ecp_class_utf8 = cp.idx_cache[int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp.idx_cache[int.from_bytes(ecp_name_and_type[2][0:2])]
			ecp_type_utf8 = cp.idx_cache[int.from_bytes(ecp_name_and_type[2][2:4])]

			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp.cache[(0x09, class_string, name_string, type_string)] = i
			continue

		if entry[1].__eq__(b'\x0a'):
			i = entry[0]
			ecp_class = cp.idx_cache[int.from_bytes(entry[2][0:2])]
			ecp_name_and_type = cp.idx_cache[int.from_bytes(entry[2][2:4])]
			ecp_class_utf8 = cp.idx_cache[int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp.idx_cache[int.from_bytes(ecp_name_and_type[2][0:2])]
			ecp_type_utf8 = cp.idx_cache[int.from_bytes(ecp_name_and_type[2][2:4])]

			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp.cache[(0x0a, class_string, name_string, type_string)] = i
			continue

	return cp

def icpx_utf8(cp, value):
	if (0x01, value) in cp.cache:
		return cp.cache[(0x01, value)]

	rcp = cp.cf[0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x01', len(value).to_bytes(2), utf8.encode(value)])
	cp.idx_cache[i] = rcp[-1]
	cp.cf[0x03] = (i + 1).to_bytes(2)
	cp.cache[(0x01, value)] = i

	return i

def i2cpx_utf8(cp, value): return icpx_utf8(cp, value).to_bytes(2)

def icpx_c(cp, internal_name):
	if (0x07, internal_name) in cp.cache:
		return cp.cache[(0x07, internal_name)]

	icp_utf8 = icpx_utf8(cp, internal_name)

	rcp = cp.cf[0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x07', icp_utf8.to_bytes(2)])
	cp.idx_cache[i] = rcp[-1]
	cp.cf[0x03] = (i + 1).to_bytes(2)
	cp.cache[(0x07, internal_name)] = i

	return i

def i2cpx_c(cp, internal_name): return icpx_c(cp, internal_name).to_bytes(2)

def icpx_string(cp, value):
	if (0x08, value) in cp.cache:
		return cp.cache[(0x08, value)]

	icp_utf8 = icpx_utf8(cp, value)

	rcp = cp.cf[0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x08', icp_utf8.to_bytes(2)])
	cp.idx_cache[i] = rcp[-1]
	cp.cf[0x03] = (i + 1).to_bytes(2)
	cp.cache[(0x08, value)] = i

	return i

def i2cpx_string(cp, value): return icpx_string(cp, value).to_bytes(2)

def icpx_name_and_type(cp, name, desc):
	if (0x0c, name, desc) in cp.cache:
		return cp.cache[(0x0c, name, desc)]

	icp_name = icpx_utf8(cp, name)
	icp_type = icpx_utf8(cp, desc)

	rcp = cp.cf[0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x0c', icp_name.to_bytes(2) + icp_type.to_bytes(2)])
	cp.idx_cache[i] = rcp[-1]
	cp.cf[0x03] = (i + 1).to_bytes(2)
	cp.cache[(0x0c, name, desc)] = i

	return i

def i2cpx_name_and_type(cp, name, desc): return icpx_name_and_type(cp, name, desc).to_bytes(2)

def icpx_f(cp, owner, name, desc):
	if (0x09, owner, name, desc) in cp.cache:
		return cp.cache[(0x09, owner, name, desc)]

	icp_class = icpx_c(cp, owner)
	icp_name_and_type = icpx_name_and_type(cp, name, desc)

	rcp = cp.cf[0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x09', icp_class.to_bytes(2) + icp_name_and_type.to_bytes(2)])
	cp.idx_cache[i] = rcp[-1]
	cp.cf[0x03] = (i + 1).to_bytes(2)
	cp.cache[(0x09, owner, name, desc)] = i

	return i

def i2cpx_f(cp, owner, name, desc): return icpx_f(cp, owner, name, desc).to_bytes(2)

def icpx_m(cp, owner, name, desc):
	if (0x0a, owner, name, desc) in cp.cache:
		return cp.cache[(0x0a, owner, name, desc)]

	icp_class = icpx_c(cp, owner)
	icp_name_and_type = icpx_name_and_type(cp, name, desc)

	rcp = cp.cf[0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x0a', icp_class.to_bytes(2) + icp_name_and_type.to_bytes(2)])
	cp.idx_cache[i] = rcp[-1]
	cp.cf[0x03] = (i + 1).to_bytes(2)
	cp.cache[(0x0a, owner, name, desc)] = i

	return i

def i2cpx_m(cp, owner, name, desc): return icpx_m(cp, owner, name, desc).to_bytes(2)
