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

	cf = class_file.load(mod.config.path("stage/client/px.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 3).to_bytes(2)

	cp.extend((
		[899, b"\x01", len("useDebugFov").to_bytes(2), utf8.encode("useDebugFov")],
		[900, b"\x0c", (899).to_bytes(2) + (748).to_bytes(2)],
		[901, b"\x09", (88).to_bytes(2) + (900).to_bytes(2)],
	))

	# update field count
	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)

	# add field
	cf[0x0b].append([(0x0001 | 0x0008).to_bytes(2), (899).to_bytes(2), (748).to_bytes(2), (0).to_bytes(2), []])

	_modify_static_initializer(cf, cp)

	# px.d(F)F → getFov
	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "d") and eq(desc, "(F)F"):
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
	a_code[0x03] = a_code[0x03][0:57] + instructions.make(57, [
		['getstatic', 901],
		['ifeq*', 'a'],
		['bipush', 30],
		'i2f',
		'freturn',
		['jump_target*', 'a']
	]) + a_code[0x03][57:76]

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

	with open(mod.config.path("stage/client/px.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:px.class → net.minecraft.client.render.GameRenderer")

def _modify_static_initializer(cf, cp):
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

	# load code attribute
	a_code = code_attribute.load(a[0x02])

	# modify code
	a_code[0x03] = a_code[0x03][0:-1] + instructions.make(0, [
		'iconst_0', ['putstatic', 901],
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
