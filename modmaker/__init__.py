import struct
from sys import exit, stderr

def utf8_decode(utf8_b):
	decoded = []

	i = 0

	while i < len(utf8_b):
		byte = utf8_b[i]

		if byte < 0x80:
			decoded.append(chr(byte))
			i += 1
		elif (byte & 0xE0).__eq__(0xC0):
			b1 = utf8_b[i + 1]

			if byte.__eq__(0xC0) and b1.__eq__(0x80):
				decoded.append('\u0000')
			else:
				decoded.append(chr(((byte & 0x1F) << 6) | (b1 & 0x3F)))

			i += 2
		elif (byte & 0xF0).__eq__(0xE0):
			b1 = utf8_b[i + 1]
			b2 = utf8_b[i + 2]

			code_unit = ((byte & 0x0F) << 12) | ((b1 & 0x3F) << 6) | (b2 & 0x3F)

			decoded.append(chr(code_unit))

			i += 3

	return str().join(decoded)

def utf8_encode(string):
	encoded = bytearray()

	for chr in string:
		code_point = ord(chr)

		if code_point.__eq__(0x0000):
			encoded.append(b'\xc0\x80')
		elif code_point < 0x007f or code_point.__eq__(0x007f):
			encoded.append(code_point)
		elif code_point < 0x07ff or code_point.__eq__(0x07ff):
			encoded.append(0xC0 | ((code_point >> 6) & 0x1F))
			encoded.append(0x80 | (code_point & 0x3F))
		else:
			encoded.append(0xE0 | ((code_point >> 12) & 0x0F))
			encoded.append(0x80 | ((code_point >> 6) & 0x3F))
			encoded.append(0x80 | (code_point & 0x3F))

	return bytes(encoded)

def cf_load(cf_b):
	cf = [None] * 16

	cf[0x00] = cf_b[0:4]
	cf[0x01] = cf_b[4:6]
	cf[0x02] = cf_b[6:8]

	cf[0x03] = cf_b[8:10]
	cp_count = int.from_bytes(cf[0x03])

	cf[0x04] = []
	cp = cf[0x04]

	i = 10
	j = 1

	while j < cp_count:
		tag = cf_b[i:i + 1]

		if tag.__eq__(b'\x07'):
			cp.append([j, tag, cf_b[i + 1:i + 3]])
			i += 3
			j += 1
			continue

		if tag.__eq__(b'\x09'):
			cp.append([j, tag, cf_b[i + 1:i + 3], cf_b[i + 3:i + 5]])
			i += 5
			j += 1
			continue

		if tag.__eq__(b'\x0a'):
			cp.append([j, tag, cf_b[i + 1:i + 3], cf_b[i + 3:i + 5]])
			i += 5
			j += 1
			continue

		if tag.__eq__(b'\x0b'):
			cp.append([j, tag, cf_b[i + 1:i + 3], cf_b[i + 3:i + 5]])
			i += 5
			j += 1
			continue

		if tag.__eq__(b'\x08'):
			cp.append([j, tag, cf_b[i + 1:i + 3]])
			i += 3
			j += 1
			continue

		if tag.__eq__(b'\x03'):
			cp.append([j, tag, cf_b[i + 1:i + 5]])
			i += 5
			j += 1
			continue

		if tag.__eq__(b'\x04'):
			cp.append([j, tag, cf_b[i + 1:i + 5]])
			i += 5
			j += 1
			continue

		if tag.__eq__(b'\x05'):
			cp.append([j, tag, cf_b[i + 1:i + 9]])
			i += 9
			j += 2
			continue

		if tag.__eq__(b'\x06'):
			cp.append([j, tag, cf_b[i + 1:i + 9]])
			i += 9
			j += 2
			continue

		if tag.__eq__(b'\x0c'):
			cp.append([j, tag, cf_b[i + 1:i + 3], cf_b[i + 3:i + 5]])
			i += 5
			j += 1
			continue

		if tag.__eq__(b'\x01'):
			sz_b = cf_b[i + 1:i + 3]
			sz = int.from_bytes(sz_b)
			cp.append([j, tag, sz_b, cf_b[i + 3:i + 3 + sz]])
			i += 3 + sz
			j += 1
			continue

		if tag.__eq__(b'\x0f'):
			cp.append([j, tag, cf_b[i + 1:i + 2], cf_b[i + 2:i + 4]])
			i += 4
			j += 1
			continue

		if tag.__eq__(b'\x10'):
			cp.append([j, tag, cf_b[i + 1:i + 3]])
			i += 3
			j += 1
			continue

		if tag.__eq__(b'\x12'):
			cp.append([j, tag, cf_b[i + 1:i + 3], cf_b[i + 3:i + 5]])
			i += 5
			j += 1
			continue

		print('Err: unknown.', file=stderr)
		exit(1)

	cf[0x05] = cf_b[i:i + 2]
	cf[0x06] = cf_b[i + 2:i + 4]
	cf[0x07] = cf_b[i + 4:i + 6]

	cf[0x08] = cf_b[i + 6:i + 8]
	if_count = int.from_bytes(cf[0x08])

	i += 8

	cf[0x09] = []
	interfaces = cf[0x09]

	for _ in range(if_count):
		interfaces.append(cf_b[i:i + 2])
		i += 2

	cf[0x0a] = cf_b[i:i + 2]
	f_count = int.from_bytes(cf[0x0a])

	i += 2

	cf[0x0b] = []
	fields = cf[0x0b]

	for _ in range(f_count):
		f = [
			cf_b[i:i + 2],
			cf_b[i + 2:i + 4],
			cf_b[i + 4:i + 6],
			None,
			None
		]

		a_count_b = cf_b[i + 6:i + 8]
		f[0x03] = a_count_b

		i += 8

		a_count = int.from_bytes(a_count_b)

		a_list = []
		f[0x04] = a_list

		for _ in range(a_count):
			a = [
				cf_b[i:i + 2],
				cf_b[i + 2:i + 6],
				None
			]
			sz = int.from_bytes(a[0x01])
			a[0x02] = cf_b[i + 6:i + 6 + sz]
			a_list.append(a)
			i += 6 + sz

		fields.append(f)

	cf[0x0c] = cf_b[i:i + 2]
	m_count = int.from_bytes(cf[0x0c])

	i += 2

	cf[0x0d] = []
	methods = cf[0x0d]

	for _ in range(m_count):
		m = [
			cf_b[i:i + 2],
			cf_b[i + 2:i + 4],
			cf_b[i + 4:i + 6],
			None,
			None
		]

		a_count_b = cf_b[i + 6:i + 8]
		m[0x03] = a_count_b

		i += 8

		a_count = int.from_bytes(a_count_b)

		a_list = []
		m[0x04] = a_list

		for _ in range(a_count):
			a = [
				cf_b[i:i + 2],
				cf_b[i + 2:i + 6],
				None
			]
			sz = int.from_bytes(a[0x01])
			a[0x02] = cf_b[i + 6:i + 6 + sz]
			a_list.append(a)
			i += 6 + sz

		methods.append(m)

	cf[0x0e] = cf_b[i:i + 2]
	a_count = int.from_bytes(cf[0x0e])

	i += 2

	cf[0x0f] = []
	attrs = cf[0x0f]

	for _ in range(a_count):
		a = [
			cf_b[i:i + 2],
			cf_b[i + 2:i + 6],
			None
		]
		sz = int.from_bytes(a[0x01])
		a[0x02] = cf_b[i + 6:i + 6 + sz]
		attrs.append(a)
		i += 6 + sz

	return cf

