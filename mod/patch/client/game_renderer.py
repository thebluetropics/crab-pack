from modmaker import *
import mod

def apply():
	if not mod.config.is_one_of_features_enabled(['debug.pause_prevention', 'zoom']):
		return

	cf = load_class_file(mod.config.path('stage/client/px.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'useDebugFov', 'Z'))

	if mod.config.is_feature_enabled('debug.pause_prevention'):
		_modify_on_frame_update_method(cf, cp_cache)

	if mod.config.is_feature_enabled('zoom'):
		_modify_render_method(cf, cp_cache)

	with open(mod.config.path('stage/client/px.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:px.class → net.minecraft.client.render.GameRenderer')

def _modify_on_frame_update_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(F)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])
	a_code[0x03] = a_code[0x03][0:21] + assemble_code(cf, cp_cache, 0, 21, [
		'aload_0',
		['getfield', 'px', 'j', 'Lnet/minecraft/client/Minecraft;'],
		['invokevirtual', 'net/minecraft/client/Minecraft', 'h', '()V'],
	]) + a_code[0x03][28:len(a_code[0x03])]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_render_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(FJ)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		'fload_1',
		['invokestatic', 'com/thebluetropics/crabpack/Zoom', 'onRenderBegin', '(F)F'],
		'f2d',
		['putfield', 'px', 'E', 'D']
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
