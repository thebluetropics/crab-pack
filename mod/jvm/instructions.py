from .istr_info import istr_info

def assemble(pc_begin, code):
	out = []
	target_table = {}

	i = pc_begin

	for istr in code:
		if type(istr) is str:
			opcode_byte, *_ = istr_info.get(istr)
			out.append(opcode_byte)

			i = i + 1
			continue

		if type(istr) is list and not istr[0][-1].__eq__('*'):
			opcode, *operands = istr
			opcode_byte, operands_info, sz = istr_info[opcode]

			out.append(opcode_byte + bytes().join(
				v.to_bytes(operands_info[j]) for j, v in enumerate(operands)
			))

			i = i + sz
			continue

		if type(istr) is list and istr[0][-1].__eq__('*'):
			opcode, *operands = istr

			if opcode[0:-1] in istr_info:
				*_, sz = istr_info[opcode[0:-1]]
				out.append(istr)
				i = i + sz
			else:
				if opcode[0:-1].__eq__('jump_target'):
					target_table[operands[0]] = i

			continue

	i = pc_begin

	for j, istr in enumerate(out):
		if type(istr) is bytes:
			i = i + len(istr)
			continue

		if type(istr) is list and istr[0][-1].__eq__('*'):
			opcode, *operands = istr
			opcode_byte, _, sz = istr_info[opcode[0:-1]]

			target_pc = target_table[operands[0]]
			offset_pc = target_pc - i

			out[j] = opcode_byte + offset_pc.to_bytes(2)
			i = i + sz

			continue

	return bytes().join(out)
