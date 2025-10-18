import struct

from sys import exit, stderr
from operator import eq
from .cp import *

def a_code_load(buf):
	a_code = [None] * 8

	a_code[0x00] = buf[0:2]
	a_code[0x01] = buf[2:4]

	a_code[0x02] = buf[4:8]
	code_length = int.from_bytes(a_code[0x02])

	a_code[0x03] = buf[8:8 + code_length]
	i = 8 + code_length

	a_code[0x04] = buf[i:i + 2]
	exception_table_length = int.from_bytes(a_code[0x04])
	i = i + 2

	a_code[0x05] = []
	exception_table = a_code[0x05]

	for _ in range(exception_table_length):
		exception_table.append([
			buf[i:i + 2],
			buf[i + 2:i + 4],
			buf[i + 4:i + 6],
			buf[i + 6:i + 8]
		])
		i = i + 8

	a_code[0x06] = buf[i:i + 2]
	a_count = int.from_bytes(a_code[0x06])
	i = i + 2

	a_code[0x07] = []
	attributes = a_code[0x07]

	for _ in range(a_count):
		a = [
			buf[i:i + 2],
			buf[i + 2:i + 6],
			None
		]
		sz = int.from_bytes(a[0x01])
		a[0x02] = buf[i + 6:i + 6 + sz]
		attributes.append(a)
		i = i + 6 + sz

	return a_code

def a_code_assemble(a_code):
	return b''.join([
		a_code[0x00], a_code[0x01],
		a_code[0x02], a_code[0x03],
		a_code[0x04],
		*[b''.join(entry) for entry in a_code[0x05]],
		a_code[0x06],
		*[b''.join(a) for a in a_code[0x07]]
	])

_opcode_only_instructions_map = {
	'nop': b'\x00',
	'aconst_null': b'\x01',
	'iconst_m1': b'\x02',
	'iconst_0': b'\x03',
	'iconst_1': b'\x04',
	'iconst_2': b'\x05',
	'iconst_3': b'\x06',
	'iconst_4': b'\x07',
	'iconst_5': b'\x08',
	'lconst_0': b'\x09',
	'lconst_1': b'\x0a',
	'fconst_0': b'\x0b',
	'fconst_1': b'\x0c',
	'fconst_2': b'\x0d',
	'dconst_0': b'\x0e',
	'dconst_1': b'\x0f',
	'iload_0': b'\x1a',
	'iload_1': b'\x1b',
	'iload_2': b'\x1c',
	'iload_3': b'\x1d',
	'lload_0': b'\x1e',
	'lload_1': b'\x1f',
	'lload_2': b'\x20',
	'lload_3': b'\x21',
	'fload_0': b'\x22',
	'fload_1': b'\x23',
	'fload_2': b'\x24',
	'fload_3': b'\x25',
	'dload_0': b'\x26',
	'dload_1': b'\x27',
	'dload_2': b'\x28',
	'dload_3': b'\x29',
	'aload_0': b'\x2a',
	'aload_1': b'\x2b',
	'aload_2': b'\x2c',
	'aload_3': b'\x2d',
	'iaload': b'\x2e',
	'laload': b'\x2f',
	'faload': b'\x30',
	'daload': b'\x31',
	'aaload': b'\x32',
	'baload': b'\x33',
	'caload': b'\x34',
	'saload': b'\x35',
	'istore_0': b'\x3b',
	'istore_1': b'\x3c',
	'istore_2': b'\x3d',
	'istore_3': b'\x3e',
	'lstore_0': b'\x3f',
	'lstore_1': b'\x40',
	'lstore_2': b'\x41',
	'lstore_3': b'\x42',
	'fstore_0': b'\x43',
	'fstore_1': b'\x44',
	'fstore_2': b'\x45',
	'fstore_3': b'\x46',
	'dstore_0': b'\x47',
	'dstore_1': b'\x48',
	'dstore_2': b'\x49',
	'dstore_3': b'\x4a',
	'astore_0': b'\x4b',
	'astore_1': b'\x4c',
	'astore_2': b'\x4d',
	'astore_3': b'\x4e',
	'iastore': b'\x4f',
	'lastore': b'\x50',
	'fastore': b'\x51',
	'dastore': b'\x52',
	'aastore': b'\x53',
	'bastore': b'\x54',
	'castore': b'\x55',
	'sastore': b'\x56',
	'pop': b'\x57',
	'pop2': b'\x58',
	'dup': b'\x59',
	'dup_x1': b'\x5a',
	'dup_x2': b'\x5b',
	'dup2': b'\x5c',
	'dup2_x1': b'\x5d',
	'dup2_x2': b'\x5e',
	'swap': b'\x5f',
	'iadd': b'\x60',
	'ladd': b'\x61',
	'fadd': b'\x62',
	'dadd': b'\x63',
	'isub': b'\x64',
	'lsub': b'\x65',
	'fsub': b'\x66',
	'dsub': b'\x67',
	'imul': b'\x68',
	'lmul': b'\x69',
	'fmul': b'\x6a',
	'dmul': b'\x6b',
	'idiv': b'\x6c',
	'ldiv': b'\x6d',
	'fdiv': b'\x6e',
	'ddiv': b'\x6f',
	'irem': b'\x70',
	'lrem': b'\x71',
	'frem': b'\x72',
	'drem': b'\x73',
	'ineg': b'\x74',
	'lneg': b'\x75',
	'fneg': b'\x76',
	'dneg': b'\x77',
	'ishl': b'\x78',
	'lshl': b'\x79',
	'ishr': b'\x7a',
	'lshr': b'\x7b',
	'iushr': b'\x7c',
	'lushr': b'\x7d',
	'iand': b'\x7e',
	'land': b'\x7f',
	'ior': b'\x80',
	'lor': b'\x81',
	'ixor': b'\x82',
	'lxor': b'\x83',
	'i2l': b'\x85',
	'i2f': b'\x86',
	'i2d': b'\x87',
	'l2i': b'\x88',
	'l2f': b'\x89',
	'l2d': b'\x8a',
	'f2i': b'\x8b',
	'f2l': b'\x8c',
	'f2d': b'\x8d',
	'd2i': b'\x8e',
	'd2l': b'\x8f',
	'd2f': b'\x90',
	'i2b': b'\x91',
	'i2c': b'\x92',
	'i2s': b'\x93',
	'lcmp': b'\x94',
	'fcmpl': b'\x95',
	'fcmpg': b'\x96',
	'dcmpl': b'\x97',
	'dcmpg': b'\x98',
	'ireturn': b'\xac',
	'lreturn': b'\xad',
	'freturn': b'\xae',
	'dreturn': b'\xaf',
	'areturn': b'\xb0',
	'return': b'\xb1',
	'arraylength': b'\xbe',
	'athrow': b'\xbf',
	'monitorenter': b'\xc2',
	'monitorexit': b'\xc3'
}
_opcode_only_instructions_reverse_map = {
	v: k for k, v in _opcode_only_instructions_map.items()
}

