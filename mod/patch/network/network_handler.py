import mod

from mod.bytecode.fields import make_field
from mod.bytecode.method import (make_method, get_method)
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	constant_pool
)
from mod.bytecode.constant_pool import (
	icpx_utf8,
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	icpx_string
)

def apply_client():
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/client/ti.class"))
	xcp = constant_pool.use_helper(cf)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].append(_on_hunger_update_client(xcp))

	with open('stage/client/ti.class', 'wb') as file:
		file.write(class_file.make(cf))

	print('Patched client:ti.class → net.minecraft.network.NetworkHandler')

def _on_hunger_update_client(xcp):
	m = make_method(['public'], icpx_utf8(xcp, 'onHungerUpdate'), icpx_utf8(xcp, '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V'))

	code = instructions.make(0, [
		'return'
	])
	a_code = code_attribute.assemble([
		(0).to_bytes(2),
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

def apply_server():
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/server/me.class"))
	xcp = constant_pool.use_helper(cf)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].append(_on_hunger_update_client(xcp))

	with open('stage/server/me.class', 'wb') as file:
		file.write(class_file.make(cf))

	print('Patched server:me.class → net.minecraft.network.NetworkHandler')

def _on_hunger_update_client(xcp):
	m = make_method(['public'], icpx_utf8(xcp, 'onHungerUpdate'), icpx_utf8(xcp, '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V'))

	code = instructions.make(0, [
		'return'
	])
	a_code = code_attribute.assemble([
		(0).to_bytes(2),
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
