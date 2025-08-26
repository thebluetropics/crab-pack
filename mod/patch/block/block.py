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
	if not mod.config.is_feature_enabled("fortress_bricks"):
		return

	cf = class_file.load(mod.config.path("stage/client/uu.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 4).to_bytes(2)
	cp.extend([
		[1211, b"\x01", len("fortress_bricks").to_bytes(2), utf8.encode("fortress_bricks")],
		[1212, b"\x0c", (1211).to_bytes(2) + (905).to_bytes(2)],
		[1213, b"\x09", (196).to_bytes(2) + (1212).to_bytes(2)],
		[1214, b"\x08", (1211).to_bytes(2)]
	])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append([
		(0x0001.__or__(0x0008)).to_bytes(2),
		(1211).to_bytes(2), (905).to_bytes(2),
		(0).to_bytes(2), []
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

	a_code[0x03] = a_code[0x03][0:3398] + instructions.make(3398, [
		['new', 196],
		'dup',
		['bipush', 97],
		['sipush', 166],
		['getstatic', 226],
		['invokespecial', 515],
		'fconst_2',
		['invokevirtual', 535],
		['ldc', 22],
		['invokevirtual', 530],
		['getstatic', 344],
		['invokevirtual', 523],
		['ldc_w', 1214],
		['invokevirtual', 527],
		['putstatic', 1213]
	]) + a_code[0x03][3398:3678]
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

	with open(mod.config.path("stage/client/uu.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:uu.class → net.minecraft.block.Block")
