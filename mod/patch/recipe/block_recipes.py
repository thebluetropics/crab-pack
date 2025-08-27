import mod

from operator import eq
from mod.bytecode.fields import make_field
from mod.bytecode.method import get_method
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	constant_pool,
	utf8
)
from mod.bytecode.constant_pool import (
	vcp_utf8_get,
	i2cp_utf8_get,
	icp_utf8_get,
	i2cp_class_get,
	icp_class_get,
	icp_f_get,
	icp_m_get
)

def apply_client():
	if not mod.config.is_feature_enabled("fortress_bricks"):
		return

	cf = class_file.load(mod.config.path("stage/client/jy.class"))
	cp = cf[0x04]

	cp.extend([
		[60, b"\x01", len("fortress_bricks").to_bytes(2), utf8.encode("fortress_bricks")],
		[61, b"\x0c", (60).to_bytes(2) + (44).to_bytes(2)],
		[62, b"\x09", (9).to_bytes(2) + (61).to_bytes(2)],
		[63, b"\x01", len("ab").to_bytes(2), utf8.encode("ab")],
		[64, b"\x08", (63).to_bytes(2)],
		[65, b"\x01", len("ba").to_bytes(2), utf8.encode("ba")],
		[66, b"\x08", (65).to_bytes(2)],
		[67, b"\x01", len("u").to_bytes(2), utf8.encode("u")],
		[68, b"\x0c", (67).to_bytes(2) + (44).to_bytes(2)],
		[69, b"\x09", (9).to_bytes(2) + (68).to_bytes(2)]
	])
	cf[0x03] = (int.from_bytes(cf[0x03]) + 10).to_bytes(2)

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "a") and eq(desc, "(Lhk;)V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:178] + instructions.make(178, [
		'aload_1',
		['new', 5],
		'dup',
		['getstatic', 62],
		['invokespecial', 18],
		['bipush', 6],
		['anewarray', 7],
		'dup',
		'iconst_0',
		['ldc', 64],
		'aastore',
		'dup',
		'iconst_1',
		['ldc', 66],
		'aastore',
		'dup',
		'iconst_2',
		['bipush', 97],
		['invokestatic', 19],
		'aastore',
		'dup',
		'iconst_3',
		['getstatic', 15],
		'aastore',
		'dup',
		'iconst_4',
		['bipush', 98],
		['invokestatic', 19],
		'aastore',
		'dup',
		'iconst_5',
		['getstatic', 69],
		'aastore',
		['invokevirtual', 17],
		'return'
	])

	# Update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# Remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, _a in a_code[0x07]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if eq(name, "LineNumberTable"):
			del a_code[0x07][i]
			break

	# Update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# Update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path("stage/client/jy.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:jy.class → net.minecraft.recipe.BlockRecipes")

def apply_server():
	if not mod.config.is_feature_enabled("fortress_bricks"):
		return

	cf = class_file.load(mod.config.path("stage/server/gp.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 10).to_bytes(2)
	cp.extend([
		[60, b"\x01", len("fortress_bricks").to_bytes(2), utf8.encode("fortress_bricks")],
		[61, b"\x0c", (60).to_bytes(2) + i2cp_utf8_get(cp, 'Lna;')],
		[62, b"\x09", i2cp_class_get(cp, 'na') + (61).to_bytes(2)],
		[63, b"\x01", len("ab").to_bytes(2), utf8.encode("ab")],
		[64, b"\x08", (63).to_bytes(2)],
		[65, b"\x01", len("ba").to_bytes(2), utf8.encode("ba")],
		[66, b"\x08", (65).to_bytes(2)],
		[67, b"\x01", len("u").to_bytes(2), utf8.encode("u")],
		[68, b"\x0c", (67).to_bytes(2) + i2cp_utf8_get(cp, 'Lna;')],
		[69, b"\x09", i2cp_class_get(cp, 'na') + (68).to_bytes(2)]
	])

	m = get_method(cf, cp, 'a', '(Ley;)V')
	a = get_attribute(m[0x04], cp, 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:178] + instructions.make(178, [
		'aload_1',
		['new', icp_class_get(cp, 'fy')],
		'dup',
		['getstatic', 62],
		['invokespecial', icp_m_get(cp, 'fy', '<init>', '(Lna;)V')],
		['bipush', 6],
		['anewarray', icp_class_get(cp, 'java/lang/Object')],
		'dup',
		'iconst_0',
		['ldc', 64],
		'aastore',
		'dup',
		'iconst_1',
		['ldc', 66],
		'aastore',
		'dup',
		'iconst_2',
		['bipush', 97],
		['invokestatic', icp_m_get(cp, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_3',
		['getstatic', icp_f_get(cp, 'na', 'x', 'Lna;')],
		'aastore',
		'dup',
		'iconst_4',
		['bipush', 98],
		['invokestatic', icp_m_get(cp, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_5',
		['getstatic', 69],
		'aastore',
		['invokevirtual', icp_m_get(cp, 'ey', 'a', '(Lfy;[Ljava/lang/Object;)V')],
		'return'
	])

	# Update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# Remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, _a in a_code[0x07]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if eq(name, "LineNumberTable"):
			del a_code[0x07][i]
			break

	# Update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# Update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path("stage/server/gp.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched server:gp.class → net.minecraft.recipe.BlockRecipes")
