import mod

from operator import eq
from mod.bytecode.fields import make_field
from mod.bytecode.method import (make_method, get_method)
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	constant_pool
)
from mod.bytecode.constant_pool import (
	icpx_utf8,
	icpx_f,
	i2cpx_utf8
)

def apply_client():
	if not mod.config.is_feature_enabled("hunger_and_thirst"):
		return

	cf = class_file.load(mod.config.path("stage/client/gs.class"))
	xcp = constant_pool.use_helper(cf)
	cp = cf[0x04]

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 6).to_bytes(2)
	cf[0x0b].append(make_field(['public'], icpx_utf8(xcp, 'hunger'), icpx_utf8(xcp, 'I')))
	cf[0x0b].append(make_field(['public'], icpx_utf8(xcp, 'maxHunger'), icpx_utf8(xcp, 'I')))
	cf[0x0b].append(make_field(['public'], icpx_utf8(xcp, 'thirst'), icpx_utf8(xcp, 'I')))
	cf[0x0b].append(make_field(['public'], icpx_utf8(xcp, 'maxThirst'), icpx_utf8(xcp, 'I')))
	cf[0x0b].append(make_field(['public'], icpx_utf8(xcp, 'hungerTick'), icpx_utf8(xcp, 'I')))
	cf[0x0b].append(make_field(['public'], icpx_utf8(xcp, 'thirstTick'), icpx_utf8(xcp, 'I')))

	m = get_method(cf, cp, '<init>', '(Lfd;)V')
	a = get_attribute(m[0x04], cp, 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + instructions.make(0, [
		'aload_0', ['bipush', 100], ['putfield', icpx_f(xcp, 'gs', 'hunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(xcp, 'gs', 'maxHunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(xcp, 'gs', 'thirst', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(xcp, 'gs', 'maxThirst', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(xcp, 'gs', 'hungerTick', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(xcp, 'gs', 'thirstTick', 'I')],
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

	_modify_player_tick_client(cf, cp, xcp)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].extend([_add_update_hunger_method(cf, cp, xcp)])

	with open("stage/client/gs.class", "wb") as f:
		f.write(class_file.make(cf))

	print("Patched client:gs.class → net.minecraft.entity.player.PlayerEntity")

def _modify_player_tick_client(cf, cp, xcp):
	# gs.w_()V → PlayerEntity.tick
	m = get_method(cf, cp, 'w_', '()V')
	a = get_attribute(m[0x04], cp, 'Code')

	a_code = code_attribute.load(a[0x02])
	a_code[0x03] = a_code[0x03][0:-1] + instructions.make(402, [
		'aload_0', ['getfield', icpx_f(xcp, 'gs', 'aI', 'Lfd;')], ['getfield', icpx_f(xcp, 'fd', 'B', 'Z')], ['ifne*', 'a06'],
		'aload_0', ['getfield', icpx_f(xcp, 'gs', 'tickCounter', 'I')], 'iconst_5', ['if_icmpge*', 'a02'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(xcp, 'gs', 'tickCounter', 'I')],
		'iconst_1',
		'iadd',
		['putfield', icpx_f(xcp, 'gs', 'tickCounter', 'I')],

		['jump_target*', 'a02'],
		'aload_0',
		['getfield', icpx_f(xcp, 'gs', 'tickCounter', 'I')],
		'iconst_5',
		['if_icmplt*', 'a06'],

		'aload_0',
		['getfield', icpx_f(xcp, 'gs', 'hunger', 'I')],
		['ifle*', 'a05'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(xcp, 'gs', 'hunger', 'I')],
		'iconst_1',
		'isub',
		['putfield', icpx_f(xcp, 'gs', 'hunger', 'I')],

		['jump_target*', 'a05'],
		'aload_0',
		'iconst_0',
		['putfield', icpx_f(xcp, 'gs', 'tickCounter', 'I')],

		['jump_target*', 'a06'],
		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if constant_pool.get_utf8(cp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _add_update_hunger_method(cf, cp, xcp):
	m = make_method(['protected'], icpx_utf8(xcp, 'updateHunger'), icpx_utf8(xcp, '(II)V'))

	code = instructions.make(0, [
		'return'
	])
	a_code = code_attribute.assemble([
		(0).to_bytes(2),
		(3).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
