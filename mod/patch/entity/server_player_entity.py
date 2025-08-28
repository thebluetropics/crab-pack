import mod

from mod.bytecode.method import (make_method)
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	constant_pool
)
from mod.bytecode.constant_pool import (
	icpx_utf8,
	i2cpx_utf8
)

def apply():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/server/dl.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].append(_make_update_hunger_method(xcp))

	with open('stage/server/dl.class', 'wb') as file:
		file.write(class_file.make(cf))

	print('Patched server:dl.class → net.minecraft.entity.ServerPlayerEntity')

def _make_update_hunger_method(xcp):
	m = make_method(['protected'], icpx_utf8(xcp, 'updateHunger'), icpx_utf8(xcp, '()V'))

	code = instructions.make(0, [
		'return'
	])
	a_code = code_attribute.assemble([
		(0).to_bytes(2),
		(1).to_bytes(2),
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
