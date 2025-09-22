import mod

from modmaker.a_code import (
	a_code_assemble,
	assemble_code
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8
)
from modmaker.m import (
	create_method
)

def apply():
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	cf = load_class_file(mod.config.path('stage/client/nb.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 2).to_bytes(2)
	cf[0x0d].append(_on_hunger_update(cf, cp_cache))
	cf[0x0d].append(_on_thirst_update(cf, cp_cache))

	with open('stage/client/nb.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:nb.class → net.minecraft.client.network.ClientNetworkHandler')

def _on_hunger_update(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I'],
		['putfield', 'dc', 'hunger', 'I'],

		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I'],
		['putfield', 'dc', 'maxHunger', 'I'],

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
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _on_thirst_update(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onThirstUpdate', '(Lcom/thebluetropics/crabpack/ThirstUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/ThirstUpdatePacket', 'thirst', 'I'],
		['putfield', 'dc', 'thirst', 'I'],

		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/ThirstUpdatePacket', 'maxThirst', 'I'],
		['putfield', 'dc', 'maxThirst', 'I'],

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
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
