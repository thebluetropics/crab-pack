from . import utf8
from sys import exit, stderr

def init_constant_pool_cache(cp):
	cp_cache = {
		'index': {},
		'lookup': {}
	}

	for entry in cp:
		cp_cache['index'][entry[0]] = entry

	for entry in cp:
		if entry[1].__eq__(b'\x01'):
			cp_cache['lookup'][(0x01, utf8.decode(entry[3]))] = entry[0]

		if entry[1].__eq__(b'\x03'):
			cp_cache['lookup'][(0x03, int.from_bytes(entry[2]))] = entry[0]

		if entry[1].__eq__(b'\x04'):
			cp_cache['lookup'][(0x04, entry[2])] = entry[0]

		if entry[1].__eq__(b'\x05'):
			cp_cache['lookup'][(0x05, int.from_bytes(entry[2]))] = entry[0]

		if entry[1].__eq__(b'\x06'):
			cp_cache['lookup'][(0x06, entry[2])] = entry[0]

	for entry in cp:
		if entry[1].__eq__(b'\x07'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp_cache['index'][int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8.decode(ecp_utf8[3])
			cp_cache['lookup'][(0x07, vcp_utf8)] = i

			continue

		if entry[1].__eq__(b'\x08'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp_cache['index'][int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8.decode(ecp_utf8[3])
			cp_cache['lookup'][(0x08, vcp_utf8)] = i

			continue

		if entry[1].__eq__(b'\x0c'):
			i = entry[0]
			ecp_name = cp_cache['index'][int.from_bytes(entry[2])]
			ecp_type = cp_cache['index'][int.from_bytes(entry[3])]
			name_string = utf8.decode(ecp_name[3])
			type_string = utf8.decode(ecp_type[3])
			cp_cache['lookup'][(0x0c, name_string, type_string)] = i

			continue

	for entry in cp:
		if entry[1].__eq__(b'\x09'):
			i = entry[0]
			ecp_class = cp_cache['index'][int.from_bytes(entry[2])]
			ecp_name_and_type = cp_cache['index'][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp_cache['index'][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[3])]
			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp_cache['lookup'][(0x09, class_string, name_string, type_string)] = i

			continue

		if entry[1].__eq__(b'\x0a'):
			i = entry[0]
			ecp_class = cp_cache['index'][int.from_bytes(entry[2])]
			ecp_name_and_type = cp_cache['index'][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp_cache['index'][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[3])]
			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp_cache['lookup'][(0x0a, class_string, name_string, type_string)] = i

			continue

		if entry[1].__eq__(b'\x0b'):
			i = entry[0]
			ecp_class = cp_cache['index'][int.from_bytes(entry[2])]
			ecp_name_and_type = cp_cache['index'][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp_cache['index'][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[3])]
			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp_cache['lookup'][(0x0b, class_string, name_string, type_string)] = i

			continue

	return cp_cache

def get_etcp_at(cp_cache, i):
	entry = cp_cache['index'][i]
	tag = entry[1]

	return tag

def get_float_at(cp_cache, i):
	entry = cp_cache['index'][i]

	if not entry[1].__eq__(b'\x04'):
		print('Err: no float found.', file=stderr)
		exit(1)

	return entry[2]

def get_double_at(cp_cache, i):
	entry = cp_cache['index'][i]

	if not entry[1].__eq__(b'\x06'):
		print('Err: no double found.', file=stderr)
		exit(1)

	return entry[2]

def get_field_reference_at(cp_cache, i):
	entry = cp_cache['index'][i]

	if not entry[1].__eq__(b'\x09'):
		print('Err: no field reference found.', file=stderr)
		exit(1)

	ecp_class = cp_cache['index'][int.from_bytes(entry[2])]
	ecp_name_and_type = cp_cache['index'][int.from_bytes(entry[3])]
	ecp_class_utf8 = cp_cache['index'][int.from_bytes(ecp_class[2])]
	ecp_name_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[2])]
	ecp_type_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[3])]
	class_name = utf8.decode(ecp_class_utf8[3])
	name = utf8.decode(ecp_name_utf8[3])
	desc = utf8.decode(ecp_type_utf8[3])

	return (class_name, name, desc)

