# Load a `.class` file into memory
def load(path):
	f = open(path, "rb")

	cf = [None] * 16

	cf[0x00] = f.read(4) # → magic
	cf[0x01] = f.read(2) # → minor ver.
	cf[0x02] = f.read(2) # → major ver.

	cf[0x03] = f.read(2)
	cp_count = int.from_bytes(cf[0x03])

	cp = []

	i = 1

	while i < cp_count:
		tag = f.read(1)

		if tag.__eq__(b"\x07"):
			cp.append([i, tag, f.read(2)])
			i += 1
			continue

		if tag.__eq__(b"\x09"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

		if tag.__eq__(b"\x0a"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

		if tag.__eq__(b"\x0b"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

		if tag.__eq__(b"\x08"):
			cp.append([i, tag, f.read(2)])
			i += 1
			continue

		if tag.__eq__(b"\x03"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

		if tag.__eq__(b"\x04"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

		if tag.__eq__(b"\x05"):
			cp.append([i, tag, f.read(8)])
			i += 2
			continue

		if tag.__eq__(b"\x06"):
			cp.append([i, tag, f.read(8)])
			i += 2
			continue

		if tag.__eq__(b"\x0c"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

		if tag.__eq__(b"\x01"):
			utf8_text_length_bytes = f.read(2)
			utf8_text_length = int.from_bytes(utf8_text_length_bytes, "big")

			cp.append(
				[i, b"\x01", utf8_text_length_bytes, f.read(utf8_text_length)]
			)

			i += 1
			continue

		if tag.__eq__(b"\x0f"):
			cp.append([i, tag, f.read(3)])
			i += 1
			continue

		if tag.__eq__(b"\x10"):
			cp.append([i, tag, f.read(2)])
			i += 1
			continue

		if tag.__eq__(b"\x12"):
			cp.append([i, tag, f.read(4)])
			i += 1
			continue

	cf[0x04] = cp

	cf[0x05] = f.read(2) # → access flags
	cf[0x06] = f.read(2) # → this class
	cf[0x07] = f.read(2) # → super class

	cf[0x08] = f.read(2)
	interface_count = int.from_bytes(cf[0x08])

	interfaces = []

	for _ in range(interface_count):
		interfaces.append(f.read(2))

	cf[0x09] = interfaces

	cf[0x0a] = f.read(2)
	field_count = int.from_bytes(cf[0x0a])

	fields = []

	for _ in range(field_count):
		field = [
			f.read(2), # → access flags
			f.read(2), # → name index
			f.read(2) # → descriptor index
		]

		# attribute count
		attr_count_bytes = f.read(2)
		attr_count = int.from_bytes(attr_count_bytes)
		field.append(attr_count_bytes)

		# attributes
		attrs = []

		for _ in range(attr_count):
			attr = [
				f.read(2),
				f.read(4),
				None
			]
			length = int.from_bytes(attr[0x01])
			attr[0x02] = f.read(length)
			attrs.append(attr)

		field.append(attrs)
		fields.append(field)

	cf[0x0b] = fields

	# method count
	cf[0x0c] = f.read(2)
	method_count = int.from_bytes(cf[0x0c])

	# methods
	methods = []

	for _ in range(method_count):
		method = [
			f.read(2), # → access flags
			f.read(2), # → name index
			f.read(2) # → descriptor index
		]

		# attribute count
		attr_count_bytes = f.read(2)
		attr_count = int.from_bytes(attr_count_bytes)
		method.append(attr_count_bytes)

		# attributes
		attrs = []

		for _ in range(attr_count):
			attr = [
				f.read(2), # → name index
				f.read(4), # → length
				None
			]
			length = int.from_bytes(attr[0x01])
			attr[0x02] = f.read(length)

			attrs.append(attr)

		method.append(attrs)

		methods.append(method)

	cf[0x0d] = methods

	# attribute count
	cf[0x0e] = f.read(2)
	attr_count = int.from_bytes(cf[0x0e])

	# attributes
	attrs = []

	for _ in range(attr_count):
		attr = [
			f.read(2), # → name index
			f.read(4), # → length
			None
		]
		length = int.from_bytes(attr[0x01])
		attr[0x02] = f.read(length)

		attrs.append(attr)

	cf[0x0f] = attrs

	f.close()

	return cf

def make(cf):
	b = bytearray()

	b.extend(cf[0x00]) # → magic
	b.extend(cf[0x01]) # → minor ver.
	b.extend(cf[0x02]) # → major ver.

	# constant pool count
	b.extend(cf[0x03])

	# constant pool
	for entry in cf[0x04]:
		if entry[1].__eq__(b"\x01"):
			b.extend(entry[1])
			b.extend(entry[2])
			b.extend(entry[3])
		else:
			b.extend(entry[1])
			b.extend(entry[2])

	b.extend(cf[0x05]) # → access flags
	b.extend(cf[0x06]) # → this class
	b.extend(cf[0x07]) # → super class

	# interface count
	b.extend(cf[0x08])

	# interfaces
	for interface in cf[0x09]:
		b.extend(interface)

	# field count
	b.extend(cf[0x0a])

	# fields
	for field in cf[0x0b]:
		b.extend(field[0x00])
		b.extend(field[0x01])
		b.extend(field[0x02])
		b.extend(field[0x03])

		for attr in field[0x04]:
			b.extend(attr[0x00])
			b.extend(attr[0x01])
			b.extend(attr[0x02])

	# method count
	b.extend(cf[0x0c])

	# methods
	for method in cf[0x0d]:
		b.extend(method[0x00])
		b.extend(method[0x01])
		b.extend(method[0x02])
		b.extend(method[0x03])

		for attr in method[0x04]:
			b.extend(attr[0x00])
			b.extend(attr[0x01])
			b.extend(attr[0x02])

	# attribute count
	b.extend(cf[0x0e])

	# attributes
	for attr in cf[0x0f]:
		b.extend(attr[0x00])
		b.extend(attr[0x01])
		b.extend(attr[0x02])

	return bytes(b)

def create_template():
	cf = [None] * 16

	cf[0x00] = b"\xca\xfe\xba\xbe"
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
