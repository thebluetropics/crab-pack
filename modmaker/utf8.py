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
