from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_one_of_features_enabled(['etc.hunger_and_thirst', 'actions']):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['ki', 'gt'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_static_initializer(cf, cp_cache, side_name)

	with open(f'stage/{side_name}/{c_name}.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.network.packet.Packet')

def _modify_static_initializer(cf, cp_cache, side_name):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	if side_name.__eq__('client'):
		a_code[0x03] = a_code[0x03][0:552] + assemble_code(cf, cp_cache, 0, 0, [
			*([] if not mod.config.is_feature_enabled('etc.hunger_and_thirst') else [
				['sipush', 201],
				'iconst_1',
				'iconst_1',
				['ldc_w.class', 'com/thebluetropics/crabpack/HungerUpdatePacket'],
				['invokestatic', 'ki', 'a', '(IZZLjava/lang/Class;)V'],

				['sipush', 202],
				'iconst_1',
				'iconst_1',
				['ldc_w.class', 'com/thebluetropics/crabpack/ThirstUpdatePacket'],
				['invokestatic', 'ki', 'a', '(IZZLjava/lang/Class;)V']
			]),
			*([] if not mod.config.is_feature_enabled('actions') else [
				['sipush', 203],
				'iconst_1',
				'iconst_1',
				['ldc_w.class', 'com/thebluetropics/crabpack/ActionsUpdatePacket'],
				['invokestatic', 'ki', 'a', '(IZZLjava/lang/Class;)V']
			])
		]) + a_code[0x03][552:567]

	if side_name.__eq__('server'):
		a_code[0x03] = a_code[0x03][0:541] + assemble_code(cf, cp_cache, 1, 0, [
			*([] if not mod.config.is_feature_enabled('etc.hunger_and_thirst') else [
				['sipush', 201],
				'iconst_1',
				'iconst_1',
				['ldc_w.class', 'com/thebluetropics/crabpack/HungerUpdatePacket'],
				['invokestatic', 'gt', 'a', '(IZZLjava/lang/Class;)V'],

				['sipush', 202],
				'iconst_1',
				'iconst_1',
				['ldc_w.class', 'com/thebluetropics/crabpack/ThirstUpdatePacket'],
				['invokestatic', 'gt', 'a', '(IZZLjava/lang/Class;)V']
			]),
			*([] if not mod.config.is_feature_enabled('actions') else [
				['sipush', 203],
				'iconst_1',
				'iconst_1',
				['ldc_w.class', 'com/thebluetropics/crabpack/ActionsUpdatePacket'],
				['invokestatic', 'gt', 'a', '(IZZLjava/lang/Class;)V']
			])
		]) + a_code[0x03][541:566]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
