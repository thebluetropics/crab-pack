from sys import (exit, stderr)
from . import utf8

def use_helper(cf):
	cp = { 'cf': cf, 'idx_cache': dict(), 'cache': dict() }

	for entry in cf[0x04]:
		cp['idx_cache'][entry[0]] = entry

	for entry in cf[0x04]:
		if entry[1].__eq__(b'\x01'):
			cp['cache'][(0x01, utf8.decode(entry[3]))] = entry[0]

		if entry[1].__eq__(b'\x03'):
			cp['cache'][(0x03, int.from_bytes(entry[2]))] = entry[0]

		if entry[1].__eq__(b'\x05'):
			cp['cache'][(0x05, int.from_bytes(entry[2]))] = entry[0]

	for entry in cf[0x04]:
		if entry[1].__eq__(b'\x07'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp['idx_cache'][int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8.decode(ecp_utf8[3])
			cp['cache'][(0x07, vcp_utf8)] = i
			continue

		if entry[1].__eq__(b'\x08'):
			i, _, i2cp_to_utf8 = entry
			ecp_utf8 = cp['idx_cache'][int.from_bytes(i2cp_to_utf8)]
			vcp_utf8 = utf8.decode(ecp_utf8[3])
			cp['cache'][(0x08, vcp_utf8)] = i
			continue

		if entry[1].__eq__(b'\x0c'):
			i = entry[0]
			ecp_name = cp['idx_cache'][int.from_bytes(entry[2])]
			ecp_type = cp['idx_cache'][int.from_bytes(entry[3])]
			name_string = utf8.decode(ecp_name[3])
			type_string = utf8.decode(ecp_type[3])
			cp['cache'][(0x0c, name_string, type_string)] = i
			continue

	for entry in cf[0x04]:
		if entry[1].__eq__(b'\x09'):
			i = entry[0]
			ecp_class = cp['idx_cache'][int.from_bytes(entry[2])]
			ecp_name_and_type = cp['idx_cache'][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp['idx_cache'][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp['idx_cache'][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp['idx_cache'][int.from_bytes(ecp_name_and_type[3])]

			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp['cache'][(0x09, class_string, name_string, type_string)] = i
			continue

		if entry[1].__eq__(b'\x0a'):
			i = entry[0]
			ecp_class = cp['idx_cache'][int.from_bytes(entry[2])]
			ecp_name_and_type = cp['idx_cache'][int.from_bytes(entry[3])]
			ecp_class_utf8 = cp['idx_cache'][int.from_bytes(ecp_class[2])]
			ecp_name_utf8 = cp['idx_cache'][int.from_bytes(ecp_name_and_type[2])]
			ecp_type_utf8 = cp['idx_cache'][int.from_bytes(ecp_name_and_type[3])]

			class_string = utf8.decode(ecp_class_utf8[3])
			name_string = utf8.decode(ecp_name_utf8[3])
			type_string = utf8.decode(ecp_type_utf8[3])
			cp['cache'][(0x0a, class_string, name_string, type_string)] = i
			continue

	return cp

def get_utf8_at(xcp, i):
	entry = xcp['idx_cache'][i]

	if not entry[1].__eq__(b'\x01'):
		print('Err: unknown.', file=stderr)
		exit(1)

	return utf8.decode(entry[3])

def icpx_utf8(xcp, value):
	if (0x01, value) in xcp['cache']:
		return xcp['cache'][(0x01, value)]

	rcp = xcp['cf'][0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x01', len(value).to_bytes(2), utf8.encode(value)])
	xcp['idx_cache'][i] = rcp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x01, value)] = i

	return i

def i2cpx_utf8(xcp, value): return icpx_utf8(xcp, value).to_bytes(2)

def icpx_c(xcp, name):
	if (0x07, name) in xcp['cache']:
		return xcp['cache'][(0x07, name)]

	icp_utf8 = icpx_utf8(xcp, name)

	rcp = xcp['cf'][0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x07', icp_utf8.to_bytes(2)])
	xcp['idx_cache'][i] = rcp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x07, name)] = i

	return i

def i2cpx_c(xcp, name): return icpx_c(xcp, name).to_bytes(2)

def icpx_string(xcp, value):
	if (0x08, value) in xcp['cache']:
		return xcp['cache'][(0x08, value)]

	icp_utf8 = icpx_utf8(xcp, value)

	rcp = xcp['cf'][0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x08', icp_utf8.to_bytes(2)])
	xcp['idx_cache'][i] = rcp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x08, value)] = i

	return i

def i2cpx_string(xcp, value): return icpx_string(xcp, value).to_bytes(2)

def icpx_int(xcp, value):
	if (0x03, value) in xcp['cache']:
		return xcp['cache'][(0x03, value)]

	cp = xcp['cf'][0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x03', value.to_bytes(4)])
	xcp['idx_cache'][i] = cp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x03, value)] = i

	return i

def i2cpx_int(xcp, value): return icpx_int(xcp, value).to_bytes(2)

def icpx_long(xcp, value):
	if (0x05, value) in xcp['cache']:
		return xcp['cache'][(0x05, value)]

	cp = xcp['cf'][0x04]
	i = 1

	if cp:
		i = cp[-1][0]

		if cp[-1][1].__eq__(b'\x05') or cp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	cp.append([i, b'\x05', value.to_bytes(8)])
	xcp['idx_cache'][i] = cp[-1]
	xcp['cf'][0x03] = (i + 2).to_bytes(2)
	xcp['cache'][(0x05, value)] = i

	return i

def i2cpx_long(xcp, value): return icpx_long(xcp, value).to_bytes(2)

def icpx_name_and_type(xcp, name, desc):
	if (0x0c, name, desc) in xcp['cache']:
		return xcp['cache'][(0x0c, name, desc)]

	icp_name = icpx_utf8(xcp, name)
	icp_type = icpx_utf8(xcp, desc)

	rcp = xcp['cf'][0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x0c', icp_name.to_bytes(2), icp_type.to_bytes(2)])
	xcp['idx_cache'][i] = rcp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x0c, name, desc)] = i

	return i

