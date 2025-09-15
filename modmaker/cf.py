from sys import exit, stderr

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
