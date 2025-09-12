import mod

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
	icpx_c
)

def apply():
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/server/dl.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 2).to_bytes(2)
	cf[0x0d].append(_create_update_hunger_method(cf, cp_cache))
	cf[0x0d].append(_create_update_thirst_method(cf, cp_cache))

	with open('stage/server/dl.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:dl.class → net.minecraft.entity.ServerPlayerEntity')

def _create_update_hunger_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['protected'], 'updateHunger', '(II)V')

	code = instructions.assemble(0, [
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'dl', 'a', 'Lha;')],
		['new', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket')],
		'dup',
		'iload_1',
		'iload_2',
		['invokespecial', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', '<init>', '(II)V')],
		['invokevirtual', icpx_m(cf, cp_cache, 'ha', 'b', '(Lgt;)V')],
		'return'
	])
	a_code = attribute.code.assemble([
		(5).to_bytes(2),
		(3).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _create_update_thirst_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['protected'], 'updateThirst', '(II)V')

	code = instructions.assemble(0, [
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'dl', 'a', 'Lha;')],
		['new', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/ThirstUpdatePacket')],
		'dup',
		'iload_1',
		'iload_2',
		['invokespecial', icpx_m(cf, cp_cache, 'com/thebluetropics/crabpack/ThirstUpdatePacket', '<init>', '(II)V')],
		['invokevirtual', icpx_m(cf, cp_cache, 'ha', 'b', '(Lgt;)V')],
		'return'
	])
	a_code = attribute.code.assemble([
		(5).to_bytes(2),
		(3).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