_load_store_instructions_map = {
	'iload': b'\x15',
	'lload': b'\x16',
	'fload': b'\x17',
	'dload': b'\x18',
	'aload': b'\x19',
	'istore': b'\x36',
	'lstore': b'\x37',
	'fstore': b'\x38',
	'dstore': b'\x39',
	'astore': b'\x3a',
}
_load_store_instructions_reverse_map = {
	v: k for k, v in _load_store_instructions_map.items()
}

_jump_instructions_map = {
	'ifeq': b'\x99',
	'ifne': b'\x9a',
	'iflt': b'\x9b',
	'ifge': b'\x9c',
	'ifgt': b'\x9d',
	'ifle': b'\x9e',
	'if_icmpeq': b'\x9f',
	'if_icmpne': b'\xa0',
	'if_icmplt': b'\xa1',
	'if_icmpge': b'\xa2',
	'if_icmpgt': b'\xa3',
	'if_icmple': b'\xa4',
	'if_acmpeq': b'\xa5',
	'if_acmpne': b'\xa6',
	'goto': b'\xa7',
	'ifnull': b'\xc6',
	'ifnonnull': b'\xc7',
	'jsr': b'\xa8'
}
_jump_instructions_reverse_map = {
	v: k for k, v in _jump_instructions_map.items()
}

_wide_jump_instructions_map = {
	'goto_w': b'\xc8',
	'jsr_w': b'\xc9'
}
_wide_jump_instructions_reverse_map = {
	v: k for k, v in _wide_jump_instructions_map.items()
}

_field_referencing_instructions_map = {
	'getstatic': b'\xb2',
	'putstatic': b'\xb3',
	'getfield': b'\xb4',
	'putfield': b'\xb5',
}
_field_referencing_instructions_reverse_map = {
	v: k for k, v in _field_referencing_instructions_map.items()
}

