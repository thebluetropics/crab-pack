import mod

from mod.jvm import (
	class_file,
	attribute,
	instructions,
	constant_pool,
	create_field,
	get_method,
	get_attribute,
	icpx_f,
	get_utf8_at,
)

def apply():
	if not mod.config.is_feature_enabled('debug_fov'):
		return

	cf = class_file.load(mod.config.path('stage/client/px.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x03] = (int.from_bytes(cf[0x03]) + 3).to_bytes(2)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(xcp, ['public', 'static'], 'useDebugFov', 'Z'))

	_modify_static_initializer(cf, xcp)

	m = get_method(cf, xcp, 'd', '(F)F') # → getFov
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	# modify code
	a_code[0x03] = a_code[0x03][0:57] + instructions.assemble(57, [
		['getstatic', icpx_f(xcp, 'px', 'useDebugFov', 'Z')],
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
		if get_utf8_at(cf[0x04], int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/px.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:px.class → net.minecraft.client.render.GameRenderer')

def _modify_static_initializer(cf, xcp):
	m = get_method(cf, xcp, '<clinit>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

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
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
