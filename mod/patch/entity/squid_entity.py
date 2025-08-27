import mod

from operator import eq
from mod.bytecode.fields import make_field
from mod.bytecode.method import get_method
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	utf8,
	constant_pool
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
	if not mod.config.is_feature_enabled("raw_squid_and_calamari"):
		return

	cf = class_file.load(mod.config.path("stage/client/xt.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 3).to_bytes(2)
	cp.extend([
		[206, b"\x01", len("raw_squid").to_bytes(2), utf8.encode("raw_squid")],
		[207, b"\x0c", (206).to_bytes(2) + (154).to_bytes(2)],
		[208, b"\x09", (19).to_bytes(2) + (207).to_bytes(2)]
	])

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "q") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:42] + instructions.make(42, [
		'aload_0',
		['new', 21],
		'dup',
		['getstatic', 208],
		'iconst_1',
		'iconst_0',
		['invokespecial', 73],
		'fconst_0',
		['invokevirtual', 78],
		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, _a in a_code[0x07]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if eq(name, "LineNumberTable"):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path("stage/client/xt.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:xt.class → net.minecraft.entity.SquidEntity")

def apply_server():
	if not mod.config.is_feature_enabled("raw_squid_and_calamari"):
		return

	cf = class_file.load(mod.config.path("stage/server/pf.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 3).to_bytes(2)
	cp.extend([
		[204, b"\x01", len("raw_squid").to_bytes(2), utf8.encode("raw_squid")],
		[205, b"\x0c", (204).to_bytes(2) + i2cp_utf8_get(cp, 'Lej;')],
		[206, b"\x09", i2cp_class_get(cp, 'ej') + (205).to_bytes(2)]
	])

	m = get_method(cf, cp, 'q', '()V')
	a = get_attribute(m[0x04], cp, 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:42] + instructions.make(42, [
		'aload_0',
		['new', icp_class_get(cp, 'fy')],
		'dup',
		['getstatic', 206],
		'iconst_1',
		'iconst_0',
		['invokespecial', icp_m_get(cp, 'fy', '<init>', '(Lej;II)V')],
		'fconst_0',
		['invokevirtual', icp_m_get(cp, 'pf', 'a', '(Lfy;F)Lez;')],
		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, _a in a_code[0x07]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if eq(name, "LineNumberTable"):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path("stage/server/pf.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:pf.class → net.minecraft.entity.SquidEntity")
