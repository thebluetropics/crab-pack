import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
)
from modmaker.m import(
	get_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	get_utf8_at
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = ['vl', 'no'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('etc.no_crop_trampling'):
		_modify_on_stepped_on_method(cf, cp_cache, side)

	if mod.config.is_feature_enabled('etc.extended_farmland_water_source'):
		_modify_is_water_nearby_method(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.FarmlandBlock')

def _modify_on_stepped_on_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, 'b', ['(Lfd;IIILsn;)V', '(Ldj;IIILlq;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_is_water_nearby_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, ['i', 'h'][side], ['(Lfd;III)Z', '(Ldj;III)Z'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		['aload', 1],
		['iload', 2], ['iload', 3], 'iconst_1', 'isub', ['iload', 4],
		['invokevirtual', ('fd', 'dj'), ('f', 'd'), ('(III)Lln;', '(III)Lhj;')],
		['getstatic', ('ln', 'hj'), 'g', ('Lln;', 'Lhj;')],
		['if_acmpne', 'end'],

		'iconst_1',
		'ireturn',

		['label', 'end']
	]) + a_code[0x03][0:77]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
