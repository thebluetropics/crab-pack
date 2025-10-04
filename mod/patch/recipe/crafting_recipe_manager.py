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
	if not mod.config.is_one_of_features_enabled(['block.fortress_bricks', 'etc.hunger_and_thirst', 'debug.debug_recipes', 'block.mortar']):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['hk', 'ey'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_constructor(cf, cp_cache, side_name, side, c_name)

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.recipe.CraftingRecipeManager')

def _modify_constructor(cf, cp_cache, side_name, side, c_name):
	m = get_method(cf, cp_cache, '<init>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])
	patch_code = []

	if mod.config.is_feature_enabled('block.fortress_bricks'):
		patch_code.extend([
			'aload_0',
			['new', ('iz', 'fy')],
			'dup',
			['getstatic', ('uu', 'na'), 'LIGHT_FORTRESS_BRICKS', ('Luu;', 'Lna;')],
			'iconst_4',
			'iconst_1',
			['invokespecial', ('iz', 'fy'), '<init>', ('(Luu;II)V', '(Lna;II)V')],
			['bipush', 4],
			['anewarray', 'java/lang/Object'],

			'dup',
			'iconst_0',
			['ldc_w.string', 'aa'],
			'aastore',

			'dup',
			'iconst_1',
			['ldc_w.string', 'aa'],
			'aastore',

			'dup',
			'iconst_2',
			['bipush', 97],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			'iconst_3',
			['getstatic', ('uu', 'na'), 'x', ('Luu;', 'Lna;')],
			'aastore',

			['invokevirtual', c_name, 'a', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])
		patch_code.extend([
			'aload_0',
			['new', ('iz', 'fy')],
			'dup',
			['getstatic', ('uu', 'na'), 'FORTRESS_BRICKS', ('Luu;', 'Lna;')],
			'iconst_4',
			'iconst_1',
			['invokespecial', ('iz', 'fy'), '<init>', ('(Luu;II)V', '(Lna;II)V')],
			['bipush', 6],
			['anewarray', 'java/lang/Object'],

			'dup',
			'iconst_0',
			['ldc_w.string', 'ab'],
			'aastore',

			'dup',
			'iconst_1',
			['ldc_w.string', 'ba'],
			'aastore',

			'dup',
			'iconst_2',
			['bipush', 97],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			'iconst_3',
			['getstatic', ('uu', 'na'), 'x', ('Luu;', 'Lna;')],
			'aastore',

			'dup',
			'iconst_4',
			['bipush', 98],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			'iconst_5',
			['getstatic', ('uu', 'na'), 'u', ('Luu;', 'Lna;')],
			'aastore',

			['invokevirtual', c_name, 'a', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		patch_code.extend([
			'aload_0',

			['new', ('iz', 'fy')],
			'dup',
			['getstatic', ('gm', 'ej'), 'BOTTLE', ('Lgm;', 'Lej;')],
			'iconst_1',
			['invokespecial', ('iz', 'fy'), '<init>', ('(Lgm;I)V', '(Lej;I)V')],

			['bipush', 7],
			['anewarray', 'java/lang/Object'],

			'dup',
			'iconst_0',
			['ldc_w.string', ' a '],
			'aastore',

			'dup',
			'iconst_1',
			['ldc_w.string', 'b b'],
			'aastore',

			'dup',
			'iconst_2',
			['ldc_w.string', ' b '],
			'aastore',

			'dup',
			'iconst_3',
			['bipush', 97],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			'iconst_4',
			['getstatic', ('uu', 'na'), 'y', ('Luu;', 'Lna;')],
			'aastore',

			'dup',
			'iconst_5',
			['bipush', 98],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			['bipush', 6],
			['getstatic', ('uu', 'na'), 'N', ('Luu;', 'Lna;')],
			'aastore',

			['invokevirtual', c_name, 'a', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		patch_code.extend([
			'aload_0',

			['new', ('iz', 'fy')],
			'dup',
			['getstatic', ('gm', 'ej'), 'BOTTLE', ('Lgm;', 'Lej;')],
			'iconst_1',
			['invokespecial', ('iz', 'fy'), '<init>', ('(Lgm;I)V', '(Lej;I)V')],

			['bipush', 7],
			['anewarray', 'java/lang/Object'],

			'dup',
			'iconst_0',
			['ldc_w.string', ' a '],
			'aastore',

			'dup',
			'iconst_1',
			['ldc_w.string', 'b b'],
			'aastore',

			'dup',
			'iconst_2',
			['ldc_w.string', ' b '],
			'aastore',

			'dup',
			'iconst_3',
			['bipush', 97],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			'iconst_4',
			['getstatic', ('uu', 'na'), 'y', ('Luu;', 'Lna;')],
			'aastore',

			'dup',
			'iconst_5',
			['bipush', 98],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			['bipush', 6],
			['getstatic', ('uu', 'na'), 'N', ('Luu;', 'Lna;')],
			'aastore',

			['invokevirtual', c_name, 'a', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

	if mod.config.is_feature_enabled('block.mortar'):
		patch_code.extend([
			'aload_0',

			['new', ('iz', 'fy')],
			'dup',
			['getstatic', ('uu', 'na'), 'MORTAR', 'Lcom/thebluetropics/crabpack/MortarBlock;'],
			'iconst_1',
			['invokespecial', ('iz', 'fy'), '<init>', ('(Luu;I)V', '(Lna;I)V')],

			['bipush', 4],
			['anewarray', 'java/lang/Object'],

			'dup',
			'iconst_0',
			['ldc_w.string', 'a a'],
			'aastore',

			'dup',
			'iconst_1',
			['ldc_w.string', ' a '],
			'aastore',

			'dup',
			'iconst_2',
			['bipush', 97],
			['invokestatic', 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;'],
			'aastore',

			'dup',
			'iconst_3',
			['getstatic', ('uu', 'na'), 'x', ('Luu;', 'Lna;')],
			'aastore',

			['invokevirtual', c_name, 'a', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

	if mod.config.is_feature_enabled('debug.debug_recipes'):
		result_dirt = [('gm', 'ej'), 'BOTTLE', ('Lgm;', 'Lej;')]
		result_sand = [('gm', 'ej'), 'l', ('Lgm;', 'Lej;')]
		result_gravel = [('gm', 'ej'), 'l', ('Lgm;', 'Lej;')]

		patch_code.extend([
			'aload_0',
			['new', ('iz', 'fy')],
			'dup',
			['getstatic', result_dirt[0][side], result_dirt[1], result_dirt[2][side]],
			'iconst_1',
			['bipush', 0],
			['invokespecial', ('iz', 'fy')[side], '<init>', f'({result_dirt[2][side]}II)V'],
			'iconst_1',
			['anewarray', 'java/lang/Object'],
			'dup',
			'iconst_0',
			['getstatic', ('uu', 'na'), 'w', ('Luu;', 'Lna;')],
			'aastore',
			['invokevirtual', c_name, 'b', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

		patch_code.extend([
			'aload_0',
			['new', ('iz', 'fy')],
			'dup',
			['getstatic', result_sand[0][side], result_sand[1], result_sand[2][side]],
			'iconst_1',
			['bipush', 0],
			['invokespecial', ('iz', 'fy'), '<init>', f'({result_sand[2][side]}II)V'],
			'iconst_1',
			['anewarray', 'java/lang/Object'],
			'dup',
			'iconst_0',
			['getstatic', ('uu', 'na'), 'F', ('Luu;', 'Lna;')],
			'aastore',
			['invokevirtual', c_name, 'b', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

		patch_code.extend([
			'aload_0',
			['new', ('iz', 'fy')],
			'dup',
			['getstatic', result_gravel[0][side], result_gravel[1], result_gravel[2][side]],
			'iconst_1',
			['bipush', 0],
			['invokespecial', ('iz', 'fy'), '<init>', f'({result_gravel[2][side]}II)V'],
			'iconst_1',
			['anewarray', 'java/lang/Object'],
			'dup',
			'iconst_0',
			['getstatic', ('uu', 'na'), 'G', ('Luu;', 'Lna;')],
			'aastore',
			['invokevirtual', c_name, 'b', ('(Liz;[Ljava/lang/Object;)V', '(Lfy;[Ljava/lang/Object;)V')]
		])

	if side_name.__eq__('client'):
		a_code[0x03] = a_code[0x03][0:3189] + assemble_code(cf, cp_cache, 0, 3189, patch_code) + a_code[0x03][3189:3238]

	if side_name.__eq__('server'):
		a_code[0x03] = a_code[0x03][0:3189] + assemble_code(cf, cp_cache, 1, 3189, patch_code) + a_code[0x03][3189:3238]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
