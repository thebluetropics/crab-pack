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

	cf = class_file.load(mod.config.path("stage/client/ey.class"))
	cp = cf[0x04]

	cp.extend([
		[130, b"\x01", len("raw_squid").to_bytes(2), utf8.encode("raw_squid")],
		[131, b"\x0c", (130).to_bytes(2) + (94).to_bytes(2)],
		[132, b"\x09", (2).to_bytes(2) + (131).to_bytes(2)],
		[133, b"\x01", len("calamari").to_bytes(2), utf8.encode("calamari")],
		[134, b"\x0c", (133).to_bytes(2) + (94).to_bytes(2)],
		[135, b"\x09", (2).to_bytes(2) + (134).to_bytes(2)],
	])
	cf[0x03] = (int.from_bytes(cf[0x03]) + 6).to_bytes(2)

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "<init>") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:219] + instructions.make(219, [
		'aload_0',
		['getstatic', 132],
		['getfield', 18],
		['new', 3],
		'dup',
		['getstatic', 135],
		'iconst_1',
		'iconst_1',
		['invokespecial', 36],
		['invokevirtual', 34],
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

	with open(mod.config.path("stage/client/ey.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:ey.class → net.minecraft.recipe.SmeltingRecipeManager")
