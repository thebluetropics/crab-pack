import mod

from mod.attribute import get_attribute
from mod.field import create_field
from mod.method import get_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	get_utf8_at,
	icpx_string,
	icpx_c
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = ['gm', 'ej'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	if mod.config.is_feature_enabled('food.raw_squid_and_calamari'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'raw_squid', f'L{c_name};'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'calamari', f'L{c_name};'))

	if mod.config.is_feature_enabled('experimental.hunger_and_thirst'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'BOTTLE', f'L{c_name};'))

	if mod.config.is_feature_enabled('experimental.cloth'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'CLOTH', f'L{c_name};'))

	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	_modify_static_initializer(cf, cp_cache, side_name, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.Item')

def _modify_static_initializer(cf, cp_cache, side_name, side):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])
	patch_code = []

	if side_name.__eq__('client'):
		if mod.config.is_feature_enabled('food.raw_squid_and_calamari'): patch_code.extend([
			['new', icpx_c(cf, cp_cache, 'yw')],
			'dup',
			['sipush', 1024],
			'iconst_1',
			'iconst_0',
			['invokespecial', icpx_m(cf, cp_cache, 'yw', '<init>', '(IIZ)V')],
			'iconst_2',
			['bipush', 15],
			['invokevirtual', icpx_m(cf, cp_cache, 'yw', 'a', '(II)Lgm;')],
			['ldc_w', icpx_string(cf, cp_cache, 'raw_squid')],
			['invokevirtual', icpx_m(cf, cp_cache, 'gm', 'a', '(Ljava/lang/String;)Lgm;')],
			['putstatic', icpx_f(cf, cp_cache, 'gm', 'raw_squid', 'Lgm;')],
			['new', icpx_c(cf, cp_cache, 'yw')],
			'dup',
			['sipush', 1025],
			'iconst_5',
			'iconst_0',
			['invokespecial', icpx_m(cf, cp_cache, 'yw', '<init>', '(IIZ)V')],
			'iconst_3',
			['bipush', 15],
			['invokevirtual', icpx_m(cf, cp_cache, 'yw', 'a', '(II)Lgm;')],
			['ldc_w', icpx_string(cf, cp_cache, 'raw_squid')],
			['invokevirtual', icpx_m(cf, cp_cache, 'gm', 'a', '(Ljava/lang/String;)Lgm;')],
			['putstatic', icpx_f(cf, cp_cache, 'gm', 'calamari', 'Lgm;')],
		])

		if mod.config.is_feature_enabled('experimental.hunger_and_thirst'): patch_code.extend([
			['new', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/BottleItem')],
			'dup',
			['sipush', 1026],
			['invokespecial', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/BottleItem', '<init>', '(I)V')],
			'iconst_4',
			['bipush', 15],
			['invokevirtual', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/BottleItem', 'a', '(II)Lgm;')],
			['ldc_w', icpx_string(cf, cp_cache, 'bottle')],
			['invokevirtual', icpx_m(cf, cp_cache, 'gm', 'a', '(Ljava/lang/String;)Lgm;')],
			['putstatic', icpx_f(cf, cp_cache, 'gm', 'BOTTLE', 'Lgm;')]
		])

		if mod.config.is_feature_enabled('experimental.cloth'):
			patch_code.extend([
				['new', icpx_c(cf, cp_cache, 'gm')],
				'dup',
				['sipush', 1027],
				['invokespecial', icpx_m(cf, cp_cache, 'gm', '<init>', '(I)V')],
				'iconst_5',
				['bipush', 15],
				['invokevirtual', icpx_m(cf, cp_cache, 'gm', 'a', '(II)Lgm;')],
				['ldc_w', icpx_string(cf, cp_cache, 'cloth')],
				['invokevirtual', icpx_m(cf, cp_cache, 'gm', 'a', '(Ljava/lang/String;)Lgm;')],
				['putstatic', icpx_f(cf, cp_cache, 'gm', 'CLOTH', 'Lgm;')]
			])

		a_code[0x03] = a_code[0x03][0:2664] + instructions.assemble(2664, patch_code) + a_code[0x03][2664:2668]

	if side_name.__eq__('server'):
		if mod.config.is_feature_enabled('food.raw_squid_and_calamari'): patch_code.extend([
			['new', icpx_c(cf, cp_cache, 'px')],
			'dup',
			['sipush', 1024],
			'iconst_1',
			'iconst_0',
			['invokespecial', icpx_m(cf, cp_cache, 'px', '<init>', '(IIZ)V')],
			'iconst_2',
			['bipush', 15],
			['invokevirtual', icpx_m(cf, cp_cache, 'px', 'a', '(II)Lej;')],
			['ldc_w', icpx_string(cf, cp_cache, 'calamari')],
			['invokevirtual', icpx_m(cf, cp_cache, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
			['putstatic', icpx_f(cf, cp_cache, 'ej', 'raw_squid', 'Lej;')],
			['new', icpx_c(cf, cp_cache, 'px')],
			'dup',
			['sipush', 1025],
			'iconst_5',
			'iconst_0',
			['invokespecial', icpx_m(cf, cp_cache, 'px', '<init>', '(IIZ)V')],
			'iconst_3',
			['bipush', 15],
			['invokevirtual', icpx_m(cf, cp_cache, 'px', 'a', '(II)Lej;')],
			['ldc_w', icpx_string(cf, cp_cache, 'calamari')],
			['invokevirtual', icpx_m(cf, cp_cache, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
			['putstatic', icpx_f(cf, cp_cache, 'ej', 'calamari', 'Lej;')],
		])

		if mod.config.is_feature_enabled('experimental.hunger_and_thirst'): patch_code.extend([
			['new', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/BottleItem')],
			'dup',
			['sipush', 1026],
			['invokespecial', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/BottleItem', '<init>', '(I)V')],
			'iconst_4',
			['bipush', 15],
			['invokevirtual', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/BottleItem', 'a', '(II)Lej;')],
			['ldc_w', icpx_string(cf, cp_cache, 'bottle')],
			['invokevirtual', icpx_m(cf, cp_cache, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
			['putstatic', icpx_f(cf, cp_cache, 'ej', 'BOTTLE', 'Lej;')]
		])

		if mod.config.is_feature_enabled('experimental.cloth'):
			patch_code.extend([
				['new', icpx_c(cf, cp_cache, 'ej')],
				'dup',
				['sipush', 1027],
				['invokespecial', icpx_m(cf, cp_cache, 'ej', '<init>', '(I)V')],
				'iconst_5',
				['bipush', 15],
				['invokevirtual', icpx_m(cf, cp_cache, 'ej', 'a', '(II)Lej;')],
				['ldc_w', icpx_string(cf, cp_cache, 'cloth')],
				['invokevirtual', icpx_m(cf, cp_cache, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
				['putstatic', icpx_f(cf, cp_cache, 'ej', 'CLOTH', 'Lej;')]
			])

		a_code[0x03] = a_code[0x03][0:2664] + instructions.assemble(2664, patch_code) + a_code[0x03][2664:2668]

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
