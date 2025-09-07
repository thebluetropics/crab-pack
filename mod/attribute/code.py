def load(a_code_bytes):
	a_code = [None] * 8

	a_code[0x00] = a_code_bytes[0:2]
	a_code[0x01] = a_code_bytes[2:4]

	a_code[0x02] = a_code_bytes[4:8]
	code_length = int.from_bytes(a_code[0x02])

	a_code[0x03] = a_code_bytes[8:8 + code_length]
	i = 8 + code_length

	a_code[0x04] = a_code_bytes[i:i + 2]
	excp_table_len = int.from_bytes(a_code[0x04])
	i += 2

	excp_table = []
	a_code[0x05] = excp_table

	for _ in range(excp_table_len):
		excp_table.append([
			a_code_bytes[i:i + 2],
			a_code_bytes[i + 2:i + 4],
			a_code_bytes[i + 4:i + 6],
			a_code_bytes[i + 6:i + 8]
		])
		i += 8

	a_code[0x06] = a_code_bytes[i:i + 2]
	attr_count = int.from_bytes(a_code[0x06])
	i += 2

	attr_list = []
	a_code[0x07] = attr_list

	for _ in range(attr_count):
		attr = [
			a_code_bytes[i:i + 2],
			a_code_bytes[i + 2:i + 6],
			None
		]
		length = int.from_bytes(attr[0x01])

		attr[0x02] = a_code_bytes[i + 6:i + 6 + length]
		i += 6 + length

	return a_code

def assemble(a_code):
	return b''.join([
		a_code[0x00], a_code[0x01],
		a_code[0x02], a_code[0x03],
		a_code[0x04],
		*[b''.join(entry) for entry in a_code[0x05]],
		a_code[0x06],
		*[b''.join(a) for a in a_code[0x07]]
	])
