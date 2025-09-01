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

def apply_client():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/client/gs.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 6).to_bytes(2)
	cf[0x0b].extend([
		create_field(cf, cp_cache, ['public'], 'hunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxHunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'thirst', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxThirst', 'I'),
		create_field(cf, cp_cache, ['public'], 'hungerTick', 'I'),
		create_field(cf, cp_cache, ['public'], 'thirstTick', 'I')
	])

	m = get_method(cf, cp_cache, '<init>', '(Lfd;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(0, [
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'gs', 'hunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'gs', 'maxHunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'gs', 'thirst', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'gs', 'maxThirst', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(cf, cp_cache, 'gs', 'hungerTick', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(cf, cp_cache, 'gs', 'thirstTick', 'I')],
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

	_modify_tick_client(cf, cp_cache)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].extend([_create_update_hunger_method_client(cf, cp_cache)])

	with open('stage/client/gs.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched client:gs.class → net.minecraft.entity.player.PlayerEntity')

def _modify_tick_client(cf, cp_cache):
	# gs.w_()V → PlayerEntity.tick
	m = get_method(cf, cp_cache, 'w_', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])
	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(402, [
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'gs', 'aI', 'Lfd;')], ['getfield', icpx_f(cf, cp_cache, 'fd', 'B', 'Z')], ['ifne*', 'a06'],
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'gs', 'hungerTick', 'I')], 'iconst_5', ['if_icmpge*', 'a02'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'gs', 'hungerTick', 'I')],
		'iconst_1',
		'iadd',
		['putfield', icpx_f(cf, cp_cache, 'gs', 'hungerTick', 'I')],

		['jump_target*', 'a02'],
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'gs', 'hungerTick', 'I')],
		'iconst_5',
		['if_icmplt*', 'a06'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'gs', 'hunger', 'I')],
		['ifle*', 'aElse'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'gs', 'hunger', 'I')],
		'iconst_1',
		'isub',
		['putfield', icpx_f(cf, cp_cache, 'gs', 'hunger', 'I')],

		'aload_0',
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'gs', 'hunger', 'I')],
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'gs', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, 'gs', 'updateHunger', '(II)V')],

		['goto*', 'a05'],

		['jump_target*', 'aElse'],
		'aload_0',
		'aconst_null',
		'iconst_1',
		['invokevirtual', icpx_m(cf, cp_cache, 'gs', 'a', '(Lsn;I)Z')],
		'pop',

		['jump_target*', 'a05'],
		'aload_0',
		'iconst_0',
		['putfield', icpx_f(cf, cp_cache, 'gs', 'hungerTick', 'I')],

		['jump_target*', 'a06'],
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

def _create_update_hunger_method_client(cf, cp_cache):
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

def apply_server():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/server/em.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 6).to_bytes(2)
	cf[0x0b].extend([
		create_field(cf, cp_cache, ['public'], 'hunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxHunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'thirst', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxThirst', 'I'),
		create_field(cf, cp_cache, ['public'], 'hungerTick', 'I'),
		create_field(cf, cp_cache, ['public'], 'thirstTick', 'I')
	])

	m = get_method(cf, cp_cache, '<init>', '(Ldj;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(0, [
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'em', 'hunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'em', 'maxHunger', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'em', 'thirst', 'I')],
		'aload_0', ['bipush', 100], ['putfield', icpx_f(cf, cp_cache, 'em', 'maxThirst', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(cf, cp_cache, 'em', 'hungerTick', 'I')],
		'aload_0', 'iconst_0', ['putfield', icpx_f(cf, cp_cache, 'em', 'thirstTick', 'I')],
		'return'
	])
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

	_modify_tick_server(cf, cp_cache)

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 1).to_bytes(2)
	cf[0x0d].extend([_create_update_hunger_method_server(cf, cp_cache)])

	with open('stage/server/em.class', 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:em.class → net.minecraft.entity.PlayerEntity')

def _modify_tick_server(cf, cp_cache):
	# em.m_()V → PlayerEntity.tick
	m = get_method(cf, cp_cache, 'm_', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])
	a_code[0x03] = a_code[0x03][0:-1] + instructions.assemble(402, [
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'em', 'aL', 'Ldj;')], ['getfield', icpx_f(cf, cp_cache, 'dj', 'B', 'Z')], ['ifne*', 'a06'],
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'em', 'hungerTick', 'I')], 'iconst_5', ['if_icmpge*', 'a02'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'em', 'hungerTick', 'I')],
		'iconst_1',
		'iadd',
		['putfield', icpx_f(cf, cp_cache, 'em', 'hungerTick', 'I')],

		['jump_target*', 'a02'],
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'em', 'hungerTick', 'I')],
		'iconst_5',
		['if_icmplt*', 'a06'],

		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'em', 'hunger', 'I')],
		['ifle*', 'aElse'],

		'aload_0',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, 'em', 'hunger', 'I')],
		'iconst_1',
		'isub',
		['putfield', icpx_f(cf, cp_cache, 'em', 'hunger', 'I')],

		'aload_0',
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'em', 'hunger', 'I')],
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'em', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, 'em', 'updateHunger', '(II)V')],

		['goto*', 'a05'],

		['jump_target*', 'aElse'],
		'aload_0',
		'aconst_null',
		'iconst_1',
		['invokevirtual', icpx_m(cf, cp_cache, 'em', 'a', '(Llq;I)Z')],
		'pop',

		['jump_target*', 'a05'],
		'aload_0',
		'iconst_0',
		['putfield', icpx_f(cf, cp_cache, 'em', 'hungerTick', 'I')],

		['jump_target*', 'a06'],
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

def _create_update_hunger_method_server(cf, cp_cache):
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
