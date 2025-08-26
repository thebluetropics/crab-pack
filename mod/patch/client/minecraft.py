import mod

from operator import eq
from mod.bytecode import (
	class_file,
	constant_pool,
	code_attribute,
	instructions,
	utf8
)

def apply():
	if not mod.config.is_feature_enabled("log_version"):
		return

	cf = class_file.load(mod.config.path("stage/client/net/minecraft/client/Minecraft.class"))
	cp = cf[0x04]

	# push new constant pool entries
	cp.append([1552, b"\x01", len(f"Crab Pack {mod.version}").to_bytes(2), utf8.encode(f"Crab Pack {mod.version}")])
	cp.append([1553, b"\x08", (1552).to_bytes(2)])

	# update constant pool count
	cf[0x03] = (int.from_bytes(cf[0x03]) + 2).to_bytes(2)

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "a") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	# modify code
	a_code[0x03] = instructions.make(0, [
		['getstatic', 245],
		['ldc_w', 1553],
		['invokevirtual', 457]
	]) + a_code[0x03]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# update exception table
	for entry in a_code[0x05]:
		entry[0x00] = (int.from_bytes(entry[0x00]) + 9).to_bytes(2)
		entry[0x01] = (int.from_bytes(entry[0x01]) + 9).to_bytes(2)
		entry[0x02] = (int.from_bytes(entry[0x02]) + 9).to_bytes(2)

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

	with open(mod.config.path("stage/client/net/minecraft/client/Minecraft.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched net.minecraft.client.Minecraft")
