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
	icpx_m,
	get_utf8_at,
	icpx_string,
	icpx_c
)

def apply_client():
	if not mod.config.is_feature_enabled('raw_squid_and_calamari'):
		return

	cf = class_file.load(mod.config.path('stage/client/gm.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 2).to_bytes(2)
	cf[0x0b].extend([
		create_field(xcp, ['public', 'static'], 'raw_squid', 'Lgm;'),
		create_field(xcp, ['public', 'static'], 'calamari', 'Lgm;')
	])

	m = get_method(cf, xcp, '<clinit>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:2664] + instructions.assemble(2664, [
		['new', icpx_c(xcp, 'yw')],
		'dup',
		['sipush', 1024],
		'iconst_1',
		'iconst_0',
		['invokespecial', icpx_m(xcp, 'yw', '<init>', '(IIZ)V')],
		'iconst_2',
		['bipush', 15],
		['invokevirtual', icpx_m(xcp, 'yw', 'a', '(II)Lgm;')],
		['ldc_w', icpx_string(xcp, 'raw_squid')],
		['invokevirtual', icpx_m(xcp, 'gm', 'a', '(Ljava/lang/String;)Lgm;')],
		['putstatic', icpx_f(xcp, 'gm', 'raw_squid', 'Lgm;')],

		['new', icpx_c(xcp, 'yw')],
		'dup',
		['sipush', 1025],
		'iconst_5',
		'iconst_0',
		['invokespecial', icpx_m(xcp, 'yw', '<init>', '(IIZ)V')],
		'iconst_3',
		['bipush', 15],
		['invokevirtual', icpx_m(xcp, 'yw', 'a', '(II)Lgm;')],
		['ldc_w', icpx_string(xcp, 'raw_squid')],
		['invokevirtual', icpx_m(xcp, 'gm', 'a', '(Ljava/lang/String;)Lgm;')],
		['putstatic', icpx_f(xcp, 'gm', 'calamari', 'Lgm;')]
	]) + a_code[0x03][2664:2668]

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

	with open(mod.config.path('stage/client/gm.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:gm.class → net.minecraft.item.Item')

def apply_server():
	if not mod.config.is_feature_enabled('raw_squid_and_calamari'):
		return

	cf = class_file.load(mod.config.path('stage/server/ej.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 2).to_bytes(2)
	cf[0x0b].extend([
		create_field(xcp, ['public', 'static'], 'raw_squid', 'Lej;'),
		create_field(xcp, ['public', 'static'], 'calamari', 'Lej;')
	])

	m = get_method(cf, xcp, '<clinit>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:2664] + instructions.assemble(2664, [
		['new', icpx_c(xcp, 'px')],
		'dup',
		['sipush', 1024],
		'iconst_1',
		'iconst_0',
		['invokespecial', icpx_m(xcp, 'px', '<init>', '(IIZ)V')],
		'iconst_2',
		['bipush', 15],
		['invokevirtual', icpx_m(xcp, 'px', 'a', '(II)Lej;')],
		['ldc_w', icpx_string(xcp, 'calamari')],
		['invokevirtual', icpx_m(xcp, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
		['putstatic', icpx_f(xcp, 'ej', 'raw_squid', 'Lej;')],

		['new', icpx_c(xcp, 'px')],
		'dup',
		['sipush', 1025],
		'iconst_5',
		'iconst_0',
		['invokespecial', icpx_m(xcp, 'px', '<init>', '(IIZ)V')],
		'iconst_3',
		['bipush', 15],
		['invokevirtual', icpx_m(xcp, 'px', 'a', '(II)Lej;')],
		['ldc_w', icpx_string(xcp, 'calamari')],
		['invokevirtual', icpx_m(xcp, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
		['putstatic', icpx_f(xcp, 'ej', 'calamari', 'Lej;')]
	]) + a_code[0x03][2664:2668]

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

	with open(mod.config.path('stage/server/ej.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:ej.class → net.minecraft.item.Item')