_method_referencing_instructions_map = {
	'invokevirtual': b'\xb6',
	'invokespecial': b'\xb7',
	'invokestatic': b'\xb8',
}
_method_referencing_instructions_reverse_map = {
	v: k for k, v in _method_referencing_instructions_map.items()
}

_class_referencing_instructions_map = {
	'new': b'\xbb',
	'anewarray': b'\xbd',
	'checkcast': b'\xc0',
	'instanceof': b'\xc1'
}
_class_referencing_instructions_reverse_map = {
	v: k for k, v in _class_referencing_instructions_map.items()
}

def load_code(cp_cache, buf):
	code = []
	i = 0

	while i < len(buf):
		opcode = buf[i].to_bytes(1)

		if opcode in _opcode_only_instructions_reverse_map:
			code.append(_opcode_only_instructions_reverse_map.get(opcode))
			i = i + 1
			continue

		if opcode in _load_store_instructions_reverse_map:
			code.append([_load_store_instructions_reverse_map.get(opcode), int.from_bytes(buf[i + 1:i + 2], signed=False)])
			i = i + 2
			continue

		if opcode.__eq__(b'\x10'):
			code.append(['bipush', int.from_bytes(buf[i + 1:i + 2], byteorder='big', signed=True)])
			i = i + 2
			continue

		if opcode.__eq__(b'\x11'):
			code.append(['sipush', int.from_bytes(buf[i + 1:i + 3], byteorder='big', signed=True)])
			i = i + 3
			continue

		if opcode.__eq__(b'\xa9'):
			code.append(['ret', int.from_bytes(buf[i + 1:i + 2], byteorder='big', signed=False)])
			i = i + 2
			continue

		if opcode.__eq__(b'\x12'):
			j = int.from_bytes(buf[i + 1:i + 2], byteorder='big', signed=False)
			entry = cp_get_entry(cp_cache, j)

			if entry[1].__eq__(b'\x08'):
				code.append(['ldc.string', cp_get_string(cp_cache, j)])

			if entry[1].__eq__(b'\x07'):
				code.append(['ldc.class', cp_get_class(cp_cache, j)])

			if entry[1].__eq__(b'\x03'):
				code.append(['ldc.i32', cp_get_i32(cp_cache, j)])

			if entry[1].__eq__(b'\x04'):
				code.append(['ldc.f32', cp_get_f32(cp_cache, j)])

			if entry[1].__eq__(b'\x0f'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if entry[1].__eq__(b'\x10'):
				print('Err: unknown.', file=stderr)
				exit(1)

			i = i + 2
			continue

		if opcode.__eq__(b'\x13'):
			j = int.from_bytes(buf[i + 1:i + 3], byteorder='big', signed=False)
			entry = cp_get_entry(cp_cache, j)

			if entry[1].__eq__(b'\x08'):
				code.append(['ldc_w.string', cp_get_string(cp_cache, j)])

			if entry[1].__eq__(b'\x07'):
				code.append(['ldc_w.class', cp_get_class(cp_cache, j)])

			if entry[1].__eq__(b'\x03'):
				code.append(['ldc_w.i32', cp_get_i32(cp_cache, j)])

			if entry[1].__eq__(b'\x04'):
				code.append(['ldc_w.f32', cp_get_f32(cp_cache, j)])

			if entry[1].__eq__(b'\x0f'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if entry[1].__eq__(b'\x10'):
				print('Err: unknown.', file=stderr)
				exit(1)

			i = i + 3
			continue

		if opcode.__eq__(b'\x14'):
			j = int.from_bytes(buf[i + 1:i + 3], byteorder='big', signed=False)
			entry = cp_get_entry(cp_cache, j)

			if entry[1].__eq__(b'\x05'):
				code.append(['ldc2_w.i64', cp_get_i64(cp_cache, j)])

			if entry[1].__eq__(b'\x06'):
				code.append(['ldc2_w.f64', cp_get_f64(cp_cache, j)])

			i = i + 3
			continue

		if opcode.__eq__(b'\x84'):
			code.append(['iinc', int.from_bytes(buf[i + 1:i + 2], signed=False), int.from_bytes(buf[i + 2:i + 3], signed=True)])
			i = i + 3
			continue

		if opcode.__eq__(b'\xbc'):
			code.append(['newarray', int.from_bytes(buf[i + 1:i + 2], signed=False)])
			i = i + 2
			continue

		if opcode in _class_referencing_instructions_reverse_map:
			code.append([_class_referencing_instructions_reverse_map.get(opcode), cp_get_class(cp_cache, int.from_bytes(buf[i + 1:i + 3], signed=False))])
			i = i + 3
			continue

		if opcode in _field_referencing_instructions_reverse_map:
			code.append([_field_referencing_instructions_reverse_map.get(opcode), *cp_get_field_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3], signed=False))])
			i = i + 3
			continue

		if opcode in _method_referencing_instructions_reverse_map:
			code.append([_method_referencing_instructions_reverse_map.get(opcode), *cp_get_method_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3], signed=False))])
			i = i + 3
			continue

		if opcode in _jump_instructions_reverse_map:
			code.append([_jump_instructions_reverse_map.get(opcode), int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if opcode in _wide_jump_instructions_map:
			code.append([_wide_jump_instructions_map.get(opcode), int.from_bytes(buf[i + 1:i + 5], signed=True)])
			i = i + 5
			continue

		if opcode.__eq__(b'\xb9'):
			code.append(['invokeinterface', *cp_get_interface_method_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3], signed=True)), int.from_bytes(buf[i + 3:i + 4], signed=False)])
			i = i + 5
			continue

		print('Err: can\'t handle instruction', opcode.hex())
		exit(1)

	return code

