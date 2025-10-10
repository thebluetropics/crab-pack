from modmaker import *
import mod

def apply():
	if not mod.config.is_one_of_features_enabled(['block.persistent_leaves', 'debug.no_clouds']):
		return

	cf = load_class_file(mod.config.path('stage/client/n.class'))
	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('block.persistent_leaves'):
		_modify_reload_method(cf, cp_cache)

	if mod.config.is_feature_enabled('debug.no_clouds'):
		_patch_render_clouds_method(cf, cp_cache)

	with open(mod.config.path('stage/client/n.class'), 'wb') as f:
		f.write(cf_assemble(cf))

	print('Patched client:n.class → net.minecraft.client.render.WorldRenderer')

def _modify_reload_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		['getstatic', 'uu', 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'],
		'aload_0',
		['getfield', 'n', 't', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'z', 'Lkv;'],
		['getfield', 'kv', 'j', 'Z'],
		['invokevirtual', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'setFancyGraphics', '(Z)V']
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _patch_render_clouds_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(F)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x00] = (0).to_bytes(2)
	a_code[0x01] = (2).to_bytes(2)
	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
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
