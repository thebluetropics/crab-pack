import os, mod

from mod.method import create_method, get_method
from mod.attribute import get_attribute
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	i2cpx_c,
	icpx_double,
	icpx_float,
	get_float_at,
	get_double_at,
	get_field_reference_at,
	get_method_reference_at
)

def apply(side_name):
	if not mod.config.is_feature_enabled('experimental.hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/BottleItem'

	cf = class_file.create_new()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['gm', 'ej'][side])

	methods = [
		_create_constructor(cf, cp_cache, side, c_name),
		_create_use_method(cf, cp_cache, side_name, side)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = instructions.assemble(0, [
		'aload_0',
		'iload_1',
		['invokespecial', icpx_m(cf, cp_cache, ['gm', 'ej'][side], '<init>', '(I)V')],

		'aload_0',
		'iconst_1',
		['putfield', icpx_f(cf, cp_cache, c_name, 'bg', 'I')],

		'return'
	])
	a_code = attribute.code.assemble([
		(2).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _get_instructions_for_use_method(cf, cp_cache, side_name, side):
	c_name_1 = ['bc', 'al'][side]
	cf_1 = class_file.load(mod.config.path(f'stage/{side_name}/{c_name_1}.class'))
	cp_cache_1 = constant_pool.init_constant_pool_cache(cf_1[0x04])

	m = get_method(cf_1, cp_cache_1, 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])
	a = get_attribute(m[0x04], cp_cache_1, 'Code')

	a_code = attribute.code.load(a[0x02])
	code = instructions.load_instructions(a_code[0x03][0:243])
	included_code = []

	for istr in code:
		opcode = istr if type(istr) is str else istr[0]

		if opcode.__eq__('ldc'):
			etcp = constant_pool.get_etcp_at(cp_cache_1, istr[1])

			if etcp.__eq__(b'\x04'):
				included_code.append(['ldc', icpx_float(cf, cp_cache, get_float_at(cp_cache_1, istr[1]))])

			continue

		if opcode in (
			'ldc_w', 'ldc2_w',
			'getstatic', 'putstatic',
			'getfield', 'putfield',
			'invokevirtual', 'invokespecial', 'invokestatic',
			'checkcast', 'instanceof',
			'anewarray', 'new',
		):
			etcp = constant_pool.get_etcp_at(cp_cache_1, istr[1])

			if etcp.__eq__(b'\x09'):
				included_code.append([opcode, icpx_f(cf, cp_cache, *get_field_reference_at(cp_cache_1, istr[1]))])

			if etcp.__eq__(b'\x0a'):
				included_code.append([opcode, icpx_m(cf, cp_cache, *get_method_reference_at(cp_cache_1, istr[1]))])

			if etcp.__eq__(b'\x06'):
				included_code.append([opcode, icpx_double(cf, cp_cache, get_double_at(cp_cache_1, istr[1]))])

			continue

		included_code.append(istr)

	final_code = instructions.assemble(0, included_code)

	return final_code[0:226] + instructions.assemble(226, ['iconst_1']) + final_code[238:243]

def _create_use_method(cf, cp_cache, side_name, side):
	included_instructions = _get_instructions_for_use_method(cf, cp_cache, side_name, side)
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])

	code = included_instructions + instructions.assemble(len(included_instructions), [
		['aload', 24],
		['ifnull*', 'do_not_refill'],

		['aload', 24],
		['getfield', icpx_f(cf, cp_cache, ['vf', 'nh'][side], 'a', ['Ljg;', 'Lgd;'][side])],
		['getstatic', icpx_f(cf, cp_cache, ['jg', 'gd'][side], 'a', ['Ljg;', 'Lgd;'][side])],
		['if_acmpne*', 'do_not_refill'],

		['aload', 2],
		['aload', 24],
		['getfield', icpx_f(cf, cp_cache, ['vf', 'nh'][side], 'b', 'I')],
		['aload', 24],
		['getfield', icpx_f(cf, cp_cache, ['vf', 'nh'][side], 'c', 'I')],
		['aload', 24],
		['getfield', icpx_f(cf, cp_cache, ['vf', 'nh'][side], 'd', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, ['fd', 'dj'][side], ['f', 'd'][side], ['(III)Lln;', '(III)Lhj;'][side])],
		['getstatic', icpx_f(cf, cp_cache, ['ln', 'hj'][side], 'g', ['Lln;', 'Lhj;'][side])],
		['if_acmpne*', 'do_not_refill'],

		['aload', 1],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], ['i', 'h'][side], '()I')],
		['bipush', 100],
		['if_icmpge*', 'skip_inc'],

		['aload', 1],
		['aload', 1],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], ['i', 'h'][side], '()I')],
		['bipush', 25],
		['iadd'],
		['bipush', 100],
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Math', 'min', '(II)I')],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], 'b', '(I)V')],

		['jump_target*', 'skip_inc'],
		['aload', 1],
		['areturn'],

		['jump_target*', 'do_not_refill'],

		['aload_1'],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], ['i', 'h'][side], '()I')],
		['ifle*', 'end'],

		['aload_1'],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], ['i', 'h'][side], '()I')],
		['iconst_5'],
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Math', 'min', '(II)I')],
		['istore', 25],

		['aload_1'],
		['aload_1'],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], ['i', 'h'][side], '()I')],
		['iload', 25],
		'isub',
		'iconst_0',
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Math', 'max', '(II)I')],
		['invokevirtual', icpx_m(cf, cp_cache, ['iz', 'fy'][side], 'b', '(I)V')],

		['aload_3'],
		['iload', 25],
		['invokevirtual', icpx_m(cf, cp_cache, ['gs', 'em'][side], 'restoreThirst', '(I)V')],

		['aload_1'],
		'areturn',

		['jump_target*', 'end'],

		'aload_1',
		'areturn'
	])
	a_code = attribute.code.assemble([
		(14).to_bytes(2),
		(26).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
