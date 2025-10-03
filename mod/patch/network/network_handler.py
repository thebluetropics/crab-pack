import mod

from modmaker.a_code import (
	a_code_assemble,
	assemble_code
)
from modmaker.m import(
	create_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8
)

def apply(side_name):
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['ti', 'me'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0d].append(_create_on_hunger_update_method(cf, cp_cache, side))
	cf[0x0d].append(_create_on_thirst_update_method(cf, cp_cache, side))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.network.NetworkHandler')

def _create_on_hunger_update_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'return'
	])
	a_code = a_code_assemble([
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

def _create_on_thirst_update_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'onThirstUpdate', '(Lcom/thebluetropics/crabpack/ThirstUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'return'
	])
	a_code = a_code_assemble([
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
