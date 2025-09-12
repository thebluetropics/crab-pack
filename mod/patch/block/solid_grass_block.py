import os, mod

from mod.method import create_method
from mod import (
	attribute,
	instructions,
	constant_pool
)
from mod.class_file import (
	create_class_file,
	assemble_class_file
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	i2cpx_c,
	icpx_i
)

def apply(side_name):
	if not mod.config.is_feature_enabled('block.solid_grass_block'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/SolidGrassBlock'

	cf = create_class_file()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['uu', 'na'][side])

	methods = [
		_create_constructor(cf, cp_cache, side, c_name),
		_create_get_dropped_item_id_method(cf, cp_cache, side)
	]

	if side_name.__eq__('client'):
		methods.append(_create_get_color_multiplier_method(cf, cp_cache))

	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(assemble_class_file(cf))

	print(f'Created {side_name}:SolidGrassBlock.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = instructions.assemble(0, [
		'aload_0',
		'iload_1',
		['getstatic', icpx_f(cf, cp_cache, ['ln', 'hj'][side], 'b', ['Lln;', 'Lhj;'][side])],
		['invokespecial', icpx_m(cf, cp_cache, ['uu', 'na'][side], '<init>', ['(ILln;)V', '(ILhj;)V'][side])],
		'aload_0',
		'iconst_0',
		['putfield', icpx_f(cf, cp_cache, c_name, 'bm', 'I')],
		'return'
	])
	a_code = attribute.code.assemble([
		(3).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _create_get_color_multiplier_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'b', '(Lxp;III)I')

	code = instructions.assemble(0, [
		'aload_1',
		['invokeinterface', icpx_i(cf, cp_cache, 'xp', 'a', '()Lxv;'), 1],
		['iload', 2],
		['iload', 4],
		'iconst_1',
		'iconst_1',
		['invokevirtual', icpx_m(cf, cp_cache, 'xv', 'a', '(IIII)[Lkd;')],
		'pop',

		'aload_1',
		['invokeinterface', icpx_i(cf, cp_cache, 'xp', 'a', '()Lxv;'), 1],
		['getfield', icpx_f(cf, cp_cache, 'xv', 'a', '[D')],
		'iconst_0',
		'daload',
		['dstore', 5],

		'aload_1',
		['invokeinterface', icpx_i(cf, cp_cache, 'xp', 'a', '()Lxv;'), 1],
		['getfield', icpx_f(cf, cp_cache, 'xv', 'b', '[D')],
		'iconst_0',
		'daload',
		['dstore', 7],

		['dload', 5],
		['dload', 7],
		['invokestatic', icpx_m(cf, cp_cache, 'ia', 'a', '(DD)I')],

		'ireturn'
	])
	a_code = attribute.code.assemble([
		(5).to_bytes(2),
		(9).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _create_get_dropped_item_id_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', '(ILjava/util/Random;)I')

	code = instructions.assemble(0, [
    ['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'w', ['Luu;', 'Lna;'][side])],
    'iconst_0',
    ['aload', 2],
    ['invokevirtual', icpx_m(cf, cp_cache, ['uu', 'na'][side], 'a', '(ILjava/util/Random;)I')],
		'ireturn'
	])
	a_code = attribute.code.assemble([
		(3).to_bytes(2),
		(3).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
