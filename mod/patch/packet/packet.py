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
	icpx_string,
	icpx_c,
)

def apply_client():
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/client/ki.class"))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, cf[0x04], '<clinit>', '()V')
	a = get_attribute(m[0x04], cf[0x04], 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:552] + instructions.make(0, [
		['sipush', 201],
		'iconst_1',
		'iconst_1',
		['ldc_w', icpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')],
		['invokestatic', icpx_m(xcp, 'ki', 'a', '(IZZLjava/lang/Class;)V')]
	]) + a_code[0x03][552:567]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if constant_pool.get_utf8(cf[0x04], int.from_bytes(a[0x00])).__eq__("LineNumberTable"):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open("stage/client/ki.class", "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:ki.class → net.minecraft.network.packet.Packet")

def apply_server():
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/server/gt.class"))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, cf[0x04], '<clinit>', '()V')
	a = get_attribute(m[0x04], cf[0x04], 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:541] + instructions.make(0, [
		['sipush', 201],
		'iconst_1',
		'iconst_1',
		['ldc_w', icpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')],
		['invokestatic', icpx_m(xcp, 'gt', 'a', '(IZZLjava/lang/Class;)V')]
	]) + a_code[0x03][541:566]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if constant_pool.get_utf8(cf[0x04], int.from_bytes(a[0x00])).__eq__("LineNumberTable"):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open("stage/server/gt.class", "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:gt.class → net.minecraft.network.packet.Packet")
