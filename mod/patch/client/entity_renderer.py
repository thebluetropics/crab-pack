from modmaker import *
import mod

def apply():
	if not mod.config.is_feature_enabled('etc.no_entity_shadows'):
		return

	cf = load_class_file(mod.config.path('stage/client/bw.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_patch_post_render_method(cf, cp_cache)

	with open(mod.config.path('stage/client/bw.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:bw.class → net.minecraft.client.render.entity.EntityRenderer')

def _patch_post_render_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(Lsn;DDDFF)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x00] = (9).to_bytes(2)
	a_code[0x01] = (10).to_bytes(2)
	a_code[0x03] = a_code[0x03][81:101]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