def get_method_reference_at(cp_cache, i):
	entry = cp_cache['index'][i]

	if not entry[1].__eq__(b'\x0a'):
		print('Err: no method reference found.', file=stderr)
		exit(1)

	ecp_class = cp_cache['index'][int.from_bytes(entry[2])]
	ecp_name_and_type = cp_cache['index'][int.from_bytes(entry[3])]
	ecp_class_utf8 = cp_cache['index'][int.from_bytes(ecp_class[2])]
	ecp_name_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[2])]
	ecp_type_utf8 = cp_cache['index'][int.from_bytes(ecp_name_and_type[3])]
	class_name = utf8.decode(ecp_class_utf8[3])
	name = utf8.decode(ecp_name_utf8[3])
	desc = utf8.decode(ecp_type_utf8[3])

	return (class_name, name, desc)

def get_utf8_at(cp_cache, i):
	entry = cp_cache['index'][i]

	if not entry[1].__eq__(b'\x01'):
		print('Err: unknown.', file=stderr)
		exit(1)

	return utf8.decode(entry[3])

def icpx_utf8(cf, cp_cache, value):
	if (0x01, value) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x01, value)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x01', len(value).to_bytes(2), utf8.encode(value)])
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x01, value)] = i

	return i

def i2cpx_utf8(cf, cp_cache, value): return icpx_utf8(cf, cp_cache, value).to_bytes(2)

def icpx_c(cf, cp_cache, name):
	if (0x07, name) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x07, name)]

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
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x07, name)] = i

	return i

def i2cpx_c(cf, cp_cache, name): return icpx_c(cf, cp_cache, name).to_bytes(2)

def icpx_string(cf, cp_cache, value):
	if (0x08, value) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x08, value)]

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
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x08, value)] = i

	return i

def i2cpx_string(cf, cp_cache, value): return icpx_string(cf, cp_cache, value).to_bytes(2)

def icpx_int(cf, cp_cache, value):
	if (0x03, value) in cp_cache['index']:
		return cp_cache['index'][(0x03, value)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x03', value.to_bytes(4)])
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x03, value)] = i

	return i

def i2cpx_int(cf, cp_cache, value): return icpx_int(cf, cp_cache, value).to_bytes(2)

def icpx_long(cf, cp_cache, value):
	if (0x05, value) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x05, value)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x05', value.to_bytes(8)])
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 2).to_bytes(2)
	cp_cache['lookup'][(0x05, value)] = i

	return i

def i2cpx_long(cf, cp_cache, value): return icpx_long(cf, cp_cache, value).to_bytes(2)

def icpx_name_and_type(cf, cp_cache, name, desc):
	if (0x0c, name, desc) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x0c, name, desc)]

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
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x0c, name, desc)] = i

	return i

def i2cpx_name_and_type(cf, cp_cache, name, desc): return icpx_name_and_type(cf, cp_cache, name, desc).to_bytes(2)

def icpx_f(cf, cp_cache, c_name, name, desc):
	if (0x09, c_name, name, desc) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x09, c_name, name, desc)]

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
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x09, c_name, name, desc)] = i

	return i

def i2cpx_f(cf, cp_cache, c_name, name, desc): return icpx_f(cf, cp_cache, c_name, name, desc).to_bytes(2)

def icpx_m(cf, cp_cache, c_name, name, desc):
	if (0x0a, c_name, name, desc) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x0a, c_name, name, desc)]

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
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x0a, c_name, name, desc)] = i

	return i

def i2cpx_m(cf, cp_cache, c_name, name, desc): return icpx_m(cf, cp_cache, c_name, name, desc).to_bytes(2)

def icpx_i(cf, cp_cache, c_name, name, desc):
	if (0x0b, c_name, name, desc) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x0b, c_name, name, desc)]

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
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x0b, c_name, name, desc)] = i

	return i

def i2cpx_i(cf, cp_cache, c_name, name, desc): return icpx_i(cf, cp_cache, c_name, name, desc).to_bytes(2)

def icpx_float(cf, cp_cache, float_bytes):
	if (0x04, float_bytes) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x04, float_bytes)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x04', float_bytes])
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 1).to_bytes(2)
	cp_cache['lookup'][(0x04, float_bytes)] = i

	return i

def i2cpx_float(cf, cp_cache, float_bytes): return icpx_float(cf, cp_cache, float_bytes).to_bytes(2)

def icpx_double(cf, cp_cache, double_bytes):
	if (0x06, double_bytes) in cp_cache['lookup']:
		return cp_cache['lookup'][(0x06, double_bytes)]

	cp = cf[0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x06', double_bytes])
	cp_cache['index'][i] = cp[-1]
	cf[0x03] = (i + 2).to_bytes(2)
	cp_cache['lookup'][(0x06, double_bytes)] = i

	return i

def i2cpx_double(cf, cp_cache, double_bytes): return icpx_double(cf, cp_cache, double_bytes).to_bytes(2)