def load_class_file(path):
	file = open(path, 'rb')
	cf = cf_load(file.read())
	file.close()
	return cf

def cf_assemble(cf):
	cf_b = bytearray()

	cf_b.extend(cf[0x00])
	cf_b.extend(cf[0x01])
	cf_b.extend(cf[0x02])
	cf_b.extend(cf[0x03])

	for entry in cf[0x04]:
		cf_b.extend(b''.join(entry[1:]))

	cf_b.extend(cf[0x05])
	cf_b.extend(cf[0x06])
	cf_b.extend(cf[0x07])
	cf_b.extend(cf[0x08])

	for inf in cf[0x09]:
		cf_b.extend(inf)

	cf_b.extend(cf[0x0a])

	for f in cf[0x0b]:
		cf_b.extend(b''.join(f[0x00:0x04]))

		for a in f[0x04]:
			cf_b.extend(b''.join(a))

	cf_b.extend(cf[0x0c])

	for m in cf[0x0d]:
		cf_b.extend(b''.join(m[0x00:0x04]))

		for a in m[0x04]:
			cf_b.extend(b''.join(a))

	cf_b.extend(cf[0x0e])

	for a in cf[0xf]:
		cf_b.extend(b''.join(a))

	cf_b = bytes(cf_b)
	return cf_b

def cf_create():
	cf = [None] * 16

	cf[0x00] = b'\xca\xfe\xba\xbe'
	cf[0x01], cf[0x02] = [(0).to_bytes(2), (52).to_bytes(2)]

	cf[0x03] = (0).to_bytes(2)
	cf[0x04] = []

	cf[0x05] = (0).to_bytes(2)
	cf[0x06] = (0).to_bytes(2)
	cf[0x07] = (0).to_bytes(2)

	cf[0x08] = (0).to_bytes(2)
	cf[0x09] = []

	cf[0x0a] = (0).to_bytes(2)
	cf[0x0b] = []

	cf[0x0c] = (0).to_bytes(2)
	cf[0x0d] = []

	cf[0x0e] = (0).to_bytes(2)
	cf[0x0f] = []

	return cf