def i2cpx_name_and_type(xcp, name, desc): return icpx_name_and_type(xcp, name, desc).to_bytes(2)

def icpx_f(xcp, c_name, name, desc):
	if (0x09, c_name, name, desc) in xcp['cache']:
		return xcp['cache'][(0x09, c_name, name, desc)]

	icp_class = icpx_c(xcp, c_name)
	icp_name_and_type = icpx_name_and_type(xcp, name, desc)

	rcp = xcp['cf'][0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x09', icp_class.to_bytes(2), icp_name_and_type.to_bytes(2)])
	xcp['idx_cache'][i] = rcp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x09, c_name, name, desc)] = i

	return i

def i2cpx_f(xcp, c_name, name, desc): return icpx_f(xcp, c_name, name, desc).to_bytes(2)

def icpx_m(xcp, c_name, name, desc):
	if (0x0a, c_name, name, desc) in xcp['cache']:
		return xcp['cache'][(0x0a, c_name, name, desc)]

	icp_class = icpx_c(xcp, c_name)
	icp_name_and_type = icpx_name_and_type(xcp, name, desc)

	rcp = xcp['cf'][0x04]
	i = 1

	if rcp:
		i = rcp[-1][0]

		if rcp[-1][1].__eq__(b'\x05') or rcp[-1][1].__eq__(b'\x06'):
			i = i + 2
		else:
			i = i + 1

	rcp.append([i, b'\x0a', icp_class.to_bytes(2), icp_name_and_type.to_bytes(2)])
	xcp['idx_cache'][i] = rcp[-1]
	xcp['cf'][0x03] = (i + 1).to_bytes(2)
	xcp['cache'][(0x0a, c_name, name, desc)] = i

	return i

def i2cpx_m(xcp, c_name, name, desc): return icpx_m(xcp, c_name, name, desc).to_bytes(2)
