import mod

from operator import eq
from mod.bytecode import (
	class_file,
	constant_pool,
	code_attribute
)

def apply():
	if not mod.config.is_feature_enabled("minimal_title_screen"):
		return

	cf = class_file.load(mod.config.path("stage/client/fu.class"))
	cp = cf[0x04]

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "a") and eq(desc, "(IIF)V"):
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
	code = bytearray(a_code[0x03])
	del code[104:227]
	a_code[0x03] = bytes(code)

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

	with open(mod.config.path("stage/client/fu.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:fu.class → net.minecraft.client.gui.screen.TitleScreen")
