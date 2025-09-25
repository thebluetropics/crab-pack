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

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/PersistentLeavesBlock'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['nr', 'in'][side])

	methods = [
		_create_constructor(cf, cp_cache, side),
		_create_is_opaque_method(cf, cp_cache, side, c_name)
	]

	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:PersistentLeavesBlock.class')

def _create_constructor(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'iload_1',
		['bipush', 52],
		['getstatic', ('ln', 'hj'), 'i', ('Lln;', 'Lhj;')],
		'iconst_0',
		['invokespecial', ('nr', 'in'), '<init>', ('(IILln;Z)V', '(IILhj;Z)V')],
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
