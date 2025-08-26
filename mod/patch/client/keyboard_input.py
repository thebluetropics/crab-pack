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
	if not mod.config.is_feature_enabled("debug_fov"):
		return

	cf = class_file.load(mod.config.path("stage/client/lr.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 5).to_bytes(2)

	cp.extend((
		[65, b"\x01", len("px").to_bytes(2), utf8.encode("px")],
		[66, b"\x07", (65).to_bytes(2)],
		[67, b"\x01", len("useDebugFov").to_bytes(2), utf8.encode("useDebugFov")],
		[68, b"\x0c", (67).to_bytes(2) + (47).to_bytes(2)],
		[69, b"\x09", (66).to_bytes(2) + (68).to_bytes(2)],
	))

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "a") and eq(desc, "(IZ)V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = instructions.make(0, [
		# 00
		'iload_1',
		['bipush', 79],
		['if_icmpne*', 'a03'],

		# 01
		'iload_2',
		['ifeq*', 'a03'],

		# 02
		['getstatic', 69],
		['iconst_1'],
		'ixor',
		['putstatic', 69],
		'return',

		# 03
		['jump_target*', 'a03']
	]) + a_code[0x03]

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

	with open(mod.config.path("stage/client/lr.class"), "wb") as file:
		file.write(class_file.make(cf))
