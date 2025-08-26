# Destructure code attribute bytes
def load(b):
	a_code = [None] * 8

	a_code[0x00] = b[0:2] # max stack
	a_code[0x01] = b[2:4] # max locals

	# code length
	a_code[0x02] = b[4:8]
	code_length = int.from_bytes(a_code[0x02])

	# code
	a_code[0x03] = b[8:8 + code_length]
	i = 8 + code_length

	# exception table length
	a_code[0x04] = b[i:i + 2]
	excp_table_len = int.from_bytes(a_code[0x04])
	i += 2

	# exception table
	excp_table = []

	for _ in range(excp_table_len):
		excp_table.append([
			b[i:i + 2],
			b[i + 2:i + 4],
			b[i + 4:i + 6],
			b[i + 6:i + 8]
		])
		i += 8

	a_code[0x05] = excp_table

	# attribute count
	a_code[0x06] = b[i:i + 2]
	attr_count = int.from_bytes(a_code[0x06])
	i += 2

	# attributes
	attr_list = []

	for _ in range(attr_count):
		attr = [
			b[i:i + 2], # → name index
			b[i + 2:i + 6], # → length
			None
		]
		length = int.from_bytes(attr[0x01])

		attr[0x02] = b[i + 6:i + 6 + length]
		i += 6 + length

	a_code[0x07] = attr_list

	return a_code

def assemble(a_code):
	o = bytearray()

	for x in [
		*[a_code[i] for i in range(0x00, 0x05)],
		*[bytes().join(entry) for entry in a_code[0x05]],
		a_code[0x06],
		*[bytes().join(a) for a in a_code[0x07]]
	]:
		o.extend(x)

	return memoryview(o).tobytes()
