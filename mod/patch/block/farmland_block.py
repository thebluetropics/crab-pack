import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod import (
	attribute,
	instructions,
	constant_pool
)
from mod.class_file import (
	load_class_file,
	assemble_class_file
)
from mod.constant_pool import (
	get_utf8_at,
	icpx_m,
	icpx_f
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = ['vl', 'no'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	if mod.config.is_feature_enabled('etc.no_crop_trampling'):
		_modify_on_stepped_on_method(cf, cp_cache, side)

	if mod.config.is_feature_enabled('etc.extended_farmland_water_source'):
		_modify_is_water_nearby_method(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(assemble_class_file(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.FarmlandBlock')

def _modify_on_stepped_on_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, 'b', ['(Lfd;IIILsn;)V', '(Ldj;IIILlq;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = instructions.assemble(0, [
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
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_is_water_nearby_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, ['i', 'h'][side], ['(Lfd;III)Z', '(Ldj;III)Z'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = instructions.assemble(0, [
		['aload', 1],
		['iload', 2],
		['iload', 3],
		'iconst_1',
		'isub',
		['iload', 4],
		['invokevirtual', icpx_m(cf, cp_cache, ['fd', 'dj'][side], ['f', 'd'][side], ['(III)Lln;', '(III)Lhj;'][side])],
		['getstatic', icpx_f(cf, cp_cache, ['ln', 'hj'][side], 'g', ['Lln;', 'Lhj;'][side])],
		['if_acmpne*', 'end'],

		'iconst_1',
		'ireturn',

		['jump_target*', 'end']
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
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
