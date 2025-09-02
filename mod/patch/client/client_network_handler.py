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
	i2cpx_utf8
)

def apply():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/client/nb.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 2).to_bytes(2)
	cf[0x0d].append(_on_hunger_update(cf, cp_cache))
	cf[0x0d].append(_on_thirst_update(cf, cp_cache))

	with open('stage/client/nb.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched client:nb.class → net.minecraft.client.network.ClientNetworkHandler')

def _on_hunger_update(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')

	code = instructions.assemble(0, [
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'nb', 'f', 'Lnet/minecraft/client/Minecraft;')],
		['getfield', icpx_f(cf, cp_cache, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')],
		'aload_1',
		['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['putfield', icpx_f(cf, cp_cache, 'dc', 'hunger', 'I')],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'nb', 'f', 'Lnet/minecraft/client/Minecraft;')],
		['getfield', icpx_f(cf, cp_cache, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')],
		'aload_1',
		['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['putfield', icpx_f(cf, cp_cache, 'dc', 'maxHunger', 'I')],

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
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _on_thirst_update(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onThirstUpdate', '(Lcom/thebluetropics/crabpack/ThirstUpdatePacket;)V')

	code = instructions.assemble(0, [
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'nb', 'f', 'Lnet/minecraft/client/Minecraft;')],
		['getfield', icpx_f(cf, cp_cache, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')],
		'aload_1',
		['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/ThirstUpdatePacket', 'thirst', 'I')],
		['putfield', icpx_f(cf, cp_cache, 'dc', 'thirst', 'I')],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'nb', 'f', 'Lnet/minecraft/client/Minecraft;')],
		['getfield', icpx_f(cf, cp_cache, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')],
		'aload_1',
		['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/ThirstUpdatePacket', 'maxThirst', 'I')],
		['putfield', icpx_f(cf, cp_cache, 'dc', 'maxThirst', 'I')],

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
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
