import os, mod

from modmaker.a_code import (
	a_code_assemble,
	assemble_code
)
from modmaker.cf import (
	cf_assemble,
	cf_create
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8,
	i2cpx_c
)
from modmaker.m import (
	create_method
)
from modmaker.f import (
	create_field
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/SmelterBlockEntity'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['ow', 'jh'][side])

	cf[0x08] = (int.from_bytes(cf[0x08]) + 1).to_bytes(2)
	cf[0x09].append(i2cpx_c(cf, cp_cache, ['lw', 'hp'][side]))

	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'inventory', ['[Liz;', '[Lfy;'][side]))
	cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'burnTime', 'I'))
	cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'fuelTime', 'I'))
	cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'cookTime', 'I'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_impl_get_name_method(cf, cp_cache, side))
	cf[0x0d].append(_impl_size_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_impl_get_max_count_per_stack_method(cf, cp_cache, side))
	cf[0x0d].append(_impl_get_stack_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_impl_can_player_use_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_impl_set_stack_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_impl_remove_stack_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_read_nbt_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_write_nbt_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_is_burning_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_get_fuel_time_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_can_accept_recipe_output_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_craft_recipe_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_tick_method(cf, cp_cache, side, c_name))

	if side_name.__eq__('client'):
		cf[0x0d].append(_create_get_cook_time_delta_method(cf, cp_cache, c_name))
		cf[0x0d].append(_create_get_fuel_time_delta_method(cf, cp_cache, c_name))

	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:SmelterBlockEntity.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['invokespecial', ('ow', 'jh'), '<init>', '()V'],
		'aload_0', 'iconst_4', ['anewarray', ('iz', 'fy')], ['putfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
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

def _impl_get_name_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'c', '()Ljava/lang/String;')

	code = assemble_code(cf, cp_cache, side, 0, [
		['ldc.string', 'Smelter'],
		'areturn'
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

def _impl_size_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', '()I')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'arraylength',
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

def _impl_get_stack_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], ['f_', 'd_'][side], ['(I)Liz;', '(I)Lfy;'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aaload',
		'areturn'
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

def _impl_remove_stack_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(II)Liz;', '(II)Lfy;'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aaload',
		['ifnull', 'L1'],

		['label', 'L2'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iload_2',
		['if_icmpgt', 'L3'],

		['label', 'L4'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aaload',
		['astore', 3],

		['label', 'L5'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aconst_null',
		'aastore',

		['label', 'L6'],
		'aload_3',
		'areturn',

		['label', 'L3'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aaload',
		'iload_2',
		['invokevirtual', ('iz', 'fy'), 'a', ('(I)Liz;', '(I)Lfy;')],
		['astore', 3],

		['label', 'L7'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['ifne', 'L8'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aconst_null',
		'aastore',

		['label', 'L8'],
		'aload_3',
		'areturn',

		['label', 'L1'],
		'aconst_null',
		'areturn'
	])
	a_code = a_code_assemble([
		(3).to_bytes(2),
		(4).to_bytes(2),
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

def _impl_set_stack_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(ILiz;)V', '(ILfy;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iload_1',
		'aload_2',
		'aastore',

		['label', 'L1'],
		'aload_2',
		['ifnull', 'L2'],
		'aload_2',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'aload_0',
		['invokevirtual', c_name, 'd', '()I'],
		['if_icmple', 'L2'],
		'aload_2',
		'aload_0',
		['invokevirtual', c_name, 'd', '()I'],
		['putfield', ('iz', 'fy'), 'a', 'I'],

		['label', 'L2'],
		'return'
	])
	a_code = a_code_assemble([
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

def _impl_get_max_count_per_stack_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'd', '()I')

	code = assemble_code(cf, cp_cache, side, 0, [
		['bipush', 64],
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

def _impl_can_player_use_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a_', ['(Lgs;)Z', '(Lem;)Z'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0', ['getfield', c_name, 'd', ('Lfd;', 'Ldj;')],
		'aload_0', ['getfield', c_name, 'e', 'I'],
		'aload_0', ['getfield', c_name, 'f', 'I'],
		'aload_0', ['getfield', c_name, 'g', 'I'],
		['invokevirtual', ('fd', 'dj'), 'b', ('(III)Low;', '(III)Ljh;')],
		'aload_0',
		['if_acmpeq', 'L1'],
		'iconst_0',
		'ireturn',

		['label', 'L1'],
		'aload_1',
		'aload_0',
		['getfield', c_name, 'e', 'I'],
		'i2d',
		['ldc2_w.f64', 0.5],
		'dadd',
		'aload_0',
		['getfield', c_name, 'f', 'I'],
		'i2d',
		['ldc2_w.f64', 0.5],
		'dadd',
		'aload_0',
		['getfield', c_name, 'g', 'I'],
		'i2d',
		['ldc2_w.f64', 0.5],
		'dadd',
		['invokevirtual', ('gs', 'em'), ('g', 'e'), '(DDD)D'],
		['ldc2_w.f64', 64.0],
		'dcmpl',
		['ifle', 'L2'],
		'iconst_0',
		'ireturn',

		['label', 'L2'],
		'iconst_1',
		'ireturn'
	])
	a_code = a_code_assemble([
		(9).to_bytes(2),
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

def _create_read_nbt_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lnu;)V', '(Liq;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'aload_1',
		['invokespecial', ('ow', 'jh'), 'a', ('(Lnu;)V', '(Liq;)V')],
		'aload_1',
		['ldc.string', 'Items'],
		['invokevirtual', ('nu', 'iq'), 'l', ('(Ljava/lang/String;)Lsp;', '(Ljava/lang/String;)Llr;')],
		['astore', 2],
		'aload_0',
		'aload_0',
		['invokevirtual', c_name, 'a', '()I'],
		['anewarray', ('iz', 'fy')],
		['putfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],

		'iconst_0',
		['istore', 3],

		['label', 'L4'],
		['iload', 3],
		['aload', 2],
		['invokevirtual', ('sp', 'lr'), 'c', '()I'],
		['if_icmpge', 'L5'],

		['aload', 2],
		['iload', 3],
		['invokevirtual', ('sp', 'lr'), 'a', ('(I)Lij;', '(I)Lfo;')],
		['checkcast', ('nu', 'iq')],
		['astore', 4],
		['aload', 4],
		['ldc.string', 'Slot'],
		['invokevirtual', ('nu', 'iq'), 'c', '(Ljava/lang/String;)B'],
		['istore', 5],
		['iload', 5],
		['iflt', 'L9'],
		['iload', 5],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'arraylength',
		['if_icmpge', 'L9'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		['iload', 5],
		['new', ('iz', 'fy')],
		'dup',
		['aload', 4],
		['invokespecial', ('iz', 'fy'), '<init>', ('(Lnu;)V', '(Liq;)V')],
		'aastore',
		['label', 'L9'],
		['iinc', 3, 1],
		['goto', 'L4'],
		['label', 'L5'],
		'aload_0',
		'aload_1',
		['ldc.string', 'BurnTime'],
		['invokevirtual', ('nu', 'iq'), 'd', '(Ljava/lang/String;)S'],
		['putfield', c_name, 'burnTime', 'I'],
		'aload_0',
		'aload_1',
		['ldc.string', 'CookTime'],
		['invokevirtual', ('nu', 'iq'), 'd', '(Ljava/lang/String;)S'],
		['putfield', c_name, 'cookTime', 'I'],
		'aload_0',
		'aload_0',
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_2',
		'aaload',
		['invokespecial', c_name, 'getFuelTime', ('(Liz;)I', '(Lfy;)I')],
		['putfield', c_name, 'fuelTime', 'I'],

		'return'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
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

def _create_write_nbt_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'b', ['(Lnu;)V', '(Liq;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'aload_1',
		['invokespecial', ('ow', 'jh'), 'b', ('(Lnu;)V', '(Liq;)V')],

		'aload_1',
		['ldc.string', 'BurnTime'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		'i2s',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;S)V'],

		'aload_1',
		['ldc.string', 'CookTime'],
		'aload_0',
		['getfield', c_name, 'cookTime', 'I'],
		'i2s',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;S)V'],

		['new', ('sp', 'lr')],
		'dup',
		['invokespecial', ('sp', 'lr'), '<init>', '()V'],
		['astore', 2],

		'iconst_0',
		['istore', 3],

		['label', 'L5'],
		['iload', 3],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'arraylength',
		['if_icmpge', 'L6'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		['iload', 3],
		'aaload',
		['ifnull', 'L8'],

		['new', ('nu', 'iq')],
		'dup',
		['invokespecial', ('nu', 'iq'), '<init>', '()V'],
		['astore', 4],

		['aload', 4],
		['ldc.string', 'Slot'],
		['iload', 3],
		'i2b',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;B)V'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		['iload', 3],
		'aaload',
		['aload', 4],
		['invokevirtual', ('iz', 'fy'), 'a', ('(Lnu;)Lnu;', '(Liq;)Liq;')],
		'pop',

		['aload', 2],
		['aload', 4],
		['invokevirtual', ('sp', 'lr'), 'a', ('(Lij;)V', '(Lfo;)V')],

		['label', 'L8'],
		['iinc', 3, 1],
		['goto', 'L5'],

		['label', 'L6'],
		'aload_1',
		['ldc.string', 'Items'],
		['aload', 2],
		['invokevirtual', ('nu', 'iq'), 'a', ('(Ljava/lang/String;Lij;)V', '(Ljava/lang/String;Lfo;)V')],

		'return'
	])
	a_code = a_code_assemble([
		(3).to_bytes(2),
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

def _create_get_cook_time_delta_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'getCookTimeDelta', '(I)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', c_name, 'cookTime', 'I'],
		'iload_1',
		'imul',
		['sipush', 200],
		'idiv',
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

def _create_get_fuel_time_delta_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'getFuelTimeDelta', '(I)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', c_name, 'fuelTime', 'I'],
		['ifne', 'L1'],

		'aload_0',
		['sipush', 200],
		['putfield', c_name, 'fuelTime', 'I'],

		['label', 'L1'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		'iload_1',
		'imul',
		'aload_0',
		['getfield', c_name, 'fuelTime', 'I'],
		'idiv',
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

def _create_is_burning_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'isBurning', '()Z')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifle', 'L1'],

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

def _create_get_fuel_time_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['private'], 'getFuelTime', ['(Liz;)I', '(Lfy;)I'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		['ifnonnull', 'L1'],
		'iconst_0',
		'ireturn',

		['label', 'L1'],
		'aload_1',
		['invokevirtual', ('iz', 'fy'), 'a', ('()Lgm;', '()Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],
		['istore', 2],

		['label', 'L2'],
		['iload', 2],
		['getstatic', ('gm', 'ej'), 'k', ('Lgm;', 'Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],
		['if_icmpne', 'L3'],
		['sipush', 1600],
		'ireturn',

		['label', 'L3'],
		'iconst_0',
		'ireturn'
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

def _create_can_accept_recipe_output_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['private'], 'canAcceptRecipeOutput', '()Z')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')], 'iconst_0', 'aaload',
		['ifnull', 'Lreturn_false'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_1',
		'aaload',
		['ifnull', 'Lreturn_false'],

		['goto', 'L1'],

		['label', 'Lreturn_false'],
		'iconst_0',
		'ireturn',

		['label', 'L1'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_0',
		'aaload',
		['invokevirtual', ('iz', 'fy'), 'a', ('()Lgm;', '()Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_1',
		'aaload',
		['invokevirtual', ('iz', 'fy'), 'a', ('()Lgm;', '()Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],

		['invokestatic', 'com/thebluetropics/crabpack/SmelterRecipeManager', 'craft', ('(II)Liz;', '(II)Lfy;')],
		'astore_1',

		'aload_1',
		['ifnonnull', 'L3'],
		'iconst_0',
		'ireturn',

		['label', 'L3'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['ifnonnull', 'L4'],
		'iconst_1',
		'ireturn',

		['label', 'L4'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['aload', 1],
		['invokevirtual',('iz', 'fy'), 'a', ('(Liz;)Z', '(Lfy;)Z')],
		['ifne', 'L5'],
		'iconst_0',
		'ireturn',

		['label', 'L5'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'aload_0',
		['invokevirtual', c_name, 'd', '()I'],
		['if_icmpge', 'L6'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['invokevirtual', ('iz', 'fy'), ('c', 'b'), '()I'],
		['if_icmpge', 'L6'],
		'iconst_1',
		'ireturn',

		['label', 'L6'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['aload', 1],
		['invokevirtual', ('iz', 'fy'), ('c', 'b'), '()I'],
		['if_icmpge', 'L7'],
		'iconst_1',
		'ireturn',

		['label', 'L7'],
		'iconst_0',
		'ireturn',
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

def _create_craft_recipe_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'craftRecipe', '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['invokespecial', c_name, 'canAcceptRecipeOutput', '()Z'],
		['ifne', 'L1'],
		'return',

		['label', 'L1'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_0',
		'aaload',
		['invokevirtual', ('iz', 'fy'), 'a', ('()Lgm;', '()Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_1',
		'aaload',
		['invokevirtual', ('iz', 'fy'), 'a', ('()Lgm;', '()Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],

		['invokestatic', 'com/thebluetropics/crabpack/SmelterRecipeManager', 'craft', ('(II)Liz;', '(II)Lfy;')],
		'astore_1',

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['ifnonnull', 'L3'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aload_1',
		['invokevirtual', ('iz', 'fy'), ('k', 'j'), ('()Liz;', '()Lfy;')],
		'aastore',
		['goto', 'L4'],

		['label', 'L3'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		['getfield', ('iz', 'fy'), 'c', 'I'],
		'aload_1',
		['getfield', ('iz', 'fy'), 'c', 'I'],
		['if_icmpne', 'L4'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_3',
		'aaload',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'iadd',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		['label', 'L4'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_0',
		'aaload',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_0',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['ifgt', 'L5'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_0',
		'aconst_null',
		'aastore',

		['label', 'L5'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_1',
		'aaload',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_1',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['ifgt', 'L6'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_1',
		'aconst_null',
		'aastore',

		['label', 'L6'],
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

def _create_tick_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], ['n_', 'g_'][side], '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifle', 'L1'],
		'iconst_1',
		['goto', 'L2'],
		['label', 'L1'],
		'iconst_0',
		['label', 'L2'],
		'istore_1',

		['label', 'L3'],
		'iconst_0',
		'istore_2',

		['label', 'L4'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifle', 'L5'],

		['label', 'L6'],
		'aload_0',
		'dup',
		['getfield', c_name, 'burnTime', 'I'],
		'iconst_1',
		'isub',
		['putfield', c_name, 'burnTime', 'I'],

		['label', 'L5'],
		'aload_0',
		['getfield', c_name, 'd', ('Lfd;', 'Ldj;')],
		['getfield', ('fd', 'dj'), 'B', 'Z'],
		['ifne', 'L7'],

		['label', 'L8'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifne', 'L9'],
		'aload_0',
		['invokespecial', c_name, 'canAcceptRecipeOutput', '()Z'],
		['ifeq', 'L9'],

		['label', 'L10'],
		'aload_0',
		'aload_0',
		'aload_0',
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_2',
		'aaload',
		['invokespecial', c_name, 'getFuelTime', ('(Liz;)I', '(Lfy;)I')],
		'dup_x1',
		['putfield', c_name, 'burnTime', 'I'],
		['putfield', c_name, 'fuelTime', 'I'],

		['label', 'L11'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifle', 'L9'],

		['label', 'L12'],
		'iconst_1',
		'istore_2',

		['label', 'L13'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_2',
		'aaload',
		['ifnull', 'L9'],

		['label', 'L14'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_2',
		'aaload',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		['label', 'L15'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_2',
		'aaload',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['ifne', 'L9'],
		'aload_0',
		['getfield', c_name, 'inventory', ('[Liz;', '[Lfy;')],
		'iconst_2',
		'aconst_null',
		'aastore',

		['label', 'L9'],
		'aload_0',
		['invokevirtual', c_name, 'isBurning', '()Z'],
		['ifeq', 'L16'],
		'aload_0',
		['invokespecial', c_name, 'canAcceptRecipeOutput', '()Z'],
		['ifeq', 'L16'],

		['label', 'L17'],
		'aload_0',
		'dup',
		['getfield', c_name, 'cookTime', 'I'],
		'iconst_1',
		'iadd',
		['putfield', c_name, 'cookTime', 'I'],

		['label', 'L18'],
		'aload_0',
		['getfield', c_name, 'cookTime', 'I'],
		['sipush', 200],
		['if_icmpne', 'L19'],

		['label', 'L20'],
		'aload_0',
		'iconst_0',
		['putfield', c_name, 'cookTime', 'I'],

		'aload_0',
		['invokevirtual', c_name, 'craftRecipe', '()V'],
		'iconst_1',
		'istore_2',
		['goto', 'L19'],

		['label', 'L16'],
		'aload_0',
		'iconst_0',
		['putfield', c_name, 'cookTime', 'I'],

		['label', 'L19'],
		'iload_1',
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifle', 'L23'],
		'iconst_1',
		['goto', 'L24'],

		['label', 'L23'],
		'iconst_0',

		['label', 'L24'],
		['if_icmpeq', 'L7'],

		['label', 'L25'],
		'iconst_1',
		'istore_2',

		['label', 'L26'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		['ifle', 'L27'],
		'iconst_1',
		['goto', 'L28'],

		['label', 'L27'],
		'iconst_0',

		['label', 'L28'],
		'aload_0',
		['getfield', c_name, 'd', ('Lfd;', 'Ldj;')],
		'aload_0',
		['getfield', c_name, 'e', 'I'],
		'aload_0',
		['getfield', c_name, 'f', 'I'],
		'aload_0',
		['getfield', c_name, 'g', 'I'],
		['invokestatic', 'com/thebluetropics/crabpack/SmelterBlock', 'updateLitState', ('(ZLfd;III)V', '(ZLdj;III)V')],

		['label', 'L7'],
		'iload_2',
		['ifeq', 'L29'],
		'aload_0',
		['invokevirtual', c_name, ('y_', 'i'), '()V'],

		['label', 'L29'],
		'return'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
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
