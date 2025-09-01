import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_m,
	get_utf8_at,
	icpx_c
)

def apply_client():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/client/ki.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:552] + instructions.assemble(0, [
		['sipush', 201],
		'iconst_1',
		'iconst_1',
		['ldc_w', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket')],
		['invokestatic', icpx_m(cf, cp_cache, 'ki', 'a', '(IZZLjava/lang/Class;)V')]
	]) + a_code[0x03][552:567]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cf, cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open('stage/client/ki.class', 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:ki.class → net.minecraft.network.packet.Packet')

def apply_server():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/server/gt.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:541] + instructions.assemble(0, [
		['sipush', 201],
		'iconst_1',
		'iconst_1',
		['ldc_w', icpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket')],
		['invokestatic', icpx_m(cf, cp_cache, 'gt', 'a', '(IZZLjava/lang/Class;)V')]
	]) + a_code[0x03][541:566]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open('stage/server/gt.class', 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched server:gt.class → net.minecraft.network.packet.Packet')
