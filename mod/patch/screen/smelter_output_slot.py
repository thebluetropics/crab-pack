from modmaker import *
import os, mod

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/SmelterOutputSlot'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['gp', 'el'][side])

	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'player', ['Lgs;', 'Lem;'][side]))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_impl_can_insert_method(cf, cp_cache, side))
	cf[0x0d].append(_impl_on_take_item_method(cf, cp_cache, side, c_name))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:SmelterOutputSlot.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', ['(Lgs;Llw;III)V', '(Lem;Lhp;III)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'aload_2',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['invokespecial', ('gp', 'el'), '<init>', ('(Llw;III)V', '(Lhp;III)V')],

		'aload_0',
		'aload_1',
		['putfield', c_name, 'player', ('Lgs;', 'Lem;')],

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

def _impl_can_insert_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'b', ['(Liz;)Z', '(Lfy;)Z'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'iconst_0',
		'ireturn'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
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

def _impl_on_take_item_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Liz;)V', '(Lfy;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		'aload_0',
		['getfield', c_name, 'player', ('Lgs;', 'Lem;')],
		['getfield', ('gs', 'em'), ('aI', 'aL'), ('Lfd;', 'Ldj;')],
		'aload_0',
		['getfield', c_name, 'player', ('Lgs;', 'Lem;')],
		['invokevirtual', ('iz', 'fy'), 'b', ('(Lfd;Lgs;)V', '(Ldj;Lem;)V')],
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
