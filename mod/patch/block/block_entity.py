from modmaker import *
import mod

def apply(side_name, side):
	if mod.config.is_one_of_features_enabled(['block.smelter']):
		return

	c_name = ('ow', 'jh')[side]
	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	modify_static_initializer(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.entity.BlockEntity')

def modify_static_initializer(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])
	code = []

	if mod.config.is_feature_enabled('block.smelter'): code.extend([
		['ldc.class', 'com/thebluetropics/crabpack/SmelterBlockEntity'],
		['ldc.string', 'Smelter'],
		['invokestatic', c_name, 'a', '(Ljava/lang/Class;Ljava/lang/String;)V']
	])

	code.append('return')
	a_code[0x03] = a_code[0x03][0:-1] + assemble_code(cf, cp_cache, side, len(a_code[0x03] - 1), code)

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
