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
	icpx_f,
	icpx_m,
	get_utf8_at,
	icpx_string
)

def apply():
	if not mod.config.is_feature_enabled('log_version'):
		return

	cf = class_file.load(mod.config.path('stage/client/net/minecraft/client/Minecraft.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, 'a', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	# modify code
	a_code[0x03] = instructions.assemble(0, [
		['getstatic', icpx_f(xcp, 'java/lang/System', 'out', 'Ljava/io/PrintStream;')],
		['ldc_w', icpx_string(xcp, f'Crab Pack {mod.version}')],
		['invokevirtual', icpx_m(xcp, 'java/io/PrintStream', 'println', '(Ljava/lang/String;)V')]
	]) + a_code[0x03]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# update exception table
	for entry in a_code[0x05]:
		entry[0x00] = (int.from_bytes(entry[0x00]) + 9).to_bytes(2)
		entry[0x01] = (int.from_bytes(entry[0x01]) + 9).to_bytes(2)
		entry[0x02] = (int.from_bytes(entry[0x02]) + 9).to_bytes(2)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/net/minecraft/client/Minecraft.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched net.minecraft.client.Minecraft')
