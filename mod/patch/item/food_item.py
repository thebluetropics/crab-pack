import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod.field import create_field
from mod.constant_pool import get_utf8_at
from mod import (
	class_file,
	attribute,
	constant_pool,
	instructions
)
from mod.constant_pool import (
	icpx_f,
	icpx_m
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = ['yw', 'px'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(cf, cp_cache, ['public', 'final'], 'hungerRestored', 'I'))

	_modify_constructor(cf, cp_cache, c_name)

	if mod.config.is_feature_enabled('experimental.hunger_and_thirst'):
		_modify_use_method(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.FoodItem')

def _modify_constructor(cf, cp_cache, c_name):
	m = get_method(cf, cp_cache, '<init>', '(IIZ)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	patch_code_0 = ['iconst_1'] if not mod.config.is_feature_enabled('food.stackable_food') else [['bipush', 16]]
	patch_code_1 = None

	if mod.config.is_feature_enabled('experimental.hunger_and_thirst'):
		patch_code_1 = [
			'aload_0',
			['bipush', 50],
			['putfield', icpx_f(cf, cp_cache, c_name, 'hungerRestored', 'I')],
			'return'
		]
	else:
		patch_code_1 = ['return']

	a_code[0x03] = a_code[0x03][0:16] + instructions.assemble(16, patch_code_0) + a_code[0x03][17:20] + instructions.assemble(20, patch_code_1)
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

def _modify_use_method(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:18] + instructions.assemble(0, [
		'aload_3',
		'aload_0',
		['getfield', icpx_f(cf, cp_cache, c_name, 'hungerRestored', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, ['gs', 'em'][side], 'restoreHunger', '(I)V')],
	]) + a_code[0x03][18:20]
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
