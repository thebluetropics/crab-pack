from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_one_of_features_enabled(['etc.hunger_and_thirst', 'food.stackable_food']):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['yw', 'px'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0b].append(create_field(cf, cp_cache, ['public', 'final'], 'hungerRestored', 'I'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	_modify_constructor(cf, cp_cache, side, c_name)

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		_modify_use_method(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.FoodItem')

def _modify_constructor(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<init>', '(IIZ)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	patch_code_0 = ['iconst_1'] if not mod.config.is_feature_enabled('food.stackable_food') else [['bipush', 16]]
	patch_code_1 = None

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		patch_code_1 = [
			'aload_0',
			['bipush', 50],
			['putfield', c_name, 'hungerRestored', 'I'],
			'return'
		]
	else:
		patch_code_1 = ['return']

	a_code[0x03] = a_code[0x03][0:16] + assemble_code(cf, cp_cache, side, 16, patch_code_0) + a_code[0x03][17:20] + assemble_code(cf, cp_cache, side, 20, patch_code_1)
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_use_method(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:18] + assemble_code(cf, cp_cache, side, 0, [
		'aload_3',
		'aload_0',
		['getfield', c_name, 'hungerRestored', 'I'],
		['invokevirtual', ('gs', 'em'), 'restoreHunger', '(I)V'],
	]) + a_code[0x03][18:20]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
