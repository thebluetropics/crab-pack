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

	cf = class_file.load(mod.config.path("stage/client/gm.class"))
	cp = cf[0x04]

	cp.extend([
		[845, b"\x01", len("raw_squid").to_bytes(2), utf8.encode("raw_squid")],
		[846, b"\x0c", (845).to_bytes(2) + (578).to_bytes(2)],
		[847, b"\x09", (121).to_bytes(2) + (846).to_bytes(2)],
		[848, b"\x08", (845).to_bytes(2)],

		[849, b"\x01", len("calamari").to_bytes(2), utf8.encode("calamari")],
		[850, b"\x0c", (849).to_bytes(2) + (578).to_bytes(2)],
		[851, b"\x09", (121).to_bytes(2) + (850).to_bytes(2)],
		[852, b"\x08", (849).to_bytes(2)],
	])
	cf[0x03] = (int.from_bytes(cf[0x03]) + 8).to_bytes(2)

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 2).to_bytes(2)
	cf[0x0b].append([
		(0x0001.__or__(0x0008)).to_bytes(2),
		(845).to_bytes(2),
		(578).to_bytes(2),
		(0).to_bytes(2),
		[]
	])
	cf[0x0b].append([
		(0x0001.__or__(0x0008)).to_bytes(2),
		(849).to_bytes(2),
		(578).to_bytes(2),
		(0).to_bytes(2),
		[]
	])

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "<clinit>") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:2664] + instructions.make(2664, [
		['new', 155],
		'dup',
		['sipush', 1024],
		'iconst_1',
		'iconst_0',
		['invokespecial', 364],
		'iconst_2',
		['bipush', 15],
		['invokevirtual', 365],
		['ldc_w', 848],
		['invokevirtual', 305],
		['putstatic', 847],

		['new', 155],
		'dup',
		['sipush', 1025],
		'iconst_5',
		'iconst_0',
		['invokespecial', 364],
		'iconst_3',
		['bipush', 15],
		['invokevirtual', 365],
		['ldc_w', 852],
		['invokevirtual', 305],
		['putstatic', 851]
	]) + a_code[0x03][2664:2668]

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

	with open(mod.config.path("stage/client/gm.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:gm.class → net.minecraft.item.Item")

def apply_server():
	if not mod.config.is_feature_enabled('raw_squid_and_calamari'):
		return

	cf = class_file.load(mod.config.path('stage/server/ej.class'))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 8).to_bytes(2)
	cp.extend([
		[834, b"\x01", len('raw_squid').to_bytes(2), utf8.encode('raw_squid')],
		[835, b"\x0c", (834).to_bytes(2) + i2cp_utf8_get(cp, 'Lej;')],
		[836, b"\x09", i2cp_class_get(cp, 'ej') + (835).to_bytes(2)],
		[837, b"\x08", (834).to_bytes(2)],
		[838, b"\x01", len('calamari').to_bytes(2), utf8.encode('calamari')],
		[839, b"\x0c", (838).to_bytes(2) + i2cp_utf8_get(cp, 'Lej;')],
		[840, b"\x09", i2cp_class_get(cp, 'ej') + (839).to_bytes(2)],
		[841, b"\x08", (838).to_bytes(2)],
	])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 2).to_bytes(2)
	cf[0x0b].append(make_field(['public', 'static'], 834, icp_utf8_get(cp, 'Lej;')))
	cf[0x0b].append(make_field(['public', 'static'], 838, icp_utf8_get(cp, 'Lej;')))

	m = get_method(cf, cp, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp, 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:2664] + instructions.make(2664, [
		['new', icp_class_get(cp, 'px')],
		'dup',
		['sipush', 1024],
		'iconst_1',
		'iconst_0',
		['invokespecial', icp_m_get(cp, 'px', '<init>', '(IIZ)V')],
		'iconst_2',
		['bipush', 15],
		['invokevirtual', icp_m_get(cp, 'px', 'a', '(II)Lej;')],
		['ldc_w', 837],
		['invokevirtual', icp_m_get(cp, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
		['putstatic', 836],
		['new', icp_class_get(cp, 'px')],
		'dup',
		['sipush', 1025],
		'iconst_5',
		'iconst_0',
		['invokespecial', icp_m_get(cp, 'px', '<init>', '(IIZ)V')],
		'iconst_3',
		['bipush', 15],
		['invokevirtual', icp_m_get(cp, 'px', 'a', '(II)Lej;')],
		['ldc_w', 841],
		['invokevirtual', icp_m_get(cp, 'ej', 'a', '(Ljava/lang/String;)Lej;')],
		['putstatic', 840]
	]) + a_code[0x03][2664:2668]

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

	with open(mod.config.path("stage/server/ej.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:ej.class → net.minecraft.item.Item")
