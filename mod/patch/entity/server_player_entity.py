import mod

from mod.jvm import (
	class_file,
	attribute,
	instructions,
	constant_pool,
	create_method,
	icpx_c,
	icpx_f,
	icpx_utf8,
	icpx_m,
	i2cpx_utf8
)

def apply():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/server/dl.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].append(_create_update_hunger_method(xcp))

	with open('stage/server/dl.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:dl.class → net.minecraft.entity.ServerPlayerEntity')

def _create_update_hunger_method(xcp):
	m = create_method(xcp, ['protected'], 'updateHunger', '(II)V')

	code = instructions.assemble(0, [
		'aload_0',
		['getfield', icpx_f(xcp, 'dl', 'a', 'Lha;')],
		['new', icpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')],
		'dup',
		'iload_1',
		'iload_2',
		['invokespecial', icpx_m(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', '<init>', '(II)V')],
		['invokevirtual', icpx_m(xcp, 'ha', 'b', '(Lgt;)V')],
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
	a = [i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
