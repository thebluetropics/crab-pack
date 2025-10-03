import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
)
from modmaker.f import (
	create_field
)
from modmaker.m import (
	get_method,
	create_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	get_utf8_at,
	i2cpx_utf8
)

def apply(side_name):
	if not mod.config.is_one_of_features_enabled(['etc.hunger_and_thirst', 'blackbox']):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['gs', 'em'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'hunger', 'I'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'maxHunger', 'I'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'thirst', 'I'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'maxThirst', 'I'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'hungerTick', 'I'))
		cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'thirstTick', 'I'))

	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	_modify_tick_method(cf, cp_cache, side_name, side, c_name)

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		_modify_constructor(cf, cp_cache, side, c_name)
		_modify_read_nbt_method(cf, cp_cache, side, c_name)
		_modify_write_nbt_method(cf, cp_cache, side, c_name)

	if mod.config.is_feature_enabled('blackbox'):
		_modify_on_killed_by_method(cf, cp_cache, side)

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		cf[0x0d].extend([
			_create_update_hunger_method(cf, cp_cache, side),
			_create_restore_hunger_method(cf, cp_cache, c_name, side),
			_create_update_thirst_method(cf, cp_cache, side),
			_create_restore_thirst_method(cf, cp_cache, c_name, side),
			_create_open_smelter_screen_method(cf, cp_cache, side)
		])
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.entity.player.PlayerEntity')

