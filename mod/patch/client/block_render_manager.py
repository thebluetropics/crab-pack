import mod, struct

from mod.attribute import get_attribute
from mod.method import get_method, create_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	icpx_double,
	i2cpx_utf8,
	get_utf8_at
)

def to_double(value):
	return struct.pack(">d", float(value))

def apply():
	if not mod.config.is_feature_enabled('block.mortar'):
		return

	cf = class_file.load(mod.config.path('stage/client/cv.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	_modify_render_method(cf, cp_cache)

	cf[0x0d].append(_create_render_mortar_method(cf, cp_cache))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open(mod.config.path('stage/client/cv.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:cv.class → net.minecraft.client.render.BlockRenderManager')

def _modify_render_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(Luu;III)Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:18] + instructions.assemble(18, [
		['iload', 5],
		['bipush', 50],
		['if_icmpne*', 'skip'],

		'aload_0',
		'aload_1',
		['iload', 2],
		['iload', 3],
		['iload', 4],
		['invokevirtual', icpx_m(cf, cp_cache, 'cv', 'renderMortar', '(Luu;III)Z')],
		'ireturn',

		['jump_target*', 'skip'],
	]) + a_code[0x03][18:324]

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

def _create_render_mortar_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'renderMortar', '(Luu;III)Z')

	code = [
		['getstatic', icpx_f(cf, cp_cache, 'nw', 'a', 'Lnw;')],
		['astore', 5],

		['aload', 1],
		['aload_0'],
		['getfield', icpx_f(cf, cp_cache, 'cv', 'c', 'Lxp;')],
		['iload', 2],
		['iload', 3],
		['iload', 4],
		['invokevirtual', icpx_m(cf, cp_cache, 'uu', 'd', '(Lxp;III)F')],
		['fstore', 6],

		['aload', 5], ['fload', 6], ['fload', 6], ['fload', 6],
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(FFF)V')],

		['ldc2_w', icpx_double(cf, cp_cache, to_double(64.0 / 256.0))],
		['dstore', 7],

		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))],
		['dstore', 9],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['dload', 7], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['dload', 9], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['dload', 7], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['dload', 9], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['dload', 7], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['dload', 9], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['dload', 7], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['dload', 9], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(2.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(80.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((3.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((3.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(2.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(80.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((3.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((13.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(2.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(80.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((13.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((13.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(2.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(80.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((13.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((3.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	]
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(96.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(96.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(96.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(96.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(13.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(1.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((1.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(0.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((16.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],

		['aload', 5],
		['iload', 2], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(15.0 / 16.0))], 'dadd',
		['iload', 3], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(6.0 / 16.0))], 'dadd',
		['iload', 4], 'i2d', ['ldc2_w', icpx_double(cf, cp_cache, to_double(3.0 / 16.0))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(112.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((15.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['ldc2_w', icpx_double(cf, cp_cache, to_double(176.0 / 256.0))], ['ldc2_w', icpx_double(cf, cp_cache, to_double((10.0 / 16.0) * (16.0 / 256.0)))], 'dadd',
		['invokevirtual', icpx_m(cf, cp_cache, 'nw', 'a', '(DDDDD)V')],
	])
	code.extend([
		'iconst_1',
		'ireturn'
	])
	code = instructions.assemble(0, code)
	a_code = attribute.code.assemble([
		(13).to_bytes(2),
		(11).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