def cp_init_cache(cp):
	cp_cache = ({}, {})

	for entry in cp:
		cp_cache[0][entry[0]] = entry

	for entry in cp:
		if entry[1].__eq__(b'\x01'):
			cp_cache[1][(0x01, utf8_decode(entry[3]))] = entry[0]

		if entry[1].__eq__(b'\x03'):
			cp_cache[1][(0x03, int.from_bytes(entry[2]))] = entry[0]

		if entry[1].__eq__(b'\x04'):
			cp_cache[1][(0x04, entry[2])] = entry[0]

		if entry[1].__eq__(b'\x05'):
			cp_cache[1][(0x05, int.from_bytes(entry[2]))] = entry[0]

		if entry[1].__eq__(b'\x06'):
			cp_cache[1][(0x06, entry[2])] = entry[0]

	for entry in cp:
		if entry[1].__eq__(b'\x07'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp_cache[0][int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8_decode(ecp_utf8[3])
			cp_cache[1][(0x07, vcp_utf8)] = i

			continue

		if entry[1].__eq__(b'\x08'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp_cache[0][int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8_decode(ecp_utf8[3])
			cp_cache[1][(0x08, vcp_utf8)] = i

			continue

		if entry[1].__eq__(b'\x0c'):
			i = entry[0]
			ecp_name = cp_cache[0][int.from_bytes(entry[2])]
			ecp_type = cp_cache[0][int.from_bytes(entry[3])]
			name_string = utf8_decode(ecp_name[3])
			type_string = utf8_decode(ecp_type[3])
			cp_cache[1][(0x0c, name_string, type_string)] = i

			continue

	for entry in cp:
		if entry[1].__eq__(b'\x09'):
			i = entry[0]
			ecp_class = cp_cache[0][int.from_bytes(entry[2])]
			ecp_name_and_type = cp_cache[0][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp_cache[0][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[3])]
			class_string = utf8_decode(ecp_class_utf8[3])
			name_string = utf8_decode(ecp_name_utf8[3])
			type_string = utf8_decode(ecp_type_utf8[3])
			cp_cache[1][(0x09, class_string, name_string, type_string)] = i

			continue

		if entry[1].__eq__(b'\x0a'):
			i = entry[0]
			ecp_class = cp_cache[0][int.from_bytes(entry[2])]
			ecp_name_and_type = cp_cache[0][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp_cache[0][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[3])]
			class_string = utf8_decode(ecp_class_utf8[3])
			name_string = utf8_decode(ecp_name_utf8[3])
			type_string = utf8_decode(ecp_type_utf8[3])
			cp_cache[1][(0x0a, class_string, name_string, type_string)] = i

			continue

		if entry[1].__eq__(b'\x0b'):
			i = entry[0]
			ecp_class = cp_cache[0][int.from_bytes(entry[2])]
			ecp_name_and_type = cp_cache[0][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp_cache[0][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[3])]
			class_string = utf8_decode(ecp_class_utf8[3])
			name_string = utf8_decode(ecp_name_utf8[3])
			type_string = utf8_decode(ecp_type_utf8[3])
			cp_cache[1][(0x0b, class_string, name_string, type_string)] = i

			continue

	return cp_cache

def get_ecp_type_at(cp_cache, i):
	entry = cp_cache[0][i]
	tag = entry[1]

	return tag

def get_float_at(cp_cache, i):
	entry = cp_cache[0][i]

	if not entry[1].__eq__(b'\x04'):
		print('Err: no float found.', file=stderr)
		exit(1)

	return entry[2]

def get_double_at(cp_cache, i):
	entry = cp_cache[0][i]

	if not entry[1].__eq__(b'\x06'):
		print('Err: no double found.', file=stderr)
		exit(1)

	return entry[2]

def get_field_reference_at(cp_cache, i):
	entry = cp_cache[0][i]

	if not entry[1].__eq__(b'\x09'):
		print('Err: no field reference found.', file=stderr)
		exit(1)

	ecp_class = cp_cache[0][int.from_bytes(entry[2])]
	ecp_name_and_type = cp_cache[0][int.from_bytes(entry[3])]
	ecp_class_utf8 = cp_cache[0][int.from_bytes(ecp_class[2])]
	ecp_name_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[2])]
	ecp_type_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[3])]
	class_name = utf8_decode(ecp_class_utf8[3])
	name = utf8_decode(ecp_name_utf8[3])
	desc = utf8_decode(ecp_type_utf8[3])

	return (class_name, name, desc)

def get_method_reference_at(cp_cache, i):
	entry = cp_cache[0][i]

	if not entry[1].__eq__(b'\x0a'):
		print('Err: no method reference found.', file=stderr)
		exit(1)

	ecp_class = cp_cache[0][int.from_bytes(entry[2])]
	ecp_name_and_type = cp_cache[0][int.from_bytes(entry[3])]
	ecp_class_utf8 = cp_cache[0][int.from_bytes(ecp_class[2])]
	ecp_name_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[2])]
	ecp_type_utf8 = cp_cache[0][int.from_bytes(ecp_name_and_type[3])]
	class_name = utf8_decode(ecp_class_utf8[3])
	name = utf8_decode(ecp_name_utf8[3])
	desc = utf8_decode(ecp_type_utf8[3])

	return (class_name, name, desc)

def get_utf8_at(cp_cache, i):
	entry = cp_cache[0][i]

	if not entry[1].__eq__(b'\x01'):
		print('Err: unknown.', file=stderr)
		exit(1)

	return utf8_decode(entry[3])

