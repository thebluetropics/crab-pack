from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_feature_enabled('food.raw_squid_and_calamari'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['ey', 'de'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, '<init>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:219] + assemble_code(cf, cp_cache, side, 219, [
		'aload_0',
		['getstatic', ('gm', 'ej'), 'raw_squid', ('Lgm;', 'Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],
		['new', ('iz', 'fy')],
		'dup',
		['getstatic', ('gm', 'ej'), 'calamari', ('Lgm;', 'Lej;')],
		'iconst_1',
		'iconst_1',
		['invokespecial', ('iz', 'fy'), '<init>', ('(Lgm;II)V', '(Lej;II)V')],
		['invokevirtual', c_name, 'a', ('(ILiz;)V', '(ILfy;)V')],
		'return'
	])

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.recipe.SmeltingRecipeManager')
