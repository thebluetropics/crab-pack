import mod

from operator import eq
from mod.bytecode import (
	class_file,
	constant_pool,
	code_attribute,
	instructions,
	utf8
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
