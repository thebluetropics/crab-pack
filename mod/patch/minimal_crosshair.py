from modmaker import *
import mod, shutil

def apply():
	if not mod.config.is_feature_enabled('minimal_crosshair'):
		return

	shutil.copy(
		mod.config.path('class_files/com/thebluetropics/crabpack/MinimalCrosshair.class'),
		mod.config.path('stage', 'client', 'com/thebluetropics/crabpack/MinimalCrosshair.class')
	)

	cf = load_class_file(mod.config.path('stage/client/qq.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, '<init>', '(Lkv;II)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	code = load_code(cp_cache, a_code[0x03])
	del code[-1]
	code = code + [
		'aload_0', ['getfield', 'qq', 'c', 'I'],
		'aload_0', ['getfield', 'qq', 'd', 'I'],
		'aload_0', ['getfield', 'qq', 'e', 'I'],
		['invokestatic', 'com/thebluetropics/crabpack/MinimalCrosshair', 'beforeRenderCrosshair', '(III)V'],
		'return'
	]
	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, code)
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/qq.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:qq.class → ScreenScaler')
