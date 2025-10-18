from modmaker import *
import os, mod

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/PersistentLeavesBlock'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['nr', 'in'][side])

	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'useFancyGraphics', 'Z'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_is_opaque_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_after_break_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_get_dropped_item_id_method(cf, cp_cache, side))

	if side_name.__eq__('client'):
		cf[0x0d].append(_create_set_fancy_graphics(cf, cp_cache, c_name))
		cf[0x0d].append(_create_get_color_method(cf, cp_cache))
		cf[0x0d].append(_create_get_texture_method(cf, cp_cache, c_name))
		cf[0x0d].append(_create_get_color_multiplier_method(cf, cp_cache))

	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:PersistentLeavesBlock.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'iload_1',
		['bipush', 52],
		['getstatic', ('ln', 'hj'), 'i', ('Lln;', 'Lhj;')],
		'iconst_0',
		['invokespecial', ('nr', 'in'), '<init>', ('(IILln;Z)V', '(IILhj;Z)V')],
		'aload_0', 'iconst_0', ['putfield', c_name, 'useFancyGraphics', 'Z'],
		'return'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
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

def _create_is_opaque_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], ['c', 'a'][side], '()Z')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'b', 'Z'],
		['ifne', 'L1'],
		'iconst_1',
		['goto', 'L2'],
		['label', 'L1'],
		'iconst_0',
		['label', 'L2'],
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

def _create_set_fancy_graphics(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'setFancyGraphics', '(Z)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0', 'iload_1', ['putfield', c_name, 'b', 'Z'],
		'aload_0', 'iload_1', ['putfield', c_name, 'useFancyGraphics', 'Z'],
		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
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

def _create_get_color_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'b', '(I)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'iload_1', 'iconst_0', ['if_icmpne', 'L1'],
		['invokestatic', 'jh', 'c', '()I'], 'ireturn',

		['label', 'L1'],
		'iload_1', 'iconst_1', ['if_icmpne', 'L2'],
		['invokestatic', 'jh', 'b', '()I'], 'ireturn',

		['label', 'L2'],
		'iload_1', 'iconst_2', ['if_icmpne', 'L3'],
		['invokestatic', 'jh', 'a', '()I'], 'ireturn',

		['label', 'L3'],
		['ldc_w.i32', 0xffffff],
		'ireturn'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
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

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_1', 'iload_2', 'iload_3', ['iload', 4], ['invokeinterface', 'xp', 'e', '(III)I', 4],
		['istore', 5],

		['iload', 5], 'iconst_1', ['if_icmpne', 'L2'],
		['invokestatic', 'jh', 'b', '()I'], 'ireturn',

		['label', 'L2'],
		['iload', 5], 'iconst_2', ['if_icmpne', 'L3'],
		['invokestatic', 'jh', 'a', '()I'], 'ireturn',

		['label', 'L3'],
		'aload_1',
		['invokeinterface', 'xp', 'a', '()Lxv;', 1],
		'iload_2',
		['iload', 4],
		'iconst_1',
		'iconst_1',
		['invokevirtual', 'xv', 'a', '(IIII)[Lkd;'],
		'pop',

		'aload_1',
		['invokeinterface', 'xp', 'a', '()Lxv;', 1],
		['getfield', 'xv', 'a', '[D'],
		'iconst_0',
		'daload',
		['dstore', 6],

		'aload_1',
		['invokeinterface', 'xp', 'a', '()Lxv;', 1],
		['getfield', 'xv', 'b', '[D'],
		'iconst_0',
		'daload',
		['dstore', 8],

		['dload', 6],
		['dload', 8],
		['invokestatic', 'jh', 'a', '(DD)I'],
		'ireturn'
	])
	a_code = a_code_assemble([
		(6).to_bytes(2),
		(10).to_bytes(2),
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

def _create_get_dropped_item_id_method(cf, cp_cache, _):
	m = create_method(cf, cp_cache, ['public'], 'a', '(ILjava/util/Random;)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'iconst_0', 'ireturn'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
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

def _create_after_break_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lfd;Lgs;IIII)V', '(Ldj;Lem;IIII)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1', ['getfield', ('fd', 'dj'), 'B', 'Z'], ['ifne', 'L1'],

		'aload_2',
		['invokevirtual', ('gs', 'em'), 'G', ('()Liz;', '()Lfy;')],
		['ifnull', 'L1'],

		'aload_2',
		['invokevirtual', ('gs', 'em'), 'G', ('()Liz;', '()Lfy;')],
		['getfield', ('iz', 'fy'), 'c', 'I'],
		['getstatic', ('gm', 'ej'), 'bc', ('Lbl;', 'Las;')],
		['getfield', ('bl', 'as'), 'bf', 'I'],
		['if_icmpne', 'L1'],

		'aload_2',
		['getstatic', ('jl', 'gg'), 'C', ('[Lvr;', '[Lns;')],
		'aload_0',
		['getfield', c_name, 'bn', 'I'],
		'aaload',
		'iconst_1',
		['invokevirtual', ('gs', 'em'), 'a', ('(Lvr;I)V', '(Lns;I)V')],

		'aload_0',
		'aload_1',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['new', ('iz', 'fy')],
		'dup',
		['getstatic', ('uu', 'na'), 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'],
		['getfield', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'bn', 'I'],
		'iconst_1',
		['iload', 6],
		'iconst_3',
		'iand',
		['invokespecial', ('iz', 'fy'), '<init>', '(III)V'],
		['invokevirtual', c_name, 'a', ('(Lfd;IIILiz;)V', '(Ldj;IIILfy;)V')],
		['goto', 'L4'],

		['label', 'L1'],
		'aload_0',
		'aload_1',
		'aload_2',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokespecial', ('nr', 'in'), 'a', ('(Lfd;Lgs;IIII)V', '(Ldj;Lem;IIII)V')],

		['label', 'L4'],
		'return'
	])
	a_code = a_code_assemble([
		(11).to_bytes(2),
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

def _create_get_texture_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', '(II)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'iload_2', 'iconst_0', ['if_icmpne', 'L2'],
		'aload_0', ['getfield', c_name, 'useFancyGraphics', 'Z'], ['ifeq', 'ret_fast_graphics_oak'],
		['bipush', 52], 'ireturn',
		['label', 'ret_fast_graphics_oak'],
		['bipush', 53], 'ireturn',

		['label', 'L2'],
		'iload_2', 'iconst_1', ['if_icmpne', 'L3'],
		'aload_0', ['getfield', c_name, 'useFancyGraphics', 'Z'], ['ifeq', 'ret_fast_graphics_birch'],
		['bipush', 52], 'ireturn',
		['label', 'ret_fast_graphics_birch'],
		['bipush', 53], 'ireturn',

		['label', 'L3'],
		'iload_2', 'iconst_2', ['if_icmpne', 'L4'],
		'aload_0', ['getfield', c_name, 'useFancyGraphics', 'Z'], ['ifeq', 'ret_fast_graphics_spruce'],
		['sipush', 132], 'ireturn',
		['label', 'ret_fast_graphics_spruce'],
		['sipush', 133], 'ireturn',

		['label', 'L4'], 'iconst_0', 'ireturn'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
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
