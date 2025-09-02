import os, mod

from mod.field import create_field
from mod.method import create_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	i2cpx_c
)

def apply(side_name):
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/BottleItem'

	cf = class_file.create_new()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['gm', 'ej'][side])

	methods = [
		_create_constructor(cf, cp_cache, side, c_name),
		_create_use_method(cf, cp_cache, side, c_name)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = instructions.assemble(0, [
		'aload_0',
		'iload_1',
		['invokespecial', icpx_m(cf, cp_cache, ['gm', 'ej'][side], '<init>', '(I)V')],

		'aload_0',
		'iconst_1',
		['putfield', icpx_f(cf, cp_cache, c_name, 'bg', 'I')],

		'return'
	])
	a_code = attribute.code.assemble([
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

def _create_use_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])

	code = instructions.assemble(0, [
		'aload_3',
		'iconst_5',
		['invokevirtual', icpx_m(cf, cp_cache, ['gs', 'em'][side], 'restoreThirst', '(I)V')],

		'aload_1',
		'areturn'
	])
	a_code = attribute.code.assemble([
		(2).to_bytes(2),
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
