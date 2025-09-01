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
	get_utf8_at
)

def apply():
	if not mod.config.is_feature_enabled('debug_fov'):
		return

	cf = class_file.load(mod.config.path('stage/client/lr.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(IZ)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = instructions.assemble(0, [
		'iload_1',
		['bipush', 79],
		['if_icmpne*', 'a03'],

		'iload_2',
		['ifeq*', 'a03'],

		['getstatic', icpx_f(cf, cp_cache, 'px', 'useDebugFov', 'Z')],
		['iconst_1'],
		'ixor',
		['putstatic', icpx_f(cf, cp_cache, 'px', 'useDebugFov', 'Z')],
		'return',

		['jump_target*', 'a03']
	]) + a_code[0x03]

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

	with open(mod.config.path('stage/client/lr.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched client:lr.class → net.minecraft.client.input.KeyboardInput')
