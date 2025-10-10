from modmaker import *
import os, mod

def apply(side_name):
	if not mod.config.is_feature_enabled('block.mortar'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/MortarBlock'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['uu', 'na'][side])

	methods = [
		_create_constructor(cf, cp_cache, side, c_name)
	]

	if side_name.__eq__('client'):
		methods.append(_create_get_render_type_method(cf, cp_cache))
		methods.append(_create_get_bounding_box_method(cf, cp_cache))

	methods.append(_create_is_opaque_method(cf, cp_cache, side))
	methods.append(_create_use_method(cf, cp_cache, side, c_name))
	methods.append(_create_drop_stacks_method(cf, cp_cache, side, c_name))
	methods.append(_create_get_collision_shape_method(cf, cp_cache, side))
	methods.append(_create_is_full_cube_method(cf, cp_cache, side))

	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:MortarBlock.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'iload_1',
		['getstatic', ('ln', 'hj'), 'b', ('Lln;', 'Lhj;')],
		['invokespecial', ('uu', 'na'), '<init>', ('(ILln;)V', '(ILhj;)V')],
		'aload_0',
		'iconst_3',
		['putfield', c_name, 'bm', 'I'],
		'return'
	])
	a_code = a_code_assemble([
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

def _create_get_render_type_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'b', '()I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		['bipush', 50],
		'ireturn'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
		(1).to_bytes(2),
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

def _create_is_opaque_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], ['c', 'a'][side], '()Z')

	code = assemble_code(cf, cp_cache, side, 0, [
		'iconst_0',
		'ireturn'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
		(1).to_bytes(2),
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

def _create_use_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lfd;IIILgs;)Z', '(Ldj;IIILem;)Z'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['invokevirtual', ('fd', 'dj'), ('e', 'c'), '(III)I'],
		'iconst_3',
		['if_icmpne', 'L0'],

		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		'iconst_0',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],

		'aload_0',
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['new', ('iz', 'fy')],
		'dup',
		['sipush', 351],
		'iconst_1',
		['bipush', 15],
		['invokespecial', ('iz', 'fy'), '<init>', '(III)V'],
		['invokevirtual', c_name, 'a', ('(Lfd;IIILiz;)V', '(Ldj;IIILfy;)V')],

		'iconst_1',
		'ireturn',

		['label', 'L0'],
		'iconst_0',
		'ireturn'
	])
	a_code = a_code_assemble([
		(10).to_bytes(2),
		(6).to_bytes(2),
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

def _create_drop_stacks_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lfd;IIIIF)V', '(Ldj;IIIIF)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['fload', 6],
		['invokespecial', ('uu', 'na'), 'a', ('(Lfd;IIIIF)V', '(Ldj;IIIIF)V')],

		['iload', 5],
		'iconst_0',
		['if_icmple', 'L0'],

		['iload', 5],
		'iconst_4',
		['if_icmpge', 'L0'],

		'aload_0',
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['new', ('iz', 'fy')],
		'dup',
		['getstatic', ('gm', 'ej'), 'Q', ('Lgm;', 'Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],
		['iload', 5],
		'iconst_0',
		['invokespecial', ('iz', 'fy'), '<init>', '(III)V'],
		['invokevirtual', c_name, 'a', ('(Lfd;IIILiz;)V', '(Ldj;IIILfy;)V')],
		'return',

		['label', 'L0'],
		'return'
	])
	a_code = a_code_assemble([
		(10).to_bytes(2),
		(7).to_bytes(2),
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

def _create_get_collision_shape_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'e', ['(Lfd;III)Leq;', '(Ldj;III)Lcz;'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		['iload', 2],
		'i2d',
		['ldc2_w.f64', 1.0 / 16.0],
		'dadd',

		['iload', 3],
		'i2d',
		'dconst_0',
		'dadd',

		['iload', 4],
		'i2d',
		['ldc2_w.f64', 1.0 / 16.0],
		'dadd',

		['iload', 2],
		'i2d',
		['ldc2_w.f64', 15.0 / 16.0],
		'dadd',

		['iload', 3],
		'i2d',
		['ldc2_w.f64', 6.0 / 16.0],
		'dadd',

		['iload', 4],
		'i2d',
		['ldc2_w.f64', 15.0 / 16.0],
		'dadd',

		['invokestatic', ('eq', 'cz'), 'b', ('(DDDDDD)Leq;', '(DDDDDD)Lcz;')],
		'areturn'
	])
	a_code = a_code_assemble([
		(14).to_bytes(2),
		(5).to_bytes(2),
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

def _create_get_bounding_box_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'f', '(Lfd;III)Leq;')

	code = assemble_code(cf, cp_cache, 0, 0, [
		['iload', 2],
		'i2d',
		['ldc2_w.f64', 1.0 / 16.0],
		'dadd',

		['iload', 3],
		'i2d',
		'dconst_0',
		'dadd',

		['iload', 4],
		'i2d',
		['ldc2_w.f64', 1.0 / 16.0],
		'dadd',

		['iload', 2],
		'i2d',
		['ldc2_w.f64', 15.0 / 16.0],
		'dadd',

		['iload', 3],
		'i2d',
		['ldc2_w.f64', 6.0 / 16.0],
		'dadd',

		['iload', 4],
		'i2d',
		['ldc2_w.f64', 15.0 / 16.0],
		'dadd',

		['invokestatic', 'eq', 'b', '(DDDDDD)Leq;'],
		'areturn'
	])
	a_code = a_code_assemble([
		(14).to_bytes(2),
		(5).to_bytes(2),
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

def _create_is_full_cube_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], ['d', 'b'][side], '()Z')

	code = assemble_code(cf, cp_cache, side, 0, [
		'iconst_0',
		'ireturn'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
		(1).to_bytes(2),
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
