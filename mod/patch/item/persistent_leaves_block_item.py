from modmaker import *
import os, mod

def apply(side_name):
	if not mod.config.is_feature_enabled('block.persistent_leaves'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/PersistentLeavesBlockItem'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['ck', 'bk'][side])

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_get_placement_metadata_method(cf, cp_cache, side))

	if side_name.__eq__('client'):
		cf[0x0d].append(_create_get_texture_id(cf, cp_cache))
		cf[0x0d].append(_create_get_color_multiplier(cf, cp_cache))

	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:PersistentLeavesBlockItem.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0', 'iload_1', ['invokespecial', ('ck', 'bk'), '<init>', '(I)V'],
		'aload_0', 'iconst_0', ['invokespecial', c_name, ('e', 'd'), ('(I)Lgm;', '(I)Lej;')],
		'aload_0', 'iconst_1', ['invokespecial', c_name, 'a', ('(Z)Lgm;', '(Z)Lej;')],
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

def _create_get_placement_metadata_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], ['b', 'a'][side], '(I)I')

	code = assemble_code(cf, cp_cache, side, 0, [
		'iload_1', 'iconst_3', 'iand', 'ireturn'
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

def _create_get_texture_id(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(I)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		['getstatic', 'uu', 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'],
		'iconst_0',
		'iload_1',
		['invokevirtual', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'a', '(II)I'],
		'ireturn'
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

def _create_get_color_multiplier(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'f', '(I)I')

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
