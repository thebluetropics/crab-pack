import mod

from operator import eq
from mod.bytecode import (
	instructions,
	class_file,
	constant_pool,
	code_attribute,
	utf8,
	fields
)

def apply_client():
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/client/gs.class"))
	cp = cf[0x04]

	# update constant pool count
	cf[0x03] = (int.from_bytes(cf[0x03]) + 18).to_bytes(2)

	# add new constant pool entries
	cp.append([801, b"\x01", len("hunger").to_bytes(2), utf8.encode("hunger")])
	cp.append([802, b"\x0c", (801).to_bytes(2) + (642).to_bytes(2)])
	cp.append([803, b"\x09", (48).to_bytes(2) + (802).to_bytes(2)])

	cp.append([804, b"\x01", len("maxHunger").to_bytes(2), utf8.encode("maxHunger")])
	cp.append([805, b"\x0c", (804).to_bytes(2) + (642).to_bytes(2)])
	cp.append([806, b"\x09", (48).to_bytes(2) + (805).to_bytes(2)])

	cp.append([807, b"\x01", len("thirst").to_bytes(2), utf8.encode("thirst")])
	cp.append([808, b"\x0c", (807).to_bytes(2) + (642).to_bytes(2)])
	cp.append([809, b"\x09", (48).to_bytes(2) + (808).to_bytes(2)])

	cp.append([810, b"\x01", len("maxThirst").to_bytes(2), utf8.encode("maxThirst")])
	cp.append([811, b"\x0c", (810).to_bytes(2) + (642).to_bytes(2)])
	cp.append([812, b"\x09", (48).to_bytes(2) + (811).to_bytes(2)])

	cp.append([813, b"\x01", len("hungerTick").to_bytes(2), utf8.encode("hungerTick")])
	cp.append([814, b"\x0c", (813).to_bytes(2) + (642).to_bytes(2)])
	cp.append([815, b"\x09", (48).to_bytes(2) + (814).to_bytes(2)])

	cp.append([816, b"\x01", len("thirstTick").to_bytes(2), utf8.encode("thirstTick")])
	cp.append([817, b"\x0c", (816).to_bytes(2) + (642).to_bytes(2)])
	cp.append([818, b"\x09", (48).to_bytes(2) + (817).to_bytes(2)])

	# update field count
	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 6).to_bytes(2)

	fields.push(cf, 0x0001, 801, 642, [])
	fields.push(cf, 0x0001, 804, 642, [])
	fields.push(cf, 0x0001, 807, 642, [])
	fields.push(cf, 0x0001, 810, 642, [])
	fields.push(cf, 0x0001, 813, 642, [])
	fields.push(cf, 0x0001, 816, 642, [])

	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "<init>") and eq(desc, "(Lfd;)V"):
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

	# Modify code
	a_code[0x03] = a_code[0x03][0:-1] + instructions.make(0, [
		'aload_0', ['bipush', 100], ['putfield', 803],
		'aload_0', ['bipush', 100], ['putfield', 806],
		'aload_0', ['bipush', 100], ['putfield', 809],
		'aload_0', ['bipush', 100], ['putfield', 812],
		'aload_0', 'iconst_0', ['putfield', 815],
		'aload_0', 'iconst_0', ['putfield', 818],
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

	_modify_player_tick_client(cf, cp)

	with open("stage/client/gs.class", "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:gs.class → net.minecraft.entity.player.PlayerEntity")

def _modify_player_tick_client(cf, cp):
	# gs.w_()V → PlayerEntity.tick
	m = None
	for _m in cf[0x0d]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_m[0x01]))
		desc = constant_pool.get_utf8(cp, int.from_bytes(_m[0x02]))

		if eq(name, "w_") and eq(desc, "()V"):
			m = _m
			break

	a = None
	for _a in m[0x04]:
		name = constant_pool.get_utf8(cp, int.from_bytes(_a[0x00]))

		if name.__eq__("Code"):
			a = _a
			break

	a_code = code_attribute.load(a[0x02])
	a_code[0x03] = a_code[0x03][0:-1] + instructions.make(402, [
		'aload_0', ['getfield', 123], ['getfield', 108], ['ifne', 'a06'],
		'aload_0', ['getfield', 815], 'iconst_5', ['if_icmpge*', 'a02'],

		# 01
		'aload_0',
		'aload_0',
		['getfield', 815],
		'iconst_1',
		'iadd',
		['putfield', 815], # → tickCounter++

		# 02
		['jump_target*', 'a02'],
		'aload_0',
		['getfield', 815],
		'iconst_5',
		['if_icmplt*', 'a06'], # → if tickCounter < 5

		# 03
		'aload_0',
		['getfield', 803],
		['ifle*', 'a05'], # → if hunger < 0 or hunger.eq(0)

		# 04
		'aload_0',
		'aload_0',
		['getfield', 803],
		'iconst_1',
		'isub',
		['putfield', 803],

		# 05
		['jump_target*', 'a05'],
		'aload_0',
		'iconst_0',
		['putfield', 815],

		# 06
		['jump_target*', 'a06'],
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
