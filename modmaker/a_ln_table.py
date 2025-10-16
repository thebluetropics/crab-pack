def a_ln_table_load(buf):
	table = (
		buf[0:2],
		[]
	)
	length = int.from_bytes(table[0x00])
	i = 2

	for _ in range(length):
		table[0x01].append((buf[i:i + 2], buf[i + 2:i + 4]))
		i = i + 4

	return table

def a_ln_table_make(table):
	buf = [table[0x00]]

	for entry in table[0x01]:
		buf.append(entry[0x00] + entry[0x01])

	return b''.join(buf)
