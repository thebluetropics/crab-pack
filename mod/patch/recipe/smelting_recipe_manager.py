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
	icpx_c
)

def apply_client():
	if not mod.config.is_feature_enabled('raw_squid_and_calamari'):
		return

	cf = class_file.load(mod.config.path('stage/client/ey.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, '<init>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:219] + instructions.assemble(219, [
		'aload_0',
		['getstatic', icpx_f(xcp, 'gm', 'raw_squid', 'Lgm;')],
		['getfield', icpx_f(xcp, 'gm', 'bf', 'I')],
		['new', icpx_c(xcp, 'iz')],
		'dup',
		['getstatic', icpx_f(xcp, 'gm', 'calamari', 'Lgm;')],
		'iconst_1',
		'iconst_1',
		['invokespecial', icpx_m(xcp, 'iz', '<init>', '(Lgm;II)V')],
		['invokevirtual', icpx_m(xcp, 'ey', 'a', '(ILiz;)V')],
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

	with open(mod.config.path('stage/client/ey.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:ey.class → net.minecraft.recipe.SmeltingRecipeManager')

def apply_server():
	if not mod.config.is_feature_enabled('raw_squid_and_calamari'):
		return

	cf = class_file.load(mod.config.path('stage/server/de.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, '<init>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:219] + instructions.assemble(219, [
		'aload_0',
		['getstatic', icpx_f(xcp, 'ej', 'raw_squid', 'Lej;')],
		['getfield', icpx_f(xcp, 'ej', 'bf', 'I')],
		['new', icpx_c(xcp, 'fy')],
		'dup',
		['getstatic', icpx_f(xcp, 'ej', 'calamari', 'Lej;')],
		'iconst_1',
		'iconst_1',
		['invokespecial', icpx_m(xcp, 'fy', '<init>', '(Lej;II)V')],
		['invokevirtual', icpx_m(xcp, 'de', 'a', '(ILfy;)V')],
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

	with open(mod.config.path('stage/server/de.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched server:de.class → net.minecraft.recipe.SmeltingRecipeManager')
