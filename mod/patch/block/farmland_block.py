import mod

from operator import eq
from mod.bytecode import (
	class_file,
	constant_pool,
	code_attribute,
	instructions
)

def apply_client():
	if not mod.config.is_feature_enabled("no_crop_trampling"):
		return

	cf = class_file.load(mod.config.path("stage/client/vl.class"))
	cp = cf[0x04]

	# vl.b(Lfd;IIILsn;)V → onSteppedOn
	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "b") and eq(desc, "(Lfd;IIILsn;)V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	# empties the method body to effectively disable farmland trampling
	a_code[0x03] = instructions.make(0, [
		"return"
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

	with open(mod.config.path("stage/client/vl.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:vl.class → net.minecraft.block.FarmlandBlock")

def apply_server():
	if not mod.config.is_feature_enabled("no_crop_trampling"):
		return

	cf = class_file.load(mod.config.path("stage/server/no.class"))
	cp = cf[0x04]

	# na.b(Ldj;IIILlq;)V → onSteppedOn
	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "b") and eq(desc, "(Ldj;IIILlq;)V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	# empties the method body to effectively disable farmland trampling
	a_code[0x02] = (1).to_bytes(4)
	a_code[0x03] = b"\xb1"

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

	with open(mod.config.path("stage/server/no.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:no.class → net.minecraft.block.FarmlandBlock")
