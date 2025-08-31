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
	icpx_c,
	icpx_f,
	icpx_m,
	icpx_string,
	get_utf8_at
)

def apply_client():
	if not mod.config.is_feature_enabled('fortress_bricks'):
		return

	cf = class_file.load(mod.config.path('stage/client/uu.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(xcp, ['public', 'static'], 'fortress_bricks', 'Luu;'))

	m = get_method(cf, xcp, '<clinit>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:3398] + instructions.assemble(3398, [
		['new', icpx_c(xcp, 'uu')],
		'dup',
		['bipush', 97],
		['sipush', 166],
		['getstatic', icpx_f(xcp, 'ln', 'e', 'Lln;')],
		['invokespecial', icpx_m(xcp, 'uu', '<init>', '(IILln;)V')],
		'fconst_2',
		['invokevirtual', icpx_m(xcp, 'uu', 'c', '(F)Luu;')],
		['ldc', 22],
		['invokevirtual', icpx_m(xcp, 'uu', 'b', '(F)Luu;')],
		['getstatic', icpx_f(xcp, 'uu', 'h', 'Lct;')],
		['invokevirtual', icpx_m(xcp, 'uu', 'a', '(Lct;)Luu;')],
		['ldc_w', icpx_string(xcp, 'fortress_bricks')],
		['invokevirtual', icpx_m(xcp, 'uu', 'a', '(Ljava/lang/String;)Luu;')],
		['putstatic', icpx_f(xcp, 'uu', 'fortress_bricks', 'Luu;')]
	]) + a_code[0x03][3398:3678]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/uu.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched client:uu.class → net.minecraft.block.Block')

def apply_server():
	if not mod.config.is_feature_enabled('fortress_bricks'):
		return

	cf = class_file.load(mod.config.path('stage/server/na.class'))
	xcp = constant_pool.use_helper(cf)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(xcp, ['public', 'static'], 'fortress_bricks', 'Lna;'))

	m = get_method(cf, xcp, '<clinit>', '()V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:3398] + instructions.assemble(3398, [
		['new', icpx_c(xcp, 'na')],
		'dup',
		['bipush', 97],
		['sipush', 166],
		['getstatic', icpx_f(xcp, 'hj', 'e', 'Lhj;')],
		['invokespecial', icpx_m(xcp, 'na', '<init>', '(IILhj;)V')],
		'fconst_2',
		['invokevirtual', icpx_m(xcp, 'na', 'c', '(F)Lna;')],
		['ldc', 21],
		['invokevirtual', icpx_m(xcp, 'na', 'b', '(F)Lna;')],
		['getstatic', icpx_f(xcp, 'na', 'h', 'Lbu;')],
		['invokevirtual', icpx_m(xcp, 'na', 'a', '(Lbu;)Lna;')],
		['ldc_w', icpx_string(xcp, 'fortress_bricks')],
		['invokevirtual', icpx_m(xcp, 'na', 'a', '(Ljava/lang/String;)Lna;')],
		['putstatic', icpx_f(xcp, 'na', 'fortress_bricks', 'Lna;')]
	]) + a_code[0x03][3398:3678]
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

	with open(mod.config.path('stage/server/na.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:na.class → net.minecraft.block.Block')
