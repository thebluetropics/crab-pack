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
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/client/uq.class"))
	cp = cf[0x04]

	cf[0x03] = (int.from_bytes(cf[0x03]) + 14).to_bytes(2)
	cp.append([508, b"\x03", (0x40ff9966).to_bytes(4)])
	cp.append([509, b"\x03", (0x400099cc).to_bytes(4)])
	cp.append([510, b"\x03", (0xff000000).to_bytes(4)])
	cp.append([511, b"\x03", (0xff33cc00).to_bytes(4)]) # Hunger Bar Color
	cp.append([512, b"\x03", (0xff00ffff).to_bytes(4)]) # Thirst bar color

	cp.append([513, b"\x01", len(utf8.encode("hunger")).to_bytes(2), utf8.encode("hunger")])
	cp.append([514, b"\x0c", (513).to_bytes(2) + (386).to_bytes(2)])
	cp.append([515, b"\x09", (44).to_bytes(2) + (514).to_bytes(2)])

	cp.append([516, b"\x01", len(utf8.encode("maxHunger")).to_bytes(2), utf8.encode("maxHunger")])
	cp.append([517, b"\x0c", (516).to_bytes(2) + (386).to_bytes(2)])
	cp.append([518, b"\x09", (44).to_bytes(2) + (517).to_bytes(2)])

	cp.append([519, b"\x03", (0x40000000).to_bytes(4)])

	cp.append([520, b"\x03", (0xff224400).to_bytes(4)])
	cp.append([521, b"\x03", (0xff004466).to_bytes(4)])

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "a") and eq(desc, "(FZII)V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])

	a_code[0x01] = (26).to_bytes(2)

	a_code[0x03] = a_code[0x03][0:943] + instructions.make(0, [
		['sipush', 2929],
		['invokestatic', 182], # → GL11.glEnable(GL11.GL_DEPTH_TEST)

		# 00
    'aload_0',
    ['getfield', 129], # → this.minecraft
    ['getfield', 115], # → this.minecraft.player
    ['getfield', 515], # → int hunger
    'i2f',
    'aload_0',
    ['getfield', 129], # → this.minecraft
    ['getfield', 115], # → this.minecraft.player
    ['getfield', 518], # → int maxHunger
    'i2f',
    'fdiv', # hunger / maxHunger
		['bipush', 10],
		'i2f',
    'fmul', # percentage * 10.0f
		'f2i',
		['istore', 24],

		# 00
		['bipush', 10],
		['iload', 24],
		'isub',
		['istore', 25],

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 79], 'iadd', # → x0
		['iload', 7], ['bipush', 33], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd', # → x1
		['iload', 7], ['bipush', 23], ['iload', 24], ['iadd'], 'isub', # → y1
		['ldc_w', 519], # → color
		['invokevirtual', 203], # → fill box for hunger (upper)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 79], 'iadd', # → x0
		['iload', 7], ['bipush', 23], ['iload', 24], ['iadd'], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd', # → x1
		['iload', 7], ['bipush', 23], 'isub', # → y1
		['ldc_w', 508], # → color
		['invokevirtual', 203], # → fill box for hunger (lower)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 69], 'iadd', # → x0
		['iload', 7], ['bipush', 33], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd', # → x1
		['iload', 7],
		['bipush', 23], # → y1
		'isub',
		['ldc_w', 509],
		['invokevirtual', 203], # → fill box for thirst (lower)

		# 00
		'aload_0',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 90], # → x0
		'iadd',
		['iload', 7],
		['bipush', 33], # → y0
		'isub',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 91], # → x1
		'iadd',
		['iload', 7],
		['bipush', 23], # → y1
		'isub',
		['ldc_w', 520], # color
		['invokevirtual', 203], # → fill box for hunger bar (background)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd', # → x0
		['iload', 7], ['bipush', 23], ['iload', 24], ['iadd'], 'isub',  # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 91], 'iadd', # → x1
		['iload', 7], ['bipush', 23], 'isub', # → y1
		['ldc_w', 511], # color
		['invokevirtual', 203], # → fill box for hunger bar (percentage)

		'aload_0',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 77], # → x0
		'iadd',
		['iload', 7],
		['bipush', 33], # → y0
		'isub',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 78], # → x1
		'iadd',
		['iload', 7],
		['bipush', 23], # → y1
		'isub',
		['ldc_w', 521],
		['invokevirtual', 203], # → fill box for thirst bar (background)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd', # → x0
		['iload', 7], ['bipush', 33], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 78], 'iadd', # → x1
		['iload', 7], ['bipush', 23], 'isub', # → y1
		['ldc_w', 512], # color
		['invokevirtual', 203], # → fill box for thirst bar (percentage)

		'fconst_1',
		'fconst_1',
		'fconst_1',
		'fconst_1',
		['invokestatic', 180],

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 80], 'iadd', # → x
		['iload', 7], ['bipush', 33], 'isub', # → y
		['bipush', 16], # → u
		['bipush', 27], # → v
		['bipush', 10], # → width
		['iload', 25], # → height
		['invokevirtual', 206], # → uq.b(IIIIII)V

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 80], 'iadd', # → x
		['iload', 7], ['bipush', 33], 'isub', ['iload', 25], 'iadd', # → y
		['bipush', 26], # → u
		['bipush', 27], ['iload', 25], 'iadd', # → v
		['bipush', 10], # → width
		['iload', 24], # → height
		['invokevirtual', 206], # → uq.b(IIIIII)V

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 70], 'iadd', # → x
		['iload', 7], ['bipush', 33], 'isub', # → y
		['bipush', 23], # → u
		['bipush', 37], # → v
		['bipush', 7], # → width
		['bipush', 10], # → height
		['invokevirtual', 206], # → uq.b(IIIIII)V

		['sipush', 2929],
		['invokestatic', 183] # → GL11.glEnable(GL11.GL_DEPTH_TEST)
	]) + a_code[0x03][943:2102]

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

	with open(mod.config.path("stage/client/uq.class"), "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:uq.class → net.minecraft.client.gui.hud.InGameHud")
