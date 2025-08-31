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
	xcp = constant_pool.use_helper(cf)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].append(_on_hunger_update(xcp))

	with open('stage/client/nb.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched client:nb.class → net.minecraft.client.network.ClientNetworkHandler')

def _on_hunger_update(xcp):
	m = create_method(xcp, ['public'], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')

	code = instructions.assemble(0, [
		'aload_0',
		['getfield', icpx_f(xcp, 'nb', 'f', 'Lnet/minecraft/client/Minecraft;')],
		['getfield', icpx_f(xcp, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')],
		'aload_1',
		['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['putfield', icpx_f(xcp, 'dc', 'hunger', 'I')],

		'aload_0',
		['getfield', icpx_f(xcp, 'nb', 'f', 'Lnet/minecraft/client/Minecraft;')],
		['getfield', icpx_f(xcp, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')],
		'aload_1',
		['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['putfield', icpx_f(xcp, 'dc', 'maxHunger', 'I')],

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
	a = [i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
