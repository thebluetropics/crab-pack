import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod.constant_pool import get_utf8_at
from mod import (
	class_file,
	attribute,
	constant_pool,
	instructions
)
from mod.constant_pool import (
	icpx_f
)

def apply(side_name):
	if not mod.config.is_feature_enabled('fix.block_break_times_fix'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['au', 'ah'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	_modify_static_initializer(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.PickaxeItem')

def _modify_static_initializer(cf, cp_cache, side):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	count = 18
	ext_code = [
		'dup',
		['bipush', 17],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'aC', ['Luu;', 'Lna;'][side])],
		'aastore'
	]

	a_code[0x03] = instructions.assemble(0, [
		['sipush', count]
	]) + a_code[0x03][2:118] + instructions.assemble(121, ext_code) + a_code[0x03][118:122]
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
