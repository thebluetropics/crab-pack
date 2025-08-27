import mod

from mod.bytecode.fields import make_field
from mod.bytecode.method import get_method
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	utf8
)
from mod.bytecode.constant_pool import (
	vcp_utf8_get,
	i2cp_utf8_get,
	icp_utf8_get,
	i2cp_class_get,
	icp_class_get,
	icp_f_get,
	icp_m_get
)

def apply_client():
	if not mod.config.is_feature_enabled('fortress_bricks'):
		return

	cf = class_file.load(mod.config.path('stage/client/uu.class'))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 4).to_bytes(2)
	cp.extend([
		[1211, b"\x01", len('fortress_bricks').to_bytes(2), utf8.encode('fortress_bricks')],
		[1212, b"\x0c", (1211).to_bytes(2) + i2cp_utf8_get(cp, 'Luu;')],
		[1213, b"\x09", i2cp_class_get(cp, 'uu') + (1212).to_bytes(2)],
		[1214, b"\x08", (1211).to_bytes(2)]
	])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(make_field(['public', 'static'], 1211, icp_utf8_get(cp, 'Luu;')))

	m = get_method(cf, cp, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp, 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:3398] + instructions.make(3398, [
		['new', icp_class_get(cp, 'uu')],
		'dup',
		['bipush', 97],
		['sipush', 166],
		['getstatic', icp_f_get(cp, 'ln', 'e', 'Lln;')],
		['invokespecial', icp_m_get(cp, 'uu', '<init>', '(IILln;)V')],
		'fconst_2',
		['invokevirtual', icp_m_get(cp, 'uu', 'c', '(F)Luu;')],
		['ldc', 22],
		['invokevirtual', icp_m_get(cp, 'uu', 'b', '(F)Luu;')],
		['getstatic', icp_f_get(cp, 'uu', 'h', 'Lct;')],
		['invokevirtual', icp_m_get(cp, 'uu', 'a', '(Lct;)Luu;')],
		['ldc_w', 1214],
		['invokevirtual', icp_m_get(cp, 'uu', 'a', '(Ljava/lang/String;)Luu;')],
		['putstatic', 1213]
	]) + a_code[0x03][3398:3678]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if vcp_utf8_get(cp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/uu.class'), 'wb') as file:
		file.write(class_file.make(cf))

	print('Patched client:uu.class → net.minecraft.block.Block')
