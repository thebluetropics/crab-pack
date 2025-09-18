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
	icpx_c,
	icpx_f,
	icpx_m,
	icpx_string,
	get_utf8_at
)

def apply(side_name):
	if not mod.config.is_feature_enabled('block.fortress_bricks') and not mod.config.is_feature_enabled('block.solid_grass_block') and not mod.config.is_feature_enabled('block.mortar'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['uu', 'na'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	if mod.config.is_feature_enabled('block.fortress_bricks'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'FORTRESS_BRICKS', f'L{c_name};'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'LIGHT_FORTRESS_BRICKS', f'L{c_name};'))

	if mod.config.is_feature_enabled('block.solid_grass_block'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'SOLID_GRASS_BLOCK', f'Lcom/thebluetropics/crabpack/SolidGrassBlock;'))

	if mod.config.is_feature_enabled('block.mortar'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'MORTAR', f'Lcom/thebluetropics/crabpack/MortarBlock;'))

	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	_patch_static_initializer(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.Block')

def _patch_static_initializer(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	code = []

	if mod.config.is_feature_enabled('block.fortress_bricks'):
		code.extend([
			['new', icpx_c(cf, cp_cache, c_name)],
			'dup',
			['bipush', 97],
			['sipush', 166],
			['getstatic', icpx_f(cf, cp_cache, ['ln', 'hj'][side], 'e', ['Lln;', 'Lhj;'][side])],
			['invokespecial', icpx_m(cf, cp_cache, c_name, '<init>', ['(IILln;)V', '(IILhj;)V'][side])],
			'fconst_2',
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'c', ['(F)Luu;', '(F)Lna;'][side])],
			['ldc', 22],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'b', ['(F)Luu;', '(F)Lna;'][side])],
			['getstatic', icpx_f(cf, cp_cache, c_name, 'h', ['Lct;', 'Lbu;'][side])],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lct;)Luu;', '(Lbu;)Lna;'][side])],
			['ldc_w', icpx_string(cf, cp_cache, 'fortress_bricks')],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;'][side])],
			['putstatic', icpx_f(cf, cp_cache, c_name, 'FORTRESS_BRICKS', ['Luu;', 'Lna;'][side])],

			['new', icpx_c(cf, cp_cache, c_name)],
			'dup',
			['bipush', 98],
			['sipush', 167],
			['getstatic', icpx_f(cf, cp_cache, ['ln', 'hj'][side], 'e', ['Lln;', 'Lhj;'][side])],
			['invokespecial', icpx_m(cf, cp_cache, c_name, '<init>', ['(IILln;)V', '(IILhj;)V'][side])],
			'fconst_2',
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'c', ['(F)Luu;', '(F)Lna;'][side])],
			['ldc', 22],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'b', ['(F)Luu;', '(F)Lna;'][side])],
			['getstatic', icpx_f(cf, cp_cache, c_name, 'h', ['Lct;', 'Lbu;'][side])],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lct;)Luu;', '(Lbu;)Lna;'][side])],
			['ldc_w', icpx_string(cf, cp_cache, 'light_fortress_bricks')],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;'][side])],
			['putstatic', icpx_f(cf, cp_cache, c_name, 'LIGHT_FORTRESS_BRICKS', ['Luu;', 'Lna;'][side])]
		])

	if mod.config.is_feature_enabled('block.solid_grass_block'):
		code.extend([
			['new', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/SolidGrassBlock')],
			'dup',
			['bipush', 99],
			['invokespecial', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/SolidGrassBlock', '<init>', '(I)V')],
			'iconst_3',
			'i2f',
			'iconst_5',
			'i2f',
			'fdiv',
			['invokevirtual', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/SolidGrassBlock', 'c', ['(F)Luu;', '(F)Lna;'][side])],
			['getstatic', icpx_f(cf, cp_cache, c_name, 'g', ['Lct;', 'Lbu;'][side])],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lct;)Luu;', '(Lbu;)Lna;'][side])],
			['ldc_w', icpx_string(cf, cp_cache, 'solid_grass_block')],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;'][side])],
			['checkcast', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/SolidGrassBlock')],
			['putstatic', icpx_f(cf, cp_cache, c_name, 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;')]
		])

	if mod.config.is_feature_enabled('block.mortar'):
		code.extend([
			['new', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/MortarBlock')],
			'dup',
			['bipush', 100],
			['invokespecial', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/MortarBlock', '<init>', '(I)V')],
			'iconst_3',
			'i2f',
			'iconst_5',
			'i2f',
			'fdiv',
			['invokevirtual', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/MortarBlock', 'c', ['(F)Luu;', '(F)Lna;'][side])],
			['getstatic', icpx_f(cf, cp_cache, c_name, 'g', ['Lct;', 'Lbu;'][side])],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lct;)Luu;', '(Lbu;)Lna;'][side])],
			['ldc_w', icpx_string(cf, cp_cache, 'mortar')],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;'][side])],
			['invokevirtual', icpx_m(cf, cp_cache, c_name, ['j', 'g'][side], ['()Luu;', '()Lna;'][side])],
			['checkcast', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/MortarBlock')],
			['putstatic', icpx_f(cf, cp_cache, c_name, 'MORTAR', 'Lcom/thebluetropics/crabpack/MortarBlock;')]
		])

	a_code[0x03] = a_code[0x03][0:3398] + instructions.assemble(3398, code) + a_code[0x03][3398:3678]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
