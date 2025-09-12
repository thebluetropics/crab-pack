import mod

from mod.method import create_method
from mod.constant_pool import i2cpx_utf8
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)

def apply(side_name):
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['ti', 'me'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 2).to_bytes(2)
	cf[0x0d].append(_create_on_hunger_update_method(cf, cp_cache))
	cf[0x0d].append(_create_on_thirst_update_method(cf, cp_cache))

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.network.NetworkHandler')

def _create_on_hunger_update_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')

	code = instructions.assemble(0, [
		'return'
	])
	a_code = attribute.code.assemble([
		(0).to_bytes(2),
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

def _create_on_thirst_update_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onThirstUpdate', '(Lcom/thebluetropics/crabpack/ThirstUpdatePacket;)V')

	code = instructions.assemble(0, [
		'return'
	])
	a_code = attribute.code.assemble([
		(0).to_bytes(2),
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
