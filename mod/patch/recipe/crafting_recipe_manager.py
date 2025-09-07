import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_m,
	get_utf8_at,
	icpx_c,
	icpx_f,
	icpx_m,
	icpx_string
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = ['hk', 'ey'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	_modify_constructor(cf, cp_cache, side_name, side, c_name)

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.recipe.CraftingRecipeManager')

def _modify_constructor(cf, cp_cache, side_name, side, c_name):
	m = get_method(cf, cp_cache, '<init>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])
	patch_code = []

	if mod.config.is_feature_enabled('experimental.hunger_and_thirst'):
		patch_code.extend([
			'aload_0',

			['new', icpx_c(cf, cp_cache, ['iz', 'fy'][side])],
			'dup',
			['getstatic', icpx_f(cf, cp_cache, ['gm', 'ej'][side], 'BOTTLE', ['Lgm;', 'Lej;'][side])],
			'iconst_1',
			['invokespecial', icpx_m(cf, cp_cache, ['iz', 'fy'][side], '<init>', ['(Lgm;I)V', '(Lej;I)V'][side])],

			['bipush', 7],
			['anewarray', icpx_c(cf, cp_cache, 'java/lang/Object')],

			'dup',
			'iconst_0',
			['ldc_w', icpx_string(cf, cp_cache, ' a ')],
			'aastore',

			'dup',
			'iconst_1',
			['ldc_w', icpx_string(cf, cp_cache, 'b b')],
			'aastore',

			'dup',
			'iconst_2',
			['ldc_w', icpx_string(cf, cp_cache, ' b ')],
			'aastore',

			'dup',
			'iconst_3',
			['bipush', 97],
			['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
			'aastore',

			'dup',
			'iconst_4',
			['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'y', ['Luu;', 'Lna;'][side])],
			'aastore',

			'dup',
			'iconst_5',
			['bipush', 98],
			['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
			'aastore',

			'dup',
			['bipush', 6],
			['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'N', ['Luu;', 'Lna;'][side])],
			'aastore',

			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V'][side])]
		])

	if mod.config.is_feature_enabled('debug.debug_recipes'):
		patch_code.extend([
			'aload_0',
			['new', icpx_c(cf, cp_cache, ['iz', 'fy'][side])],
			'dup',
			['getstatic', icpx_f(cf, cp_cache, ['gm', 'ej'][side], 'l', ['Lgm;', 'Lej;'][side])],
			'iconst_1',
			['bipush', 0],
			['invokespecial', icpx_m(cf, cp_cache, ['iz', 'fy'][side], '<init>', ['(Lgm;II)V', '(Lej;II)V'][side])],
			'iconst_1',
			['anewarray', icpx_c(cf, cp_cache, 'java/lang/Object')],
			'dup',
			'iconst_0',
			['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'w', ['Luu;', 'Lna;'][side])],
			'aastore',
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'b', ['(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V'][side])]
		])

	if side_name.__eq__('client'):
		a_code[0x03] = a_code[0x03][0:3189] + instructions.assemble(0, patch_code) + a_code[0x03][3189:3238]

	if side_name.__eq__('server'):
		a_code[0x03] = a_code[0x03][0:3189] + instructions.assemble(0, patch_code) + a_code[0x03][3189:3238]

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