def assemble_code(cf, cp_cache, side, pc_begin, code):
	stage = []
	target_table = {}
	i = pc_begin

	for ins in code:
		if type(ins) is str:
			if not ins in _opcode_only_instructions_map:
				print(f'Err: can\'t find opcode-only instruction {ins}', file=stderr)
				exit(1)

			stage.append(_opcode_only_instructions_map.get(ins))
			i = i + 1
		else:
			if ins[0] in _load_store_instructions_map:
				stage.append(_load_store_instructions_map.get(ins[0]) + ins[1].to_bytes(1))
				i = i + 2
				continue

			if ins[0].__eq__('bipush'):
				stage.append(b'\x10' + ins[1].to_bytes(1, signed=True))
				i = i + 2
				continue

			if ins[0].__eq__('sipush'):
				stage.append(b'\x11' + ins[1].to_bytes(2, signed=True))
				i = i + 3
				continue

			if ins[0].__eq__('ret'):
				stage.append(b'\xa9' + ins[1].to_bytes(1))
				i = i + 2
				continue

			if ins[0].__eq__('ldc.string'):
				stage.append(b'\x12' + icpx_string(cf, cp_cache, ins[1]).to_bytes(1))
				i = i + 2
				continue

			if ins[0].__eq__('ldc.class'):
				stage.append(b'\x12' + icpx_c(cf, cp_cache, ins[1]).to_bytes(1))
				i = i + 2
				continue

			if ins[0].__eq__('ldc.i32'):
				if type(ins[1]) is bytes:
					stage.append(b'\x12' + icpx_int(cf, cp_cache, ins[1]).to_bytes(1))

				if type(ins[1]) is int:
					stage.append(b'\x12' + icpx_int(cf, cp_cache, ins[1].to_bytes(4, signed=True)).to_bytes(1))

				i = i + 2
				continue

			if ins[0].__eq__('ldc.f32'):
				if type(ins[1]) is bytes:
					stage.append(b'\x12' + icpx_float(cf, cp_cache, ins[1]).to_bytes(1))

				if type(ins[1]) is int or type(ins[1]) is float:
					stage.append(b'\x12' + icpx_float(cf, cp_cache, struct.pack('>f', ins[1])).to_bytes(1))

				i = i + 2
				continue

			if ins[0].__eq__('ldc.method_type'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if ins[0].__eq__('ldc.method_handle'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if ins[0].__eq__('ldc_w.string'):
				stage.append(b'\x13' + i2cpx_string(cf, cp_cache, ins[1]))
				i = i + 3
				continue

			if ins[0].__eq__('ldc_w.class'):
				stage.append(b'\x13' + i2cpx_c(cf, cp_cache, ins[1]))
				i = i + 3
				continue

			if ins[0].__eq__('ldc_w.i32'):
				if type(ins[1]) is bytes:
					stage.append(b'\x13' + i2cpx_int(cf, cp_cache, ins[1]))

				if type(ins[1]) is int:
					stage.append(b'\x13' + i2cpx_int(cf, cp_cache, ins[1].to_bytes(4, signed=True)))

				i = i + 3
				continue

			if ins[0].__eq__('ldc_w.f32'):
				if type(ins[1]) is bytes:
					stage.append(b'\x13' + i2cpx_float(cf, cp_cache, ins[1]))

				if type(ins[1]) is int or type(ins[1]) is float:
					stage.append(b'\x13' + i2cpx_float(cf, cp_cache, struct.pack('>f', ins[1])))

				i = i + 3
				continue

			if ins[0].__eq__('ldc_w.method_type'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if ins[0].__eq__('ldc_w.method_handle'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if ins[0].__eq__('ldc2_w.i64'):
				if type(ins[1]) is bytes:
					stage.append(b'\x14' + i2cpx_long(cf, cp_cache, ins[1]))

				if type(ins[1]) is int:
					stage.append(b'\x14' + i2cpx_long(cf, cp_cache, ins[1].to_bytes(8, signed=True)))

				i = i + 3
				continue

			if ins[0].__eq__('ldc2_w.f64'):
				if type(ins[1]) is bytes:
					stage.append(b'\x14' + i2cpx_double(cf, cp_cache, ins[1]))

				if type(ins[1]) is int or type(ins[1]) is float:
					stage.append(b'\x14' + i2cpx_double(cf, cp_cache, struct.pack('>d', ins[1])))

				i = i + 3
				continue

			if ins[0].__eq__('iinc'):
				stage.append(b'\x84' + ins[1].to_bytes(1) + ins[2].to_bytes(1))
				i = i + 3
				continue

			if ins[0].__eq__('newarray'):
				stage.append(b'\xbc' + ins[1].to_bytes(1))
				i = i + 2
				continue

			if ins[0] in _class_referencing_instructions_map:
				stage.append(_class_referencing_instructions_map.get(ins[0]) + i2cpx_c(cf, cp_cache, ins[1][side] if type(ins[1]) is tuple else ins[1]))
				i = i + 3
				continue

			if ins[0] in _field_referencing_instructions_map:
				args = []

				for arg in ins[1:4]:
					args.append(arg[side] if type(arg) is tuple else arg)

				stage.append(_field_referencing_instructions_map.get(ins[0]) + i2cpx_f(cf, cp_cache, *args))
				i = i + 3
				continue

			if ins[0] in _method_referencing_instructions_map:
				args = []

				for arg in ins[1:4]:
					args.append(arg[side] if type(arg) is tuple else arg)

				stage.append(_method_referencing_instructions_map.get(ins[0]) + i2cpx_m(cf, cp_cache, *args))
				i = i + 3
				continue

			if ins[0] in _jump_instructions_map:
				if type(ins[1]) is str:
					stage.append(ins)
				else:
					stage.append(_jump_instructions_map.get(ins[0]) + ins[1].to_bytes(2, signed=True))
				i = i + 3
				continue

			if ins[0] in _wide_jump_instructions_map:
				if type(ins[1]) is str:
					stage.append(ins)
				else:
					stage.append(_wide_jump_instructions_map.get(ins[0]) + ins[1].to_bytes(4, signed=True))
				i = i + 5
				continue

			if ins[0].__eq__('invokeinterface'):
				args = []

				for arg in ins[1:4]:
					args.append(arg[side] if type(arg) is tuple else arg)

				stage.append(b'\xb9' + i2cpx_i(cf, cp_cache, *args) + ins[4].to_bytes(1) + b'\x00')
				i = i + 5
				continue

			if ins[0].__eq__('label'):
				target_table[ins[1]] = i
				continue

			if ins[0] in ('invokedynamic', 'multianewarray', 'wide', 'tableswitch', 'lookupswitch'):
				print('Err: unimplemented.', file=stderr)
				exit(1)

			print('Err: can\'t handle instruction', ins)
			exit(1)

	i = pc_begin

	for j, ins in enumerate(stage):
		if isinstance(ins, bytes):
			i = i + len(ins)
		else:
			target_pc = target_table[ins[1]]
			offset_pc = target_pc - i

			if ins[0] in _jump_instructions_map:
				stage[j] = _jump_instructions_map[ins[0]] + offset_pc.to_bytes(2, signed=True)
				i = i + 3
			else:
				stage[j] = _wide_jump_instructions_map[ins[0]] + offset_pc.to_bytes(4, signed=True)
				i = i + 5

	return b''.join(stage)
