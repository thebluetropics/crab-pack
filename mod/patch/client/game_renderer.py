import mod

from mod.attribute import get_attribute
from mod.field import create_field
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
	if not mod.config.is_feature_enabled('debug.debug_fov'):
		return

	cf = class_file.load(mod.config.path('stage/client/px.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x03] = (int.from_bytes(cf[0x03]) + 3).to_bytes(2)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'useDebugFov', 'Z'))

	_modify_static_initializer(cf, cp_cache)

	m = get_method(cf, cp_cache, 'd', '(F)F') # → getFov
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	# modify code
	a_code[0x03] = a_code[0x03][0:57] + instructions.assemble(57, [
		['getstatic', icpx_f(cf, cp_cache, 'px', 'useDebugFov', 'Z')],
		['ifeq*', 'a'],
		['bipush', 30],
		'i2f',
		'freturn',
		['jump_target*', 'a']
	]) + a_code[0x03][57:76]

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

	with open(mod.config.path('stage/client/px.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:px.class → net.minecraft.client.render.GameRenderer')

def _modify_static_initializer(cf, cp_cache):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	# load code attribute
	a_code = attribute.code.load(a[0x02])

	# modify code
	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(0, [
		'iconst_0', ['putstatic', 901],
		'return'
	])

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