def icpx_utf8(cf, cp_cache, value):
	if (0x01, value) in cp_cache[1]:
		return cp_cache[1][(0x01, value)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x01', len(value).to_bytes(2), utf8_encode(value)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x01, value)] = i

	return i

def i2cpx_utf8(cf, cp_cache, value): return icpx_utf8(cf, cp_cache, value).to_bytes(2)

def icpx_c(cf, cp_cache, name):
	if (0x07, name) in cp_cache[1]:
		return cp_cache[1][(0x07, name)]

	icp_utf8 = icpx_utf8(cf, cp_cache, name)

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x07', icp_utf8.to_bytes(2)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x07, name)] = i

	return i

def i2cpx_c(cf, cp_cache, name): return icpx_c(cf, cp_cache, name).to_bytes(2)

def icpx_string(cf, cp_cache, value):
	if (0x08, value) in cp_cache[1]:
		return cp_cache[1][(0x08, value)]

	icp_utf8 = icpx_utf8(cf, cp_cache, value)

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x08', icp_utf8.to_bytes(2)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x08, value)] = i

	return i

def i2cpx_string(cf, cp_cache, value): return icpx_string(cf, cp_cache, value).to_bytes(2)

def icpx_int(cf, cp_cache, value):
	if (0x03, value) in cp_cache[0]:
		return cp_cache[0][(0x03, value)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x03', value.to_bytes(4)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x03, value)] = i

	return i

def i2cpx_int(cf, cp_cache, value): return icpx_int(cf, cp_cache, value).to_bytes(2)

def icpx_long(cf, cp_cache, value):
	if (0x05, value) in cp_cache[1]:
		return cp_cache[1][(0x05, value)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x05', value.to_bytes(8)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 2).to_bytes(2)
	cp_cache[1][(0x05, value)] = i

	return i

def i2cpx_long(cf, cp_cache, value): return icpx_long(cf, cp_cache, value).to_bytes(2)

def icpx_name_and_type(cf, cp_cache, name, desc):
	if (0x0c, name, desc) in cp_cache[1]:
		return cp_cache[1][(0x0c, name, desc)]

	icp_name = icpx_utf8(cf, cp_cache, name)
	icp_type = icpx_utf8(cf, cp_cache, desc)

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x0c', icp_name.to_bytes(2), icp_type.to_bytes(2)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x0c, name, desc)] = i

	return i

def i2cpx_name_and_type(cf, cp_cache, name, desc): return icpx_name_and_type(cf, cp_cache, name, desc).to_bytes(2)

def icpx_f(cf, cp_cache, c_name, name, desc):
	if (0x09, c_name, name, desc) in cp_cache[1]:
		return cp_cache[1][(0x09, c_name, name, desc)]

	icp_class = icpx_c(cf, cp_cache, c_name)
	icp_name_and_type = icpx_name_and_type(cf, cp_cache, name, desc)

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x09', icp_class.to_bytes(2), icp_name_and_type.to_bytes(2)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x09, c_name, name, desc)] = i

	return i

def i2cpx_f(cf, cp_cache, c_name, name, desc): return icpx_f(cf, cp_cache, c_name, name, desc).to_bytes(2)

def icpx_m(cf, cp_cache, c_name, name, desc):
	if (0x0a, c_name, name, desc) in cp_cache[1]:
		return cp_cache[1][(0x0a, c_name, name, desc)]

	icp_class = icpx_c(cf, cp_cache, c_name)
	icp_name_and_type = icpx_name_and_type(cf, cp_cache, name, desc)

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x0a', icp_class.to_bytes(2), icp_name_and_type.to_bytes(2)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x0a, c_name, name, desc)] = i

	return i

def i2cpx_m(cf, cp_cache, c_name, name, desc): return icpx_m(cf, cp_cache, c_name, name, desc).to_bytes(2)

def icpx_i(cf, cp_cache, c_name, name, desc):
	if (0x0b, c_name, name, desc) in cp_cache[1]:
		return cp_cache[1][(0x0b, c_name, name, desc)]

	icp_class = icpx_c(cf, cp_cache, c_name)
	icp_name_and_type = icpx_name_and_type(cf, cp_cache, name, desc)

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x0b', icp_class.to_bytes(2), icp_name_and_type.to_bytes(2)])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x0b, c_name, name, desc)] = i

	return i

def i2cpx_i(cf, cp_cache, c_name, name, desc): return icpx_i(cf, cp_cache, c_name, name, desc).to_bytes(2)

def icpx_float(cf, cp_cache, float_bytes):
	if (0x04, float_bytes) in cp_cache[1]:
		return cp_cache[1][(0x04, float_bytes)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x04', float_bytes])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache[1][(0x04, float_bytes)] = i

	return i

def i2cpx_float(cf, cp_cache, float_bytes): return icpx_float(cf, cp_cache, float_bytes).to_bytes(2)

def icpx_double(cf, cp_cache, double_bytes):
	if (0x06, double_bytes) in cp_cache[1]:
		return cp_cache[1][(0x06, double_bytes)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x06', double_bytes])
	cp_cache[0][i] = cp[-1]
	cf[0x03] = (i + 2).to_bytes(2)
	cp_cache[1][(0x06, double_bytes)] = i

	return i

def i2cpx_double(cf, cp_cache, double_bytes): return icpx_double(cf, cp_cache, double_bytes).to_bytes(2)

def get_attribute(attributes, cp_cache, name):
	for a in attributes:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__(name):
			return a

	return None

def a_code_load(a_code_b):
	a_code = [None] * 8

	a_code[0x00] = a_code_b[0:2]
	a_code[0x01] = a_code_b[2:4]

	a_code[0x02] = a_code_b[4:8]
	code_length = int.from_bytes(a_code[0x02])

	a_code[0x03] = a_code_b[8:8 + code_length]
	i = 8 + code_length

	a_code[0x04] = a_code_b[i:i + 2]
	excp_table_len = int.from_bytes(a_code[0x04])
	i += 2

	excp_table = []
	a_code[0x05] = excp_table

	for _ in range(excp_table_len):
		excp_table.append([
			a_code_b[i:i + 2],
			a_code_b[i + 2:i + 4],
			a_code_b[i + 4:i + 6],
			a_code_b[i + 6:i + 8]
		])
		i += 8

	a_code[0x06] = a_code_b[i:i + 2]
	attr_count = int.from_bytes(a_code[0x06])
	i += 2

	attr_list = []
	a_code[0x07] = attr_list

	for _ in range(attr_count):
		attr = [
			a_code_b[i:i + 2],
			a_code_b[i + 2:i + 6],
			None
		]
		length = int.from_bytes(attr[0x01])

		attr[0x02] = a_code_b[i + 6:i + 6 + length]
		i += 6 + length

	return a_code

def a_code_assemble(a_code):
	return b''.join([
		a_code[0x00], a_code[0x01],
		a_code[0x02], a_code[0x03],
		a_code[0x04],
		*[b''.join(entry) for entry in a_code[0x05]],
		a_code[0x06],
		*[b''.join(a) for a in a_code[0x07]]
	])


# multianewarray, jsr, jsr_w, ret, invokedynamic, invokeinterface, monitorenter,
# monitorexit, wide, tableswitch, lookupswitch, iinc
_info_table = [
	['nop', 0x00],
	['aconst_null', 0x01],
	['iconst_m1', 0x02],
	['iconst_0', 0x03],
	['iconst_1', 0x04],
	['iconst_2', 0x05],
	['iconst_3', 0x06],
	['iconst_4', 0x07],
	['iconst_5', 0x08],
	['lconst_0', 0x09],
	['lconst_1', 0x0a],
	['fconst_0', 0x0b],
	['fconst_1', 0x0c],
	['fconst_2', 0x0d],
	['dconst_0', 0x0e],
	['dconst_1', 0x0f],
	['bipush', 0x10, 1],
	['sipush', 0x11, 2],
	['ldc', 0x12, 1],
	['ldc_w', 0x13, 2],
	['ldc2_w', 0x14, 2],
	['iload', 0x15, 1],
	['lload', 0x16, 1],
	['fload', 0x17, 1],
	['dload', 0x18, 1],
	['aload', 0x19, 1],
	['iload_0', 0x1a],
	['iload_1', 0x1b],
	['iload_2', 0x1c],
	['iload_3', 0x1d],
	['lload_0', 0x1e],
	['lload_1', 0x1f],
	['lload_2', 0x20],
	['lload_3', 0x21],
	['fload_0', 0x22],
	['fload_1', 0x23],
	['fload_2', 0x24],
	['fload_3', 0x25],
	['dload_0', 0x26],
	['dload_1', 0x27],
	['dload_2', 0x28],
	['dload_3', 0x29],
	['aload_0', 0x2a],
	['aload_1', 0x2b],
	['aload_2', 0x2c],
	['aload_3', 0x2d],
	['iaload', 0x2e],
	['laload', 0x2f],
	['faload', 0x30],
	['daload', 0x31],
	['aaload', 0x32],
	['baload', 0x33],
	['caload', 0x34],
	['saload', 0x35],
	['istore', 0x36, 1],
	['lstore', 0x37, 1],
	['fstore', 0x38, 1],
	['dstore', 0x39, 1],
	['astore', 0x3a, 1],
	['istore_0', 0x3b],
	['istore_1', 0x3c],
	['istore_2', 0x3d],
	['istore_3', 0x3e],
	['lstore_0', 0x3f],
	['lstore_1', 0x40],
	['lstore_2', 0x41],
	['lstore_3', 0x42],
	['fstore_0', 0x43],
	['fstore_1', 0x44],
	['fstore_2', 0x45],
	['fstore_3', 0x46],
	['dstore_0', 0x47],
	['dstore_1', 0x48],
	['dstore_2', 0x49],
	['dstore_3', 0x4a],
	['astore_0', 0x4b],
	['astore_1', 0x4c],
	['astore_2', 0x4d],
	['astore_3', 0x4e],
	['iastore', 0x4f],
	['lastore', 0x50],
	['fastore', 0x51],
	['dastore', 0x52],
	['aastore', 0x53],
	['bastore', 0x54],
	['castore', 0x55],
	['sastore', 0x56],
	['pop', 0x57],
	['pop2', 0x58],
	['dup', 0x59],
	['dup_x1', 0x5a],
	['dup_x2', 0x5b],
	['dup2', 0x5c],
	['dup2_x1', 0x5d],
	['dup2_x2', 0x5e],
	['swap', 0x5f],
	['iadd', 0x60],
	['ladd', 0x61],
	['fadd', 0x62],
	['dadd', 0x63],
	['isub', 0x64],
	['lsub', 0x65],
	['fsub', 0x66],
	['dsub', 0x67],
	['imul', 0x68],
	['lmul', 0x69],
	['fmul', 0x6a],
	['dmul', 0x6b],
	['idiv', 0x6c],
	['ldiv', 0x6d],
	['fdiv', 0x6e],
	['ddiv', 0x6f],
	['irem', 0x70],
	['lrem', 0x71],
	['frem', 0x72],
	['drem', 0x73],
	['ineg', 0x74],
	['lneg', 0x75],
	['fneg', 0x76],
	['dneg', 0x77],
	['ishl', 0x78],
	['lshl', 0x79],
	['ishr', 0x7a],
	['lshr', 0x7b],
	['iushr', 0x7c],
	['lushr', 0x7d],
	['iand', 0x7e],
	['land', 0x7f],
	['ior', 0x80],
	['lor', 0x81],
	['ixor', 0x82],
	['lxor', 0x83],
	['i2l', 0x85],
	['i2f', 0x86],
	['i2d', 0x87],
	['l2i', 0x88],
	['l2f', 0x89],
	['l2d', 0x8a],
	['f2i', 0x8b],
	['f2l', 0x8c],
	['f2d', 0x8d],
	['d2i', 0x8e],
	['d2l', 0x8f],
	['d2f', 0x90],
	['i2b', 0x91],
	['i2c', 0x92],
	['i2s', 0x93],
	['lcmp', 0x94],
	['fcmpl', 0x95],
	['fcmpg', 0x96],
	['dcmpl', 0x97],
	['dcmpg', 0x98],
	['ifeq', 0x99, 2],
	['ifne', 0x9a, 2],
	['iflt', 0x9b, 2],
	['ifge', 0x9c, 2],
	['ifgt', 0x9d, 2],
	['ifle', 0x9e, 2],
	['if_icmpeq', 0x9f, 2],
	['if_icmpne', 0xa0, 2],
	['if_icmplt', 0xa1, 2],
	['if_icmpge', 0xa2, 2],
	['if_icmpgt', 0xa3, 2],
	['if_icmple', 0xa4, 2],
	['if_acmpeq', 0xa5, 2],
	['if_acmpne', 0xa6, 2],
	['goto', 0xa7, 2],
	['ireturn', 0xac],
	['lreturn', 0xad],
	['freturn', 0xae],
	['dreturn', 0xaf],
	['areturn', 0xb0],
	['return', 0xb1],
	['getstatic', 0xb2, 2],
	['putstatic', 0xb3, 2],
	['getfield', 0xb4, 2],
	['putfield', 0xb5, 2],
	['invokevirtual', 0xb6, 2],
	['invokespecial', 0xb7, 2],
	['invokestatic', 0xb8, 2],
	['new', 0xbb, 2],
	['newarray', 0xbc, 1],
	['anewarray', 0xbd, 2],
	['arraylength', 0xbe],
	['athrow', 0xbf],
	['checkcast', 0xc0, 2],
	['instanceof', 0xc1, 2],
	['ifnull', 0xc6, 2],
	['ifnonnull', 0xc7, 2],
	['goto_w', 0xc8, 4],
	['breakpoint', 0xca],
]

def _gen_ins_info_table(entries):
	table = {}

	for info in entries:
		if len(info).__eq__(3):
			name, opcode, sz_operand = info
			table[name] = (bytes([opcode]), 1 + sz_operand, sz_operand)
		else:
			name, opcode = info
			table[name] = (bytes([opcode]), 1)

	return table

_ins_info_table = _gen_ins_info_table(_info_table)

def _gen_ins_info_table_2(entries):
	table = {}

	for info in entries:
		if len(info).__eq__(3):
			name, opcode, sz_operand = info
			table[opcode] = (name, 1 + sz_operand, sz_operand)
		else:
			name, opcode = info
			table[opcode] = (name, 1)

	return table

_ins_info_table_2 = _gen_ins_info_table_2(_info_table)

def is_opcode_only(opcode_name):
	return not (_ins_info_table.get(opcode_name)[1] != 1)

def is_opcode_only_2(opcode):
	return _ins_info_table_2.get(opcode)[1].__eq__(1)

def get_opcode_name_2(opcode):
	return _ins_info_table_2.get(opcode)[0]

def is_jump(opcode_name):
	return opcode_name[0:2].__eq__('if') or opcode_name.__eq__('goto') or opcode_name.__eq__('goto_w')

def is_opcode_accept_field_reference(opcode_name):
	return opcode_name in ['getstatic', 'putstatic', 'getfield', 'putfield']

def _get_opcode_and_size(opcode_name): return _ins_info_table[opcode_name][0:2]

def load_code(cp_cache, code_bytes):
	i = 0
	code = []

	while i < len(code_bytes):
		opcode = code_bytes[i]
		if not opcode in _ins_info_table_2:
			print('Err: unknown instruction.', file=stderr)
			exit(1)

		if is_opcode_only_2(opcode):
			opcode_name, *_ = _ins_info_table_2.get(opcode)
			code.append(opcode_name)
			i += 1
		else:
			opcode_name, sz, sz_operand = _ins_info_table_2.get(opcode)

			if opcode_name.__eq__('ldc'):
				icp = int.from_bytes(code_bytes[i + 1:i + 2])
				ecp_type = get_ecp_type_at(cp_cache, icp)

				if ecp_type.__eq__(b'\x03'):
					pass

				if ecp_type.__eq__(b'\x04'):
					code.append(['ldc_w.f32', get_float_at(cp_cache, icp)])

				if ecp_type.__eq__(b'\x08'):
					pass

				if ecp_type.__eq__(b'\x07'):
					pass

				if ecp_type.__eq__(b'\x0f'):
					pass

				if ecp_type.__eq__(b'\x10'):
					pass

				i += 2
				continue

			if opcode_name.__eq__('ldc2_w'):
				icp = int.from_bytes(code_bytes[i + 1:i + 3])
				ecp_type = get_ecp_type_at(cp_cache, icp)

				if ecp_type.__eq__(b'\x05'):
					pass

				if ecp_type.__eq__(b'\x06'):
					code.append(['ldc2_w.f64', get_double_at(cp_cache, icp)])

				i += 3
				continue

			if opcode_name in ['getfield', 'putfield', 'getstatic', 'putstatic']:
				icp = int.from_bytes(code_bytes[i + 1:i + 3])
				ecp_type = get_ecp_type_at(cp_cache, icp)
				code.append([opcode_name, *get_field_reference_at(cp_cache, icp)])
				i += 3
				continue

			if opcode_name in ['invokevirtual', 'invokespecial', 'invokestatic']:
				icp = int.from_bytes(code_bytes[i + 1:i + 3])
				ecp_type = get_ecp_type_at(cp_cache, icp)
				code.append([opcode_name, *get_method_reference_at(cp_cache, icp)])
				i += 3
				continue

			if opcode_name in ['checkcast', 'instanceof', 'anewarray', 'new']:
				pass

			code.append([opcode_name, int.from_bytes(code_bytes[i + 1:i + 1 + sz_operand])])
			i += sz

	return code

def assemble_code(cf, cp_cache, select, pc_begin, code):
	temp = []
	target_table = {}
	i = pc_begin

	for ins in code:
		if type(ins) is str:
			if not is_opcode_only(ins):
				print(f'Err: invalid opcode `{ins}`', file=stderr)
				exit(1)
			temp.append(_ins_info_table[ins][0])
			i += 1
		else:
			opcode_name, *args = ins

			if opcode_name.__eq__('iinc'):
				temp.append(b'\x84' + args[0].to_bytes(1) + args[1].to_bytes(1))
				i += 3
				continue

			if opcode_name in ('new', 'anewarray', 'checkcast'):
				opcode, sz = _get_opcode_and_size(opcode_name)
				(name,) = args
				temp.append(opcode + i2cpx_c(cf, cp_cache, name[select] if isinstance(name, tuple) else name))
				i += sz
				continue

			if opcode_name.__eq__('ldc2_w.i64') and isinstance(args[0], int):
				opcode, sz, _ = _ins_info_table['ldc2_w']
				temp.append(opcode + i2cpx_long(cf, cp_cache, args[0]))
				i += sz
				continue

			if opcode_name.__eq__('ldc2_w.f64') and isinstance(args[0], int):
				opcode, sz, _ = _ins_info_table['ldc2_w']
				temp.append(opcode + i2cpx_double(cf, cp_cache, struct.pack('>d', float(args[0]))))
				i += sz
				continue

			if opcode_name.__eq__('ldc2_w.f64') and isinstance(args[0], float):
				opcode, sz, _ = _ins_info_table['ldc2_w']
				temp.append(opcode + i2cpx_double(cf, cp_cache, struct.pack('>d', args[0])))
				i += sz
				continue

			if opcode_name.__eq__('ldc2_w.f64'):
				opcode, sz, _ = _ins_info_table['ldc2_w']
				temp.append(opcode + i2cpx_double(cf, cp_cache, args[0]))
				i += sz
				continue

			if opcode_name.__eq__('ldc_w.f32') and isinstance(args[0], float):
				opcode, sz, _ = _ins_info_table['ldc_w']
				temp.append(opcode + i2cpx_float(cf, cp_cache, struct.pack('>f', float(args[0]))))
				i += sz
				continue

			if opcode_name.__eq__('ldc_w.f32'):
				opcode, sz, _ = _ins_info_table['ldc_w']
				temp.append(opcode + i2cpx_float(cf, cp_cache, args[0]))
				i += sz
				continue

			if opcode_name.__eq__('ldc_w.string'):
				opcode, sz, _ = _ins_info_table['ldc_w']
				temp.append(opcode + i2cpx_string(cf, cp_cache, args[0]))
				i += sz
				continue

			if opcode_name.__eq__('ldc_w.i32') and isinstance(args[0], int):
				opcode, sz, _ = _ins_info_table['ldc_w']
				temp.append(opcode + icpx_int(cf, cp_cache, args[0]).to_bytes(2))
				i += sz
				continue

			if opcode_name.__eq__('ldc.f32') and isinstance(args[0], int):
				opcode, sz, _ = _ins_info_table['ldc']
				temp.append(opcode + icpx_float(cf, cp_cache, struct.pack('>f', float(args[0]))).to_bytes(1))
				i += sz
				continue

			if opcode_name.__eq__('ldc.f32') and isinstance(args[0], float):
				opcode, sz, _ = _ins_info_table['ldc']
				temp.append(opcode + icpx_float(cf, cp_cache, struct.pack('>f', args[0])).to_bytes(1))
				i += sz
				continue

			if opcode_name.__eq__('ldc.f32'):
				opcode, sz, _ = _ins_info_table['ldc']
				temp.append(opcode + icpx_float(cf, cp_cache, args[0]).to_bytes(1))
				i += sz
				continue

			if opcode_name.__eq__('ldc.string'):
				opcode, sz, _ = _ins_info_table['ldc']
				temp.append(opcode + icpx_string(cf, cp_cache, args[0]).to_bytes(1))
				i += sz
				continue

			if opcode_name.__eq__('ldc.class'):
				opcode, sz, _ = _ins_info_table['ldc']
				temp.append(opcode + icpx_c(cf, cp_cache, args[0]).to_bytes(1))
				i += sz
				continue

			if opcode_name.__eq__('ldc_w.class'):
				opcode, sz, _ = _ins_info_table['ldc_w']
				temp.append(opcode + icpx_c(cf, cp_cache, args[0]).to_bytes(2))
				i += sz
				continue

			if opcode_name.__eq__('invokeinterface'):
				r_args = []

				for arg in args[0:-1]:
					if type(arg) is tuple:
						r_args.append(arg[select])
					else:
						r_args.append(arg)

				temp.append(b'\xb9' + i2cpx_i(cf, cp_cache, *r_args) + args[3].to_bytes(1) + b'\x00')
				i += 5
				continue

			if is_jump(opcode_name):
				opcode, sz, sz_operand = _ins_info_table[opcode_name]
				if type(args[0]) is str:
					temp.append(ins)
				else:
					temp.append(opcode + args[0].to_bytes(sz_operand))
				i += sz
				continue

			if is_opcode_accept_field_reference(opcode_name):
				opcode, sz, sz_operand = _ins_info_table[opcode_name]
				if type(args[0]) is str or type(args[0]) is tuple:
					r_args = []

					for arg in args:
						if type(arg) is tuple:
							r_args.append(arg[select])
						else:
							r_args.append(arg)

					temp.append(opcode + i2cpx_f(cf, cp_cache, *r_args))
				else:
					temp.append(opcode + args[0].to_bytes(sz_operand))
				i += sz
				continue

			if opcode_name in ['invokevirtual', 'invokespecial', 'invokestatic']:
				opcode, sz, sz_operand = _ins_info_table[opcode_name]
				if type(args[0]) is str or type(args[0]) is tuple:
					r_args = []

					for arg in args:
						if type(arg) is tuple:
							r_args.append(arg[select])
						else:
							r_args.append(arg)

					temp.append(opcode + i2cpx_m(cf, cp_cache, *r_args))
				else:
					temp.append(opcode + args[0].to_bytes(sz_operand))
				i += sz
				continue

			if opcode_name.__eq__('label'):
				target_table[args[0]] = i
				continue

			opcode, sz, sz_operand = _ins_info_table[opcode_name]
			temp.append(opcode + args[0].to_bytes(sz_operand))
			i += sz

	i = pc_begin

	for j, ins in enumerate(temp):
		if type(ins) is bytes:
			i += len(ins)
		else:
			opcode_name, *args = ins
			opcode, sz, sz_operand = _ins_info_table[opcode_name]

			target_pc = target_table[args[0]]
			offset_pc = target_pc - i

			temp[j] = opcode + offset_pc.to_bytes(2, signed=True)
			i += sz

	return b''.join(temp)

field_access_flags = {
	'public': 0x0001,
	'private': 0x0002,
	'protected': 0x0004,
	'static': 0x0008,
	'final': 0x0010,
	'volatile': 0x0040,
	'transient': 0x0080,
	'synthetic': 0x1000,
	'enum': 0x4000,
}

def create_field(cf, cp_cache, acc_flags, name, desc):
	acc = 0x0000

	for flag in acc_flags:
		acc = acc.__or__(field_access_flags[flag])

	f = [None] * 5

	f[0x00] = acc.to_bytes(2)
	f[0x01] = i2cpx_utf8(cf, cp_cache, name)
	f[0x02] = i2cpx_utf8(cf, cp_cache, desc)

	f[0x03] = bytes(2)
	f[0x04] = []

	return f

method_access_flags = {
	'public': 0x0001,
	'private': 0x0002,
	'protected': 0x0004,
	'static': 0x0008,
	'final': 0x0010,
	'synchronized': 0x0020,
	'bridge': 0x0040,
	'varargs': 0x0080,
	'native': 0x0100,
	'abstract': 0x0400,
	'strict': 0x0800,
	'synthetic': 0x1000,
}

def create_method(cf, cp_cache, acc_flags, name, desc):
	acc = 0x0000

	for flag in acc_flags:
			acc = acc.__or__(method_access_flags[flag])

	m = [None] * 5

	m[0x00] = acc.to_bytes(2)
	m[0x01] = i2cpx_utf8(cf, cp_cache, name)
	m[0x02] = i2cpx_utf8(cf, cp_cache, desc)

	m[0x03] = bytes(2)
	m[0x04] = []

	return m

def get_method(cf, cp_cache, name, desc):
	for m in cf[0x0d]:
		if not get_utf8_at(cp_cache, int.from_bytes(m[0x01])).__eq__(name) or not get_utf8_at(cp_cache, int.from_bytes(m[0x02])).__eq__(desc):
			continue

		return m

	print('Err: unknown.', file=stderr)
	exit(1)
