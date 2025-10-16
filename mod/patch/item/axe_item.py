from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_feature_enabled('fix.block_break_times_fix'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['ta', 'ly'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_static_initializer(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.AxeItem')

def _modify_static_initializer(cf, cp_cache, side):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	count = 5
	ext_code = [
		'dup',
		['bipush', 4],
		['getstatic', ('uu', 'na'), 'az', ('Luu;', 'Lna;')],
		'aastore'
	]

	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		['sipush', count]
	]) + a_code[0x03][1:28] + assemble_code(cf, cp_cache, side, 28, ext_code) + a_code[0x03][28:32]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
