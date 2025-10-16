from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_one_of_features_enabled([
		'block.fortress_bricks',
		'block.solid_grass_block',
		'block.mortar',
		'block.smelter',
		'block.persistent_leaves'
	]): return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['uu', 'na'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('block.fortress_bricks'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'FORTRESS_BRICKS', ['Luu;', 'Lna;'][side]))
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'LIGHT_FORTRESS_BRICKS', ['Luu;', 'Lna;'][side]))

	if mod.config.is_feature_enabled('block.solid_grass_block'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;'))

	if mod.config.is_feature_enabled('block.mortar'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'MORTAR', 'Lcom/thebluetropics/crabpack/MortarBlock;'))

	if mod.config.is_feature_enabled('block.smelter'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'SMELTER', 'Lcom/thebluetropics/crabpack/SmelterBlock;'))

	if mod.config.is_feature_enabled('block.persistent_leaves'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'))

	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	_patch_static_initializer(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.Block')

def _patch_static_initializer(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	code = []

	if mod.config.is_feature_enabled('block.fortress_bricks'):
		code.extend([
			['new', c_name],
			'dup',
			['bipush', 97],
			['sipush', 166],
			['getstatic', ('ln', 'hj'), 'e', ('Lln;', 'Lhj;')],
			['invokespecial', c_name, '<init>', ('(IILln;)V', '(IILhj;)V')],
			'fconst_2',
			['invokevirtual', c_name, 'c', ('(F)Luu;', '(F)Lna;')],
			['ldc_w.f32', 10.0],
			['invokevirtual', c_name, 'b', ('(F)Luu;', '(F)Lna;')],
			['getstatic', c_name, 'h', ('Lct;', 'Lbu;')],
			['invokevirtual', c_name, 'a', ('(Lct;)Luu;', '(Lbu;)Lna;')],
			['ldc_w.string', 'fortress_bricks'],
			['invokevirtual', c_name, 'a', ('(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;')],
			['putstatic', c_name, 'FORTRESS_BRICKS', ('Luu;', 'Lna;')],

			['new', c_name],
			'dup',
			['bipush', 98],
			['sipush', 167],
			['getstatic', ('ln', 'hj'), 'e', ('Lln;', 'Lhj;')],
			['invokespecial', c_name, '<init>', ('(IILln;)V', '(IILhj;)V')],
			'fconst_2',
			['invokevirtual', c_name, 'c', ('(F)Luu;', '(F)Lna;')],
			['ldc_w.f32', 10.0],
			['invokevirtual', c_name, 'b', ('(F)Luu;', '(F)Lna;')],
			['getstatic', c_name, 'h', ('Lct;', 'Lbu;')],
			['invokevirtual', c_name, 'a', ('(Lct;)Luu;', '(Lbu;)Lna;')],
			['ldc_w.string', 'light_fortress_bricks'],
			['invokevirtual', c_name, 'a', ('(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;')],
			['putstatic', c_name, 'LIGHT_FORTRESS_BRICKS', ('Luu;', 'Lna;')]
		])

	if mod.config.is_feature_enabled('block.solid_grass_block'):
		code.extend([
			['new', 'com/thebluetropics/crabpack/SolidGrassBlock'],
			'dup',
			['bipush', 99],
			['invokespecial', 'com/thebluetropics/crabpack/SolidGrassBlock', '<init>', '(I)V'],
			'iconst_3',
			'i2f',
			'iconst_5',
			'i2f',
			'fdiv',
			['invokevirtual', 'com/thebluetropics/crabpack/SolidGrassBlock', 'c', ('(F)Luu;', '(F)Lna;')],
			['getstatic', c_name, 'g', ('Lct;', 'Lbu;')],
			['invokevirtual', c_name, 'a', ('(Lct;)Luu;', '(Lbu;)Lna;')],
			['ldc_w.string', 'solid_grass_block'],
			['invokevirtual', c_name, 'a', ('(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;')],
			['checkcast', 'com/thebluetropics/crabpack/SolidGrassBlock'],
			['putstatic', c_name, 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;']
		])

	if mod.config.is_feature_enabled('block.mortar'):
		code.extend([
			['new', 'com/thebluetropics/crabpack/MortarBlock'],
			'dup',
			['bipush', 100],
			['invokespecial', 'com/thebluetropics/crabpack/MortarBlock', '<init>', '(I)V'],
			'iconst_3',
			'i2f',
			'iconst_5',
			'i2f',
			'fdiv',
			['invokevirtual', 'com/thebluetropics/crabpack/MortarBlock', 'c', ('(F)Luu;', '(F)Lna;')],
			['getstatic', c_name, 'g', ('Lct;', 'Lbu;')],
			['invokevirtual', c_name, 'a', ('(Lct;)Luu;', '(Lbu;)Lna;')],
			['ldc_w.string', 'mortar'],
			['invokevirtual', c_name, 'a', ('(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;')],
			['invokevirtual', c_name, ('j', 'g'), ('()Luu;', '()Lna;')],
			['checkcast', 'com/thebluetropics/crabpack/MortarBlock'],
			['putstatic', c_name, 'MORTAR', 'Lcom/thebluetropics/crabpack/MortarBlock;']
		])

	if mod.config.is_feature_enabled('block.smelter'):
		code.extend([
			['new', 'com/thebluetropics/crabpack/SmelterBlock'],
			'dup',
			['bipush', 101],
			['invokespecial', 'com/thebluetropics/crabpack/SmelterBlock', '<init>', '(I)V'],
			'iconst_3',
			'i2f',
			'iconst_5',
			'i2f',
			'fdiv',
			['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlock', 'c', ('(F)Luu;', '(F)Lna;')],
			['getstatic', c_name, 'g', ('Lct;', 'Lbu;')],
			['invokevirtual', c_name, 'a', ('(Lct;)Luu;', '(Lbu;)Lna;')],
			['ldc_w.string', 'smelter'],
			['invokevirtual', c_name, 'a', ('(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;')],
			['invokevirtual', c_name, ('j', 'g'), ('()Luu;', '()Lna;')],
			['checkcast', 'com/thebluetropics/crabpack/SmelterBlock'],
			['putstatic', c_name, 'SMELTER', 'Lcom/thebluetropics/crabpack/SmelterBlock;']
		])

	if mod.config.is_feature_enabled('block.persistent_leaves'):
		code.extend([
			['new', 'com/thebluetropics/crabpack/PersistentLeavesBlock'],
			'dup', ['bipush', 102], ['invokespecial', 'com/thebluetropics/crabpack/PersistentLeavesBlock', '<init>', '(I)V'],
			['ldc_w.f32', 0.2], ['invokevirtual', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'c', ('(F)Luu;', '(F)Lna;')],
			['getstatic', c_name, 'g', ('Lct;', 'Lbu;')], ['invokevirtual', c_name, 'a', ('(Lct;)Luu;', '(Lbu;)Lna;')],
			['ldc_w.string', 'persistent_leaves'], ['invokevirtual', c_name, 'a', ('(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;')],
			['invokevirtual', c_name, ('j', 'g'), ('()Luu;', '()Lna;')],
			'iconst_1', ['invokevirtual', c_name, ('g', 'f'), ('(I)Luu;', '(I)Lna;')],
			['checkcast', 'com/thebluetropics/crabpack/PersistentLeavesBlock'],
			['putstatic', c_name, 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;']
		])

	code_2 = []

	if mod.config.is_feature_enabled('block.persistent_leaves'):
		code_2.extend([
			['getstatic', ('gm', 'ej'), 'c', ('[Lgm;', '[Lej;')],
			['getstatic', ('uu', 'na'), 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'],
			['getfield', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'bn', 'I'],
			['new', 'com/thebluetropics/crabpack/PersistentLeavesBlockItem'],
			'dup',
			['getstatic', ('uu', 'na'), 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'],
			['getfield', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'bn', 'I'],
			['sipush', 256],
			'isub',
			['invokespecial', 'com/thebluetropics/crabpack/PersistentLeavesBlockItem', '<init>', '(I)V'],
			['ldc_w.string', 'persistent_leaves'],
			['invokevirtual', 'com/thebluetropics/crabpack/PersistentLeavesBlockItem', 'a', ('(Ljava/lang/String;)Lgm;', '(Ljava/lang/String;)Lej;')],
			'aastore',
		])

	a_code[0x03] = a_code[0x03][0:3398] + assemble_code(cf, cp_cache, side, 3398, code) + a_code[0x03][3398:3558] + assemble_code(cf, cp_cache, side, 3558, code_2) + a_code[0x03][3558:3678]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
