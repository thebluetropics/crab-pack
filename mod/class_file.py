# Load `.class` file into memory
def load(path):
	file = open(path, 'rb')

	cf = [None] * 16

	cf[0x00] = file.read(4)
	cf[0x01] = file.read(2)
	cf[0x02] = file.read(2)

	cf[0x03] = file.read(2)
	cp_count = int.from_bytes(cf[0x03])

	cp = []
	cf[0x04] = cp

	i = 1

	while i < cp_count:
		tag = file.read(1)

		if tag.__eq__(b'\x07'):
			cp.append([i, tag, file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x09'):
			cp.append([i, tag, file.read(2), file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x0a'):
			cp.append([i, tag, file.read(2), file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x0b'):
			cp.append([i, tag, file.read(2), file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x08'):
			cp.append([i, tag, file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x03'):
			cp.append([i, tag, file.read(4)])
			i += 1
			continue

		if tag.__eq__(b'\x04'):
			cp.append([i, tag, file.read(4)])
			i += 1
			continue

		if tag.__eq__(b'\x05'):
			cp.append([i, tag, file.read(8)])
			i += 2
			continue

		if tag.__eq__(b'\x06'):
			cp.append([i, tag, file.read(8)])
			i += 2
			continue

		if tag.__eq__(b'\x0c'):
			cp.append([i, tag, file.read(2), file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x01'):
			utf8_text_length_bytes = file.read(2)
			utf8_text_length = int.from_bytes(utf8_text_length_bytes, 'big')

			cp.append(
				[i, b'\x01', utf8_text_length_bytes, file.read(utf8_text_length)]
			)

			i += 1
			continue

		if tag.__eq__(b'\x0f'):
			cp.append([i, tag, file.read(1), file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x10'):
			cp.append([i, tag, file.read(2)])
			i += 1
			continue

		if tag.__eq__(b'\x12'):
			cp.append([i, tag, file.read(2), file.read(2)])
			i += 1
			continue

	cf[0x05] = file.read(2)
	cf[0x06] = file.read(2)
	cf[0x07] = file.read(2)

	cf[0x08] = file.read(2)
	interface_count = int.from_bytes(cf[0x08])

	interfaces = []
	cf[0x09] = interfaces

	for _ in range(interface_count):
		interfaces.append(file.read(2))

	cf[0x0a] = file.read(2)
	field_count = int.from_bytes(cf[0x0a])

	fields = []
	cf[0x0b] = fields

	for _ in range(field_count):
		field = [
			file.read(2),
			file.read(2),
			file.read(2)
		]

		attr_count_bytes = file.read(2)
		attr_count = int.from_bytes(attr_count_bytes)
		field.append(attr_count_bytes)

		attrs = []

		for _ in range(attr_count):
			attr = [
				file.read(2),
				file.read(4),
				None
			]
			length = int.from_bytes(attr[0x01])
			attr[0x02] = file.read(length)
			attrs.append(attr)

		field.append(attrs)
		fields.append(field)

	cf[0x0c] = file.read(2)
	method_count = int.from_bytes(cf[0x0c])

	methods = []
	cf[0x0d] = methods

	for _ in range(method_count):
		method = [
			file.read(2),
			file.read(2),
			file.read(2)
		]

		attr_count_bytes = file.read(2)
		attr_count = int.from_bytes(attr_count_bytes)
		method.append(attr_count_bytes)

		attrs = []

		for _ in range(attr_count):
			attr = [
				file.read(2),
				file.read(4),
				None
			]
			length = int.from_bytes(attr[0x01])
			attr[0x02] = file.read(length)

			attrs.append(attr)

		method.append(attrs)

		methods.append(method)

	cf[0x0e] = file.read(2)
	a_count = int.from_bytes(cf[0x0e])

	attrs = []
	cf[0x0f] = attrs

	for _ in range(a_count):
		attr = [
			file.read(2),
			file.read(4),
			None
		]
		length = int.from_bytes(attr[0x01])
		attr[0x02] = file.read(length)

		attrs.append(attr)

	file.close()
	return cf

# Assemble `.class` file back into byte array
def assemble(cf):
	out = bytearray()

	out.extend(cf[0x00])
	out.extend(cf[0x01])
	out.extend(cf[0x02])
	out.extend(cf[0x03])

	for entry in cf[0x04]:
		out.extend(b''.join(entry[1:]))

	out.extend(cf[0x05])
	out.extend(cf[0x06])
	out.extend(cf[0x07])
	out.extend(cf[0x08])

	for inf in cf[0x09]:
		out.extend(inf)

	out.extend(cf[0x0a])

	for f in cf[0x0b]:
		out.extend(b''.join(f[0x00:0x04]))

		for a in f[0x04]:
			out.extend(b''.join(a))

	out.extend(cf[0x0c])

	for m in cf[0x0d]:
		out.extend(b''.join(m[0x00:0x04]))

		for a in m[0x04]:
			out.extend(b''.join(a))

	out.extend(cf[0x0e])

	for a in cf[0xf]:
		out.extend(b''.join(a))

	return bytes(out)

# Construct a new empty in-memory `.class` file
def create_new():
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
