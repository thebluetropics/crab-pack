import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod.constant_pool import get_utf8_at
from mod import (
	attribute,
	constant_pool,
	instructions
)
from mod.class_file import (
	load_class_file,
	assemble_class_file
)

def apply():
	if not mod.config.is_feature_enabled('etc.no_entity_shadows'):
		return

	cf = load_class_file(mod.config.path('stage/client/bw.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	_patch_render_clouds_method(cf, cp_cache)

	with open(mod.config.path('stage/client/bw.class'), 'wb') as f:
		f.write(assemble_class_file(cf))

	print('Patched client:bw.class → net.minecraft.client.render.entity.EntityRenderer')

def _patch_render_clouds_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(Lsn;DDDFF)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	# load code attribute
	a_code = attribute.code.load(a[0x02])

	# modify code
	a_code[0x00] = (9).to_bytes(2)
	a_code[0x01] = (10).to_bytes(2)
	a_code[0x03] = a_code[0x03][81:101]

	# update code length
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
