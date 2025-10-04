import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
)
from modmaker.f import (
	create_field
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
	c_name = ['gm', 'ej'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('food.raw_squid_and_calamari'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'raw_squid', f'L{c_name};'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'calamari', f'L{c_name};'))

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'BOTTLE', f'L{c_name};'))

	if mod.config.is_feature_enabled('item.cloth'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'CLOTH', f'L{c_name};'))

	if mod.config.is_feature_enabled('block.smelter'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'STEEL_INGOT', f'L{c_name};'))

	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	_modify_static_initializer(cf, cp_cache, side_name, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as f:
		f.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.Item')

def _modify_static_initializer(cf, cp_cache, side_name, side):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])
	patch_code = []

	if mod.config.is_feature_enabled('food.raw_squid_and_calamari'): patch_code.extend([
		['new', ('yw', 'px')],
		'dup', ['sipush', 1024], 'iconst_1', 'iconst_0', ['invokespecial', ('yw', 'px'), '<init>', '(IIZ)V'],
		'iconst_2', ['bipush', 15], ['invokevirtual', ('yw', 'px'), 'a', ('(II)Lgm;', '(II)Lej;')],
		['ldc_w.string', 'raw_squid'], ['invokevirtual', ('gm', 'ej'), 'a', ('(Ljava/lang/String;)Lgm;', '(Ljava/lang/String;)Lej;')],
		['putstatic', ('gm', 'ej'), 'raw_squid', ('Lgm;', 'Lej;')],

		['new', ('yw', 'px')],
		'dup', ['sipush', 1025], 'iconst_5', 'iconst_0', ['invokespecial', ('yw', 'px'), '<init>', '(IIZ)V'],
		'iconst_3', ['bipush', 15], ['invokevirtual', ('yw', 'px'), 'a', ('(II)Lgm;', '(II)Lej;')],
		['ldc_w.string', 'raw_squid'], ['invokevirtual', ('gm', 'ej'), 'a', ('(Ljava/lang/String;)Lgm;', '(Ljava/lang/String;)Lej;')],
		['putstatic', ('gm', 'ej'), 'calamari', ('Lgm;', 'Lej;')],
	])

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'): patch_code.extend([
		['new', 'com/thebluetropics/crabpack/BottleItem'],
		'dup', ['sipush', 1026], ['invokespecial', 'com/thebluetropics/crabpack/BottleItem', '<init>', '(I)V'],
		'iconst_4',
		['bipush', 15],
		['invokevirtual', 'com/thebluetropics/crabpack/BottleItem', 'a', ('(II)Lgm;', '(II)Lej;')],
		['ldc_w.string', 'bottle'],
		['invokevirtual', ('gm', 'ej'), 'a', ('(Ljava/lang/String;)Lgm;', '(Ljava/lang/String;)Lej;')],
		['putstatic', ('gm', 'ej'), 'BOTTLE', ('Lgm;', 'Lej;')]
	])

	if mod.config.is_feature_enabled('item.cloth'):
		patch_code.extend([
			['new', ('gm', 'ej')],
			'dup',
			['sipush', 1028],
			['invokespecial', ('gm', 'ej'), '<init>', '(I)V'],
			['bipush', 6],
			['bipush', 15],
			['invokevirtual', ('gm', 'ej'), 'a', ('(II)Lgm;', '(II)Lej;')],
			['ldc_w.string', 'cloth'],
			['invokevirtual', ('gm', 'ej'), 'a', ('(Ljava/lang/String;)Lgm;', '(Ljava/lang/String;)Lej;')],
			['putstatic', ('gm', 'ej'), 'CLOTH', ('Lgm;', 'Lej;')]
		])

	if mod.config.is_feature_enabled('block.smelter'):
		patch_code.extend([
			['new', ('gm', 'ej')],
			'dup',
			['sipush', 1027],
			['invokespecial', ('gm', 'ej'), '<init>', '(I)V'],
			'iconst_5',
			['bipush', 15],
			['invokevirtual', ('gm', 'ej'), 'a', ('(II)Lgm;', '(II)Lej;')],
			['ldc_w.string', 'steel_ingot'],
			['invokevirtual', ('gm', 'ej'), 'a', ('(Ljava/lang/String;)Lgm;', '(Ljava/lang/String;)Lej;')],
			['putstatic', ('gm', 'ej'), 'STEEL_INGOT', ('Lgm;', 'Lej;')]
		])

	if side_name.__eq__('client'):
		a_code[0x03] = a_code[0x03][0:2664] + assemble_code(cf, cp_cache, side, 2664, patch_code) + a_code[0x03][2664:2668]

	if side_name.__eq__('server'):
		a_code[0x03] = a_code[0x03][0:2664] + assemble_code(cf, cp_cache, side, 2664, patch_code) + a_code[0x03][2664:2668]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
