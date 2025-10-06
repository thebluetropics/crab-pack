import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_assemble,
	assemble_code,
	a_code_load
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8,
	get_utf8_at
)
from modmaker.m import (
	create_method,
	get_method
)

def apply():
	if not mod.config.is_one_of_features_enabled(['etc.hunger_and_thirst', 'block.smelter', 'actions']):
		return

	cf = load_class_file(mod.config.path('stage/client/nb.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		cf[0x0d].append(_on_hunger_update(cf, cp_cache))
		cf[0x0d].append(_on_thirst_update(cf, cp_cache))

	if mod.config.is_feature_enabled('block.smelter'):
		_modify_on_open_screen_method(cf, cp_cache)

	if mod.config.is_feature_enabled('actions'):
		cf[0x0d].append(_create_on_actions_update_method(cf, cp_cache))

	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open('stage/client/nb.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:nb.class → net.minecraft.client.network.ClientNetworkHandler')

def _on_hunger_update(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I'],
		['putfield', 'dc', 'hunger', 'I'],

		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I'],
		['putfield', 'dc', 'maxHunger', 'I'],

		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _on_thirst_update(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onThirstUpdate', '(Lcom/thebluetropics/crabpack/ThirstUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/ThirstUpdatePacket', 'thirst', 'I'],
		['putfield', 'dc', 'thirst', 'I'],

		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/ThirstUpdatePacket', 'maxThirst', 'I'],
		['putfield', 'dc', 'maxThirst', 'I'],

		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _modify_on_open_screen_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(Liw;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x01] = (7).to_bytes(2)
	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		'aload_1',
		['getfield', 'iw', 'b', 'I'],
		'iconst_4',
		['if_icmpne', 'next'],

		['new', 'com/thebluetropics/crabpack/SmelterBlockEntity'],
		'dup',
		['invokespecial', 'com/thebluetropics/crabpack/SmelterBlockEntity', '<init>', '()V'],
		['astore', 6],

		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		['aload', 6],
		['invokevirtual', 'dc', 'openSmelterScreen', '(Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V'],

		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		['getfield', 'dc', 'e', 'Ldw;'],
		'aload_1',
		['getfield', 'iw', 'a', 'I'],
		['putfield', 'dw', 'f', 'I'],

		'return',

		['label', 'next']
	]) + a_code[0x03]

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

def _create_on_actions_update_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'onActionsUpdate', '(Lcom/thebluetropics/crabpack/ActionsUpdatePacket;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', 'nb', 'f', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
		'aload_1',
		['getfield', 'com/thebluetropics/crabpack/ActionsUpdatePacket', 'actions', 'I'],
		['putfield', 'dc', 'actions', 'I'],

		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
