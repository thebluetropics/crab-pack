import mod

from operator import eq
from mod.bytecode import (
	class_file,
	constant_pool,
	code_attribute
)

def apply_client():
	if not mod.config.is_feature_enabled("stackable_food"):
		return

	cf = class_file.load(mod.config.path("stage/client/yw.class"))
	cp = cf[0x04]

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "<init>") and eq(desc, "(IIZ)V"):
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
	del code[16]
	code[16:16] = b"\x10" + b"\x10" # bipush 16
	a_code[0x03] = bytes(code)

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove LineNumberTable
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

	with open(mod.config.path("stage/client/yw.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:yw.class → net.minecraft.item.FoodItem")

def apply_server():
	if not mod.config.is_feature_enabled("stackable_food"):
		return

	cf = class_file.load(mod.config.path("stage/server/px.class"))
	cp = cf[0x04]

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "<init>") and eq(desc, "(IIZ)V"):
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
	del code[16]
	code[16:16] = b"\x10" + b"\x10" # bipush 16
	a_code[0x03] = bytes(code)

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove LineNumberTable
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

	with open(mod.config.path("stage/server/px.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:px.class → net.minecraft.item.FoodItem")