def _modify_constructor(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<init>', ['(Lfd;)V', '(Ldj;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + assemble_code(cf, cp_cache, side, 0, [
		'aload_0', ['bipush', 100], ['putfield', c_name, 'hunger', 'I'],
		'aload_0', ['bipush', 100], ['putfield', c_name, 'maxHunger', 'I'],
		'aload_0', ['bipush', 100], ['putfield', c_name, 'thirst', 'I'],
		'aload_0', ['bipush', 100], ['putfield', c_name, 'maxThirst', 'I'],
		'aload_0', 'iconst_0', ['putfield', c_name, 'hungerTick', 'I'],
		'aload_0', 'iconst_0', ['putfield', c_name, 'thirstTick', 'I'],
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
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_tick_method(cf, cp_cache, side_name, side, c_name):
	m = get_method(cf, cp_cache, ['w_', 'm_'][side], '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	hunger_reduce_every = ['sipush', 200]
	thirst_reduce_every = ['sipush', 160]

	a_code[0x00] = (12).to_bytes(2)

	code = []

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		code.extend([
			'aload_0',
			['getfield', c_name, ('aI', 'aL'), ('Lfd;', 'Ldj;')],
			['getfield', ('fd', 'dj'), 'B', 'Z'],
			['ifne', 'end_hunger_tick'],

			'aload_0',
			['getfield', c_name, 'hungerTick', 'I'],
			hunger_reduce_every,
			['if_icmpge', 'a'],

			'aload_0',
			'aload_0',
			['getfield', c_name, 'hungerTick', 'I'],
			'iconst_1',
			'iadd',
			['putfield', c_name, 'hungerTick', 'I'],

			['label', 'a'],
			'aload_0',
			['getfield', c_name, 'hungerTick', 'I'],
			hunger_reduce_every,
			['if_icmplt', 'end_hunger_tick'],

			'aload_0',
			['getfield', c_name, 'hunger', 'I'],
			['ifle', 'b'],

			'aload_0',
			'aload_0',
			['getfield', c_name, 'hunger', 'I'],
			'iconst_1',
			'isub',
			['putfield', c_name, 'hunger', 'I'],

			'aload_0',
			'aload_0', ['getfield', c_name, 'hunger', 'I'],
			'aload_0', ['getfield', c_name, 'maxHunger', 'I'],
			['invokevirtual', c_name, 'updateHunger', '(II)V'],

			['goto', 'c'],

			['label', 'b'],
			'aload_0',
			'aconst_null',
			'iconst_1',
			['invokevirtual', c_name, 'a', ('(Lsn;I)Z', '(Llq;I)Z')],
			'pop',

			['label', 'c'],
			'aload_0',
			'iconst_0',
			['putfield', c_name, 'hungerTick', 'I'],

			['label', 'end_hunger_tick'],

			'aload_0',
			['getfield', c_name, ('aI', 'aL'), ('Lfd;', 'Ldj;')],
			['getfield', ('fd', 'dj'), 'B', 'Z'],
			['ifne', 'end_thirst_tick'],

			'aload_0',
			['getfield', c_name, 'thirstTick', 'I'],
			thirst_reduce_every,
			['if_icmpge', 'd'],

			'aload_0',
			'aload_0',
			['getfield', c_name, 'thirstTick', 'I'],
			'iconst_1',
			'iadd',
			['putfield', c_name, 'thirstTick', 'I'],

			['label', 'd'],
			'aload_0',
			['getfield', c_name, 'thirstTick', 'I'],
			thirst_reduce_every,
			['if_icmplt', 'end_thirst_tick'],

			'aload_0',
			['getfield', c_name, 'thirst', 'I'],
			['ifle', 'e'],

			'aload_0',
			'aload_0',
			['getfield', c_name, 'thirst', 'I'],
			'iconst_1',
			'isub',
			['putfield', c_name, 'thirst', 'I'],

			'aload_0',
			'aload_0', ['getfield', c_name, 'thirst', 'I'],
			'aload_0', ['getfield', c_name, 'maxThirst', 'I'],
			['invokevirtual', c_name, 'updateThirst', '(II)V'],

			['goto', 'f'],

			['label', 'e'],
			'aload_0',
			'aconst_null',
			'iconst_1',
			['invokevirtual', c_name, 'a', ('(Lsn;I)Z', '(Llq;I)Z')],
			'pop',

			['label', 'f'],
			'aload_0',
			'iconst_0',
			['putfield', c_name, 'thirstTick', 'I'],

			['label', 'end_thirst_tick']
		])

	if mod.config.is_feature_enabled('blackbox'):
		code.extend([
			'aload_0', ['getfield', ('gs', 'em'), ('aI', 'aL'), ('Lfd;', 'Ldj;')], ['getfield', ('fd', 'dj'), 'B', 'Z'],
			['ifne', 'skip'],
			'aload_0', ['invokevirtual', ('gs', 'em'), ('W', 'T'), '()Z'],
			['ifeq', 'skip'],

			['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
			'aload_0', ['getfield', ('gs', 'em'), ('l', 'r'), 'Ljava/lang/String;'],
			'aload_0',
			['getfield', ('gs', 'em'), ('aI', 'aL'), ('Lfd;', 'Ldj;')],
			['getfield', ('fd', 'dj'), 't', ('Lxa;', 'Los;')],
			['getfield', ('xa', 'os'), 'g', 'I'],
			'aload_0', ['getfield', ('gs', 'em'), ('aM', 'aP'), 'D'],
			'aload_0', ['getfield', ('gs', 'em'), ('aN', 'aQ'), 'D'],
			'aload_0', ['getfield', ('gs', 'em'), ('aO', 'aR'), 'D'],
			'aload_0', ['getfield', ('gs', 'em'), ('aS', 'aV'), 'F'],
			'aload_0', ['getfield', ('gs', 'em'), ('aT', 'aW'), 'F'],
			'aload_0', ['invokevirtual', ('gs', 'em'), ('t', 'ah'), '()Z'],
			['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'onPlayerTick', '(Ljava/lang/String;IDDDFFZ)V'],

			['label', 'skip'],
		])

	code.append('return')

	a_code[0x03] = a_code[0x03][0:-1] + assemble_code(cf, cp_cache, side, 402, code)

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _create_update_hunger_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['protected'], 'updateHunger', '(II)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'return'
	])
	a_code = a_code_assemble([
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

def _create_restore_hunger_method(cf, cp_cache, c_name, side):
	m = create_method(cf, cp_cache, ['public'], 'restoreHunger', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'dup',
		['getfield', c_name, 'maxHunger', 'I'],
		'aload_0',
		['getfield', c_name, 'hunger', 'I'],
		'iload_1',
		'iadd',
		['invokestatic', 'java/lang/Math', 'min', '(II)I'],
		['putfield', c_name, 'hunger', 'I'],
		'return'
	])
	a_code = a_code_assemble([
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

def _create_update_thirst_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['protected'], 'updateThirst', '(II)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'return'
	])
	a_code = a_code_assemble([
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

def _create_restore_thirst_method(cf, cp_cache, c_name, side):
	m = create_method(cf, cp_cache, ['public'], 'restoreThirst', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'dup',
		['getfield', c_name, 'maxThirst', 'I'],
		'aload_0',
		['getfield', c_name, 'thirst', 'I'],
		'iload_1',
		'iadd',
		['invokestatic', 'java/lang/Math', 'min', '(II)I'],
		['putfield', c_name, 'thirst', 'I'],
		'return'
	])
	a_code = a_code_assemble([
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

def _modify_read_nbt_method(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, 'a', ['(Lnu;)V', '(Liq;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:152] + assemble_code(cf, cp_cache, side, 152, [
		'aload_0',
		'aload_1',
		['ldc_w.string', 'Hunger'],
		['invokevirtual', ('nu', 'iq'), 'd', '(Ljava/lang/String;)S'],
		['putfield', c_name, 'hunger', 'I'],
		'aload_0',
		'aload_1',
		['ldc_w.string', 'MaxHunger'],
		['invokevirtual', ('nu', 'iq'), 'd', '(Ljava/lang/String;)S'],
		['putfield', c_name, 'maxHunger', 'I'],
		'aload_0',
		'aload_1',
		['ldc_w.string', 'Thirst'],
		['invokevirtual', ('nu', 'iq'), 'd', '(Ljava/lang/String;)S'],
		['putfield', c_name, 'thirst', 'I'],
		'aload_0',
		'aload_1',
		['ldc_w.string', 'MaxThirst'],
		['invokevirtual', ('nu', 'iq'), 'd', '(Ljava/lang/String;)S'],
		['putfield', c_name, 'maxThirst', 'I'],
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
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_write_nbt_method(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, 'b', ['(Lnu;)V', '(Liq;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:102] + assemble_code(cf, cp_cache, side, 102, [
		'aload_1',
		['ldc_w.string', 'Hunger'],
		'aload_0',
		['getfield', c_name, 'hunger', 'I'],
		'i2s',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;S)V'],
		'aload_1',
		['ldc_w.string', 'MaxHunger'],
		'aload_0',
		['getfield', c_name, 'maxHunger', 'I'],
		'i2s',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;S)V'],
		'aload_1',
		['ldc_w.string', 'Thirst'],
		'aload_0',
		['getfield', c_name, 'thirst', 'I'],
		'i2s',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;S)V'],
		'aload_1',
		['ldc_w.string', 'MaxThirst'],
		'aload_0',
		['getfield', c_name, 'maxThirst', 'I'],
		'i2s',
		['invokevirtual', ('nu', 'iq'), 'a', '(Ljava/lang/String;S)V'],
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
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

def _create_open_smelter_screen_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'openSmelterScreen', '(Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'return'
	])
	a_code = a_code_assemble([
		(0).to_bytes(2),
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

def _modify_on_killed_by_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, ['b', 'a'][side], ['(Lsn;)V', '(Llq;)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + assemble_code(cf, cp_cache, side, len(a_code[0x03]) - 1, [
		'aload_0', ['getfield', ('gs', 'em'), ('aI', 'aL'), ('Lfd;', 'Ldj;')], ['getfield', ('fd', 'dj'), 'B', 'Z'],
		['ifne', 'skip'],
		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		'aload_0', ['getfield', ('gs', 'em'), ('l', 'r'), 'Ljava/lang/String;'],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'onPlayerDied', '(Ljava/lang/String;)V'],

		['label', 'skip'],
		'return'
	])

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
