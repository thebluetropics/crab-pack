import mod

from mod.attribute import get_attribute
from mod.field import create_field
from mod.method import create_method, get_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	get_utf8_at
)

def apply(side_name):
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['gs', 'em'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	add_fields = [
		create_field(cf, cp_cache, ['public'], 'hunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxHunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'thirst', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxThirst', 'I'),
		create_field(cf, cp_cache, ['public'], 'hungerTick', 'I'),
		create_field(cf, cp_cache, ['public'], 'thirstTick', 'I')
	]
	cf[0x0a] = (int.from_bytes(cf[0x0a]) + len(add_fields)).to_bytes(2)
	cf[0x0b].extend(add_fields)

	_modify_constructor(cf, cp_cache, side, c_name)
	_modify_tick_method(cf, cp_cache, side_name, side, c_name)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 4).to_bytes(2)
	cf[0x0d].extend([
		_create_update_hunger_method(cf, cp_cache),
		_create_restore_hunger_method(cf, cp_cache, c_name),
		_create_update_thirst_method(cf, cp_cache),
		_create_restore_thirst_method(cf, cp_cache, c_name)
	])

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.entity.player.PlayerEntity')

def _modify_constructor(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<init>', ['(Lfd;)V', '(Ldj;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(0, [
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, c_name, 'maxHunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, c_name, 'maxThirst', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(cf, cp_cache, c_name, 'hungerTick', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(cf, cp_cache, c_name, 'thirstTick', 'I')],
		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_tick_method(cf, cp_cache, side_name, side, c_name):
	m = get_method(cf, cp_cache, ['w_', 'm_'][side], '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(402, [
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, ['aI', 'aL'][side], ['Lfd;', 'Ldj;'][side])],
		['getfield', icpx_f(cf, cp_cache, ['fd', 'dj'][side], 'B', 'Z')],
		['ifne*', 'end_hunger_tick'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hungerTick', 'I')],
		'iconst_5',
		['if_icmpge*', 'a'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hungerTick', 'I')],
		'iconst_1',
		'iadd',
		['putfield', icpx_f(cf, cp_cache, c_name, 'hungerTick', 'I')],

		['jump_target*', 'a'],
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hungerTick', 'I')],
		'iconst_5',
		['if_icmplt*', 'end_hunger_tick'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],
		['ifle*', 'b'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],
		'iconst_1',
		'isub',
		['putfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],

		'aload_0',
		'aload_0', ['getfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],
		'aload_0', ['getfield', icpx_f(cf, cp_cache, c_name, 'maxHunger', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'updateHunger', '(II)V')],

		['goto*', 'c'],

		['jump_target*', 'b'],
		'aload_0',
		'aconst_null',
		'iconst_1',
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lsn;I)Z', '(Llq;I)Z'][side])],
		'pop',

		['jump_target*', 'c'],
		'aload_0',
		'iconst_0',
		['putfield', icpx_f(cf, cp_cache, c_name, 'hungerTick', 'I')],

		['jump_target*', 'end_hunger_tick'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, ['aI', 'aL'][side], ['Lfd;', 'Ldj;'][side])],
		['getfield', icpx_f(cf, cp_cache, ['fd', 'dj'][side], 'B', 'Z')],
		['ifne*', 'end_thirst_tick'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'thirstTick', 'I')],
		'iconst_5',
		['if_icmpge*', 'd'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'thirstTick', 'I')],
		'iconst_1',
		'iadd',
		['putfield', icpx_f(cf, cp_cache, c_name, 'thirstTick', 'I')],

		['jump_target*', 'd'],
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'thirstTick', 'I')],
		'iconst_5',
		['if_icmplt*', 'end_thirst_tick'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],
		['ifle*', 'e'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],
		'iconst_1',
		'isub',
		['putfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],

		'aload_0',
		'aload_0', ['getfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],
		'aload_0', ['getfield', icpx_f(cf, cp_cache, c_name, 'maxThirst', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'updateThirst', '(II)V')],

		['goto*', 'f'],

		['jump_target*', 'e'],
		'aload_0',
		'aconst_null',
		'iconst_1',
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lsn;I)Z', '(Llq;I)Z'][side])],
		'pop',

		['jump_target*', 'f'],
		'aload_0',
		'iconst_0',
		['putfield', icpx_f(cf, cp_cache, c_name, 'thirstTick', 'I')],

		['jump_target*', 'end_thirst_tick'],

		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _create_update_hunger_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['protected'], 'updateHunger', '(II)V')

	code = instructions.assemble(0, [
		'return'
	])
	a_code = attribute.code.assemble([
		(0).to_bytes(2),
		(3).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _create_restore_hunger_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'restoreHunger', '(I)V')

	code = instructions.assemble(0, [
		'aload_0',
		'dup',
		['getfield', icpx_f(cf, cp_cache, c_name, 'maxHunger', 'I')],
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],
		'iload_1',
		'iadd',
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Math', 'min', '(II)I')],
		['putfield', icpx_f(cf, cp_cache, c_name, 'hunger', 'I')],
		'return'
	])
	a_code = attribute.code.assemble([
		(4).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _create_update_thirst_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['protected'], 'updateThirst', '(II)V')

	code = instructions.assemble(0, [
		'return'
	])
	a_code = attribute.code.assemble([
		(0).to_bytes(2),
		(3).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _create_restore_thirst_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'restoreThirst', '(I)V')

	code = instructions.assemble(0, [
		'aload_0',
		'dup',
		['getfield', icpx_f(cf, cp_cache, c_name, 'maxThirst', 'I')],
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],
		'iload_1',
		'iadd',
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Math', 'min', '(II)I')],
		['putfield', icpx_f(cf, cp_cache, c_name, 'thirst', 'I')],
		'return'
	])
	a_code = attribute.code.assemble([
		(4).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
