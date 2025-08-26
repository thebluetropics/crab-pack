import mod

from operator import eq
from mod.bytecode import (
	class_file,
	constant_pool,
	code_attribute
)

def apply_client():
	if not mod.config.is_feature_enabled("fixed_time"):
		return

	cf = class_file.load(mod.config.path("stage/client/fd.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 2).to_bytes(2)

	cp.append([1155, b"\x05", (6000).to_bytes(8)])

	# fd.l()V → tick
	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "l") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	code = bytearray(a_code[0x03])
	del code[184]
	code[184:184] = bytes().join([
		b"\x14" + (1155).to_bytes(2)
	])
	a_code[0x03] = bytes(code)
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

	with open(mod.config.path("stage/client/fd.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:fd.class → net.minecraft.world.World")

def apply_server():
	if not mod.config.is_feature_enabled("fixed_time"):
		return

	cf = class_file.load(mod.config.path("stage/server/dj.class")) # → net/minecraft/world/World
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 2).to_bytes(2)

	cp.append([1078, b"\x05", (6000).to_bytes(8)])

	# dj.h()V → tick
	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "h") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	code = bytearray(a_code[0x03])
	del code[184]
	code[184:184] = bytes().join([
		b"\x14" + (1078).to_bytes(2)
	])
	a_code[0x03] = bytes(code)
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

	with open(mod.config.path("stage/server/dj.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:dj.class → net.minecraft.world.World")
